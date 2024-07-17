import base64
from email.message import EmailMessage
import ssl
import smtplib
import os
import pika
from pika.exchange_type import ExchangeType
import logging
import json
from dotenv import load_dotenv
load_dotenv()

email_sender = "projectproject163@gmail.com"




def gmail_send_message(preference, sender_email,response):
    em = EmailMessage()
    em['from'] = sender_email
    subject=preference.get("_id", "")
    em['subject'] = f"The Latest News in {subject}" 
    em.set_content(response)
    context = ssl.create_default_context()
    email_recivers=preference.get('notificationGroup', [])
    for email_reciver in email_recivers:
        em['to'] = email_reciver
        message = em.as_string()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, os.getenv('GMAIL_PASSCODE'))
            server.sendmail(sender_email, email_reciver, message)
            
            
def on_message_received(ch, method, properties, body): 
    logging.info(f'Processing message: {body.decode("utf-8")}') 
    data_str = body.decode("utf-8")
    try:
        data_json = json.loads(data_str)
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON: {e}')
        return   
    logging.info(f'Processing data: {data_json.get("data", [])}') 
    data_array = data_json.get("data", [])
    for item in data_array:
        preference = item.get("preference", {})
        response = item.get("response", "")
        gmail_send_message(preference, email_sender,response)
    logging.info('Message processed successfully')
    logging.info(method.delivery_tag)
    logging.info(ch.basic_ack(delivery_tag=method.delivery_tag))
    
def gmail_consumers(on_message_received):
    connection_parameters = pika.ConnectionParameters('rabbitmq')

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

    queue = channel.queue_declare(queue='', exclusive=True)

    channel.queue_bind(exchange='topic', queue=queue.method.queue, routing_key='gmail.#')

    channel.basic_consume(queue=queue.method.queue, auto_ack=True,
    on_message_callback=on_message_received)

    logging.info('Payments Starting Consuming')

    channel.start_consuming()


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  gmail_consumers(on_message_received)
 