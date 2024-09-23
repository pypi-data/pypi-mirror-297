import unittest
from unittest.mock import patch, MagicMock
from intelliw.utils.kafka import KafkaClient


class TestKafkaClient(unittest.TestCase):

    @patch('confluent_kafka.Producer')
    def test_create_producer_with_default_config(self, mock_producer):
        # 测试使用默认配置创建生产者
        kafka_client = KafkaClient(brokers='localhost:9092')
        producer = kafka_client.create_producer()

        # 验证 Producer 被正确实例化
        mock_producer.assert_called_once_with({
            'bootstrap.servers': 'localhost:9092',
            'linger.ms': 10,
            'batch.num.messages': 1000,
            'queue.buffering.max.ms': 1000,
            'message.timeout.ms': 30000,
            'retries': 5,
        })

    @patch('confluent_kafka.Producer')
    def test_create_producer_with_custom_config(self, mock_producer):
        # 测试使用自定义配置创建生产者
        custom_config = {'compression.type': 'gzip', 'acks': 'all'}
        kafka_client = KafkaClient(brokers='localhost:9092', producer_config=custom_config)
        producer = kafka_client.create_producer()

        # 验证自定义配置覆盖了默认配置
        mock_producer.assert_called_once_with({
            'bootstrap.servers': 'localhost:9092',
            'linger.ms': 10,
            'batch.num.messages': 1000,
            'queue.buffering.max.ms': 1000,
            'message.timeout.ms': 30000,
            'retries': 5,
            'compression.type': 'gzip',
            'acks': 'all',
        })

    @patch('confluent_kafka.Consumer')
    def test_create_consumer_with_default_config(self, mock_consumer):
        # 测试使用默认配置创建消费者
        kafka_client = KafkaClient(brokers='localhost:9092', group_id='test-group')
        consumer = kafka_client.create_consumer(topics=['test-topic'])

        # 验证 Consumer 被正确实例化
        mock_consumer.assert_called_once_with({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'test-group',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        })
        mock_consumer.return_value.subscribe.assert_called_once_with(['test-topic'])

    @patch('confluent_kafka.Consumer')
    def test_create_consumer_with_custom_config(self, mock_consumer):
        # 测试使用自定义配置创建消费者
        custom_config = {'auto.offset.reset': 'latest', 'enable.auto.commit': True}
        kafka_client = KafkaClient(brokers='localhost:9092', group_id='test-group', consumer_config=custom_config)
        consumer = kafka_client.create_consumer(topics=['test-topic'])

        # 验证自定义配置覆盖了默认配置
        mock_consumer.assert_called_once_with({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'test-group',
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True,
        })
        mock_consumer.return_value.subscribe.assert_called_once_with(['test-topic'])

    @patch('confluent_kafka.Producer')
    def test_produce_message(self, mock_producer):
        # 测试生产消息功能
        kafka_client = KafkaClient(brokers='localhost:9092')
        kafka_client.produce_message(topic='test-topic', key='key1', value='value1')

        # 验证消息生产流程被调用
        mock_producer.return_value.produce.assert_called_once_with(
            'test-topic', key='key1', value='value1', callback=unittest.mock.ANY
        )
        mock_producer.return_value.flush.assert_called_once()

    @patch('confluent_kafka.Consumer')
    def test_consume_message(self, mock_consumer):
        # 测试消费消息功能
        kafka_client = KafkaClient(brokers='localhost:9092', group_id='test-group')

        mock_msg = MagicMock()
        mock_msg.error.return_value = None
        mock_msg.key.return_value = 'key1'
        mock_msg.value.return_value = 'value1'
        mock_consumer.return_value.poll.return_value = mock_msg

        def handle_func(key, value):
            self.assertEqual(key, 'key1')
            self.assertEqual(value, 'value1')

        kafka_client.consume_messages(topics=['test-topic'], handle_func=handle_func)

        # 验证消息消费流程被调用
        mock_consumer.return_value.poll.assert_called()
        mock_consumer.return_value.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
