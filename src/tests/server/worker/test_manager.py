import pytest
import sys

sys.path.append("/src")

from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.jobs.job import Job, JobStatus
from app.server.worker.manager import Manager


@pytest.fixture
def manager():
    manager = Manager()
    manager.start()
    yield manager
    manager.stop()


class TestManagerStartStop:
    def test_manager_start_stop(self, manager):
        assert manager.worker.is_alive()


class TestManagerSingleton:
    @pytest.mark.skip(
        "This test currently causes problems related to Popen._children references"
    )
    def test_manager_single_instance(self, manager):
        other_manager = Manager()
        assert manager is other_manager
        del other_manager


class TestManagerRunsJob:
    def test_manager_runs_job(self, manager: Manager):
        job = manager.submit_job(EXAMPLE_MODELS["TJoint"])
        manager.wait_for_job(job.id)
        jobout = manager.get_job(job.id)
        assert jobout.status == JobStatus.RUNNING
        assert jobout.error is None

    def test_manager_raises_error(self, manager):
        pass
