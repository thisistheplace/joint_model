import pytest
import sys

sys.path.append("/src")

from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.jobs.job import Job
from app.server.worker.worker import Worker
from app.server.worker.runner import RunJob


@pytest.fixture
def worker() -> Worker:
    worker = Worker()
    worker.start()
    yield worker
    worker.stop()


@pytest.fixture
def job() -> Job:
    return Job(EXAMPLE_MODELS["TJoint"])


@pytest.fixture
def runner(worker, job) -> RunJob:
    runner = RunJob(worker, job, False)
    yield runner
    if runner.is_alive():
        runner.stop()


class TestRunJob:
    def test_runjob_success(self, runner):
        runner.start()
        runner.wait()
        runner.stop()
        assert not runner.is_alive()
