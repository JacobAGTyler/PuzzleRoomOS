import pytest

from kafka import KafkaConsumer, KafkaAdminClient
from kafka.errors import NoBrokersAvailable, NodeNotReadyError


class TestKafkaConnect:
    # def test_consumer_connect(self):
    #     kc = KafkaConsumer(bootstrap_servers='broker:29092')
    #
    #     assert isinstance(kc, KafkaConsumer)

    def test_consumer_connect_fail(self):
        with pytest.raises(NoBrokersAvailable):
            kc = KafkaConsumer(bootstrap_servers='broker:29093')

    # def test_admin_connect(self):
    #     with pytest.raises(NodeNotReadyError):
    #         ka = KafkaAdminClient(bootstrap_servers='broker:29092')
