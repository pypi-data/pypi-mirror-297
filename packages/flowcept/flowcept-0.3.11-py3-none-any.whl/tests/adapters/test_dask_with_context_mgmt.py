import unittest
import numpy as np

from dask.distributed import Client

from flowcept import FlowceptConsumerAPI
from flowcept.commons.flowcept_logger import FlowceptLogger
from flowcept.commons.utils import assert_by_querying_tasks_until
from flowcept.flowceptor.adapters.dask.dask_plugins import (
    register_dask_workflow,
)
from tests.adapters.dask_test_utils import (
    setup_local_dask_cluster,
    close_dask,
)


def dummy_func1(x):
    cool_var = "cool value"  # test if we can intercept this var
    print(cool_var)
    y = cool_var
    return x * 2


class TestDaskContextMgmt(unittest.TestCase):
    client: Client = None
    cluster = None
    consumer = None

    def __init__(self, *args, **kwargs):
        super(TestDaskContextMgmt, self).__init__(*args, **kwargs)
        self.logger = FlowceptLogger()

    @classmethod
    def setUpClass(cls):
        (
            TestDaskContextMgmt.client,
            TestDaskContextMgmt.cluster,
            TestDaskContextMgmt.consumer,
        ) = setup_local_dask_cluster(TestDaskContextMgmt.consumer, 2)

    def test_workflow(self):
        i1 = np.random.random()
        register_dask_workflow(self.client)
        with FlowceptConsumerAPI():
            o1 = self.client.submit(dummy_func1, i1)
            self.logger.debug(o1.result())
            self.logger.debug(o1.key)

            assert assert_by_querying_tasks_until(
                {"task_id": o1.key},
                condition_to_evaluate=lambda docs: "ended_at" in docs[0],
            )

    @classmethod
    def tearDownClass(cls):
        print("Ending tests!")
        try:
            close_dask(
                TestDaskContextMgmt.client, TestDaskContextMgmt.cluster
            )
        except Exception as e:
            print(e)
            pass

        if TestDaskContextMgmt.consumer:
            TestDaskContextMgmt.consumer.stop()
