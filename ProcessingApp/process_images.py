import pika
import os

# Connection parameters for RabbitMQ
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_FILE_QUEUE = 'file_queue'
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')

def process_file(file_data, file_name):
    # Check if the file contains 'dog' or 'cat'
    if b'dog' in file_data:
        animal_check = "File contains 'dog'."
    elif b'cat' in file_data:
        animal_check = "File contains 'cat'."
    else:
        animal_check = "File contains neither 'dog' nor 'cat'."

    # Calculate file size
    file_size = len(file_data)

    # Construct processing result
    processing_result = f"{animal_check} File size: {file_size} bytes."

    return processing_result

def callback(ch, method, properties, body):
    file_data = body

    # Process the file data and get processing result
    processing_result = process_file(file_data, method.routing_key)

    # Send processing status back to RabbitMQ using the correlation ID and reply-to queue
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=processing_result
    )

    print("Processing completed for file:", method.routing_key)  # Print for debugging
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message processing

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    )
)
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_FILE_QUEUE)
channel.basic_consume(queue=RABBITMQ_FILE_QUEUE, on_message_callback=callback, auto_ack=False)
print('Waiting for messages...')
channel.start_consuming()
