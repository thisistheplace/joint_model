import pytest
import sys
from unittest import mock

sys.path.append("/src")

from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.job import Job
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


class TestWorkerSingleton:
    @pytest.mark.skip(
        "This test currently causes problems related to Popen._children references"
    )
    def test_worker_single_instance(self, worker):
        other_worker = Worker()
        assert worker is other_worker
        del other_worker


class TestWorkerRunsJob:
    def test_worker_runs_job(self, worker):
        jobin = Job(EXAMPLE_MODELS["TJoint"])
        worker.inqueue.put(jobin)
        jobout = worker.outqueue.get(timeout=5)
        assert jobin.id == jobout.id
        assert jobout.error is None
        assert jobin.data == jobout.data

    def test_worker_raises_error(self, worker):
        pass
