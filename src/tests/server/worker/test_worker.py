import pytest
import sys

sys.path.append("/src")

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
