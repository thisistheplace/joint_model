import pytest
import sys

sys.path.append("src")

from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.jobs.job import Job
from app.server.worker.worker import Worker, WorkerException


@pytest.fixture
def worker():
    worker = Worker()
    worker.start()
    yield worker
    worker.stop()


class TestWorkerStartStop:
    def test_worker_start_stop(self, worker):
        assert worker.is_alive()


class TestWorkerRunsJob:
    def test_worker_submits_job(self, worker):
        jobin = Job(EXAMPLE_MODELS["KJoint"])
        worker.submit(jobin)
        jobout = worker.outqueue.get(timeout=5)
        assert jobin.id == jobout.id
        assert jobout.error is None
        assert jobin.data == jobout.data
