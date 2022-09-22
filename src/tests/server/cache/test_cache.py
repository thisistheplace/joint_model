import pytest
import sys

sys.path.append("/src")

from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.jobs.job import Job, JobStatus
from app.server.cache.cache import Cache, get_job, store_job


@pytest.fixture
def cache() -> Cache:
    cache = Cache()
    yield cache
    del cache


@pytest.fixture
def job() -> Job:
    yield Job(EXAMPLE_MODELS["TJoint"])


class TestCacheSingleton:
    def test_cache_single_instance(self, cache):
        other_cache = Cache()
        assert cache is other_cache
        del other_cache


class TestCache:
    def test_store_job(self, cache: Cache, job: Job):
        store_job(job)
        with cache.store as store:
            assert job.id in store
            assert job is store[job.id]

    def test_get_job(self, cache: Cache, job: Job):
        store_job(job)
        other_job = get_job(job.id)
        assert other_job.id == job.id
        assert other_job.status == job.status
        assert other_job is not job
