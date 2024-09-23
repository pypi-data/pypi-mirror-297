
try:
    from confluent_kafka import Producer, Consumer, KafkaError
except ImportError:
    raise ImportError("\033[31mIf use kafka, you need: pip install confluent_kafka>=2.5.3 \033[0m")
import threading


class KafkaClient:
    def __init__(self, brokers: str, group_id: str = None, producer_config: dict = None, consumer_config: dict = None):
        """
        Kafka 通用客户端初始化
        :param brokers: Kafka 集群的地址 (例如 'localhost:9092')
        :param group_id: 消费者使用的分组ID，生产者可忽略
        :param producer_config: 自定义的生产者配置字典
        :param consumer_config: 自定义的消费者配置字典
        """
        self.brokers = brokers
        self.group_id = group_id
        self.producer_config = producer_config or {}  # 用户自定义的生产者配置
        self.consumer_config = consumer_config or {}  # 用户自定义的消费者配置

    def create_producer(self):
        """创建 Kafka 生产者，优先使用用户传入配置"""
        default_producer_conf = {
            'bootstrap.servers': self.brokers,
            'linger.ms': 10,  # 批量发送时等待时间
            'batch.num.messages': 1000,  # 批量发送的最大消息数
            'queue.buffering.max.ms': 1000,  # 最大缓冲时间
            'message.timeout.ms': 30000,  # 消息超时配置
            'retries': 5,  # 消息发送失败重试次数
        }
        # 将用户配置合并到默认配置中
        config = {**default_producer_conf, **self.producer_config}
        return Producer(config)

    def create_consumer(self, topics: list):
        """创建 Kafka 消费者，优先使用用户传入配置"""
        default_consumer_conf = {
            'bootstrap.servers': self.brokers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',  # 从最早的偏移量开始消费
            'enable.auto.commit': False,  # 手动提交偏移量
        }
        # 将用户配置合并到默认配置中
        config = {**default_consumer_conf, **self.consumer_config}
        consumer = Consumer(config)
        consumer.subscribe(topics)
        return consumer

    def produce_message(self, topic: str, key: str, value: str):
        """发送 Kafka 消息"""
        producer = self.create_producer()

        def delivery_callback(err, msg):
            if err:
                print(f"Message failed delivery: {err}")
            else:
                print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

        try:
            producer.produce(topic, key=key, value=value, callback=delivery_callback)
            producer.flush()  # 确保消息发送
        except Exception as e:
            print(f"Error producing message: {e}")

    def consume_messages(self, topics: list, handle_func, timeout=1.0):
        """消费 Kafka 消息"""
        consumer = self.create_consumer(topics)

        try:
            while True:
                msg = consumer.poll(timeout)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        print(f"Kafka error: {msg.error()}")
                    continue

                handle_func(msg.key(), msg.value())  # 处理消息
                consumer.commit()  # 手动提交偏移量

        except Exception as e:
            print(f"Error consuming messages: {e}")
        finally:
            consumer.close()

    def consume_messages_with_threads(self, topics: list, handle_func, num_threads=5, timeout=1.0):
        """多线程消费 Kafka 消息"""
        def consumer_thread():
            self.consume_messages(topics, handle_func, timeout)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=consumer_thread)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


# 消费者处理函数示例
def handle_message(key, value):
    print(f"Received message with key: {key}, value: {value}")


