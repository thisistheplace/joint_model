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
        job_in = manager.submit_job(EXAMPLE_MODELS["TJoint"])
        job_out = manager.wait_for_job(job_in.id)
        assert job_out.status == JobStatus.COMPLETE
        assert job_out.error is None

    def test_manager_raises_error(self, manager):
        pass
