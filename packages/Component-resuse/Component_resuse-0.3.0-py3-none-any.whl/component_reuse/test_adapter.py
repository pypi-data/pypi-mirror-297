from Pipify_Components_Package.rabbitmq_adapter import RabbitMQAdapter

def test_rabbitmq_connection():
    adapter = RabbitMQAdapter(host='localhost', username='', password='', queue='default')
    adapter.connect()
    adapter.close_connection()

if __name__ == "__main__":
    test_rabbitmq_connection()