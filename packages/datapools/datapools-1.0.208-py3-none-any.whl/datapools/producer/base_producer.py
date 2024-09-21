import asyncio
import json

# import importlib
# import inspect
import os

# import sys
import traceback

# from enum import Enum
from typing import Optional, Set

from ..common.backend_api import BackendAPI, BackendAPIException
from ..common.logger import logger
from ..common.queues import GenericQueue, QueueMessage, QueueMessageType, QueueRole, QueueRoutedMessage
from ..common.session_manager import SessionManager, Session, ContentStatus
from ..common.stoppable import Stoppable
from ..common.storage.file_storage import FileStorage
from ..common.storage.metadata_storage import MetadataStorage
from ..common.storage.session_file_storage import SessionFileStorage
from ..common.types import (
    BaseProducerSettings,
    InvalidUsageException,
    SchedulerEvaluationReport,
    EvaluationStatus,
    WorkerEvaluationReport,
    ProducerTask,
)
from ..worker.utils import get_worker_storage_invalidation_routing_key


# from .rules import DatapoolRulesChecker


class BaseProducer(Stoppable):
    cfg: BaseProducerSettings
    reports_queue: GenericQueue
    eval_queue: GenericQueue
    worker_reports_exchange: GenericQueue
    todo_tasks: Set[asyncio.Task]

    def __init__(self, cfg: Optional[BaseProducerSettings] = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else BaseProducerSettings()
        self.session_manager = SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)

        if not self.cfg.CLI_MODE:
            self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)
        
        self.todo_tasks = set()

        # receives tasks from workers
        self.eval_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.EVAL_TASKS_QUEUE_NAME,
            size=self.cfg.MAX_PROCESSING_TASKS
        )
        logger.info("created receiver eval_tasks")

        # will invalidate worker cache entries
        self.worker_reports_exchange = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=None,
            exchange_name=self.cfg.STORAGE_INVALIDATION_EXCHANGE_NAME,
        )
        logger.info("created publisher worker_tasks")

        # sends reports to the scheduler
        self.reports_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.REPORTS_QUEUE_NAME,
        )

        if self.cfg.CLI_MODE is True:
            self.stop_task_received = asyncio.Event()

        # self.datapool_rules_checker = DatapoolRulesChecker()

    async def run(self):
        self.tasks.append(asyncio.create_task(self.router_loop()))
        await self.eval_queue.run()
        await self.worker_reports_exchange.run()
        await self.reports_queue.run()
        await super().run()

    async def wait(self):
        if self.cfg.CLI_MODE is False:
            logger.error("baseproducer invalid usage")
            raise InvalidUsageException("not a cli mode")

        logger.info("BaseProducer wait()")
        await self.stop_task_received.wait()
        logger.info("BaseProducer stop_task_received")
        waiters = (
            self.eval_queue.until_empty(),
            self.worker_reports_exchange.until_empty(),
            self.reports_queue.until_empty(),
        )
        await asyncio.gather(*waiters)
        logger.info("BaseProducer wait done")

    async def stop(self):
        logger.debug("waiting todo tasks..")
        while len(self.st_todo_tasks) > 0 or len(self.todo_tasks) > 0:
            await asyncio.sleep(0.2)
        logger.debug("todo tasks done")

        await self.eval_queue.stop()
        await self.worker_reports_exchange.stop()
        await self.reports_queue.stop()
        await super().stop()
        logger.info("BaseProducer stopped")

    async def router_loop(self):
        try:
            def on_done(task: asyncio.Task):
                logger.debug(f"_process_task done {task=}")
                self.todo_tasks.discard(task)
                logger.debug(f"{len(self.todo_tasks)} still working")

            sleep_time = 0
            while not await self.is_stopped(sleep_time):
                if len(self.todo_tasks) < self.cfg.MAX_PROCESSING_TASKS:
                    message = await self.eval_queue.pop(timeout=0.2)
                    if message:
                        task = asyncio.create_task( self._process_task(message))
                        task.add_done_callback(on_done)
                        self.todo_tasks.add(task)
                    sleep_time = 0
                else:
                    sleep_time = 0.1

        except Exception as e:
            logger.error(f"Catched: {traceback.format_exc()}")
            logger.error(f"!!!!!!! Exception in Datapools::router_loop() {e}")
            
    async def _process_task(self, message):
        qm = QueueMessage.decode(message.body)
        logger.info(f"{qm.session_id=}")

        storage_file_path: Optional[str] = None
        started_evaluation = False
        try:
            session = await self.session_manager.get(qm.session_id)
            if (
                session is None
            ):  # or not await session.is_alive(): <= PROCESS EVEN IF SESSION IS STOPPED - crawled content still have to be processed to the end
                # logger.info(f"session is deleted or stopped {qm.session_id=} {message.message_id}")
                logger.info(f"session is deleted {qm.session_id=} {message.message_id}")
                await self.eval_queue.mark_done(message)
                return
                        

            if qm.type == QueueMessageType.Task:
                task = ProducerTask(**qm.data)
                logger.info(f"Producer got: {task}")
                
                if not await session.start_evaluation(message.message_id):
                    logger.info( f"message is being processed already {message.message_id}")
                    await self._reject_message(message, qm.session_id, requeue=True)
                    await asyncio.sleep(5)
                    return
                
                started_evaluation = True

                if not self.is_shared_storage():
                    # copying file
                    path = self.cfg.STORAGE_PATH
                    # if not os.path.exists(path):  # type: ignore
                    #     os.mkdir(path)  # type: ignore
                    storage = FileStorage(path)
                    # put data into persistent storage
                    session_storage = SessionFileStorage(self.cfg.WORKER_STORAGE_PATH, session.id)
                    with session_storage.get_reader(task.storage_id) as raw_data_reader:
                        await storage.put(task.storage_id, raw_data_reader)
                    storage_file_path = storage.get_path(task.storage_id)

                    if task.metadata is not None:
                        metadata_storage = MetadataStorage(path)
                        await metadata_storage.put(task.storage_id, json.dumps(task.metadata.model_dump()))

                await self.process_content(session, task)

            elif qm.type == QueueMessageType.Stop:
                logger.info("base_producer: stop task received")
                self.stop_task_received.set()
            else:
                raise Exception(f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}")

            await self.eval_queue.mark_done(message)
        except BackendAPIException as e:
            logger.error("Caught BackendAPIException")
            logger.error(traceback.format_exc())
            if storage_file_path is not None:
                os.unlink(storage_file_path)
            await self.eval_queue.reject(message, requeue=True)
            await asyncio.sleep(5)
        except Exception as e:
            logger.error("Caught Exception")
            logger.error(traceback.format_exc())
            if storage_file_path is not None:
                os.unlink(storage_file_path)
            await self.eval_queue.reject(message, requeue=False)
            await self._report_evaluation(session, task, EvaluationStatus.Failure)        
            
        finally:
            if started_evaluation:
                await session.finish_evaluation(message.message_id)

    async def process_content(self, session: Session, task: ProducerTask):
        if await session.exists():  # session may have been deleted while processing content
            await self._report_evaluation(session, task, EvaluationStatus.Success)

    async def _report_evaluation(self, session: Session, task: ProducerTask, status: EvaluationStatus):
        await session.set_content_status(
            task.content_key,
            (
                ContentStatus.EVALUATION_SUCCESS
                if status == EvaluationStatus.Success
                else ContentStatus.EVALUATION_FAILURE
            ),
        )
        report = SchedulerEvaluationReport(status=status)
        await self.reports_queue.push(
            QueueMessage(session_id=session.id, message_type=QueueMessageType.ReportEvaluation, data=report)
        )
        await self.worker_reports_exchange.push(
            QueueRoutedMessage(
                get_worker_storage_invalidation_routing_key(task.worker_id),
                WorkerEvaluationReport(
                    url=task.url,
                    storage_id=task.storage_id,
                    session_id=session.id,
                    is_shared_storage=self.is_shared_storage(),
                    status=status,
                ),
            )
        )

    def is_shared_storage(self):
        return self.cfg.STORAGE_PATH is None or self.cfg.WORKER_STORAGE_PATH == self.cfg.STORAGE_PATH
