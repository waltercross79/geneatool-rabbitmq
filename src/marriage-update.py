import requests
import sys
import json
import time
import pika

credentials = pika.PlainCredentials('admin', 'admin2017')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.30.5.1', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='personal_records',
                         exchange_type='direct',
                         durable=True)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='personal_records',
                    queue=queue_name,
                    routing_key='marriage')

print(' [*] Waiting for logs. To exit press CTRL+C')

def on_marriage_added(ch, method, properties, body):
    # call rest marriage service and submit the update
    # body is json object with values
    # recordType: marriage
    # recordDate: yyyy-MM-dd
    # bride: id
    # groo: id
    record = json.loads(body)
    # if record.recordType == "marriage":
    #     payload = {'groom_id': record.person1, 'bride_id': record.person2}
    #     r.request.post("http://localhost/api/v1/marriages/", )

    if record['recordType'] == 'marriage':
        payload = { 
            'dateOfWedding': record['dateOfWedding'], 
            'bride_id': record['bride_id'], 
            'groom_id': record['groom_id'] 
            }
        r = requests.patch("http://172.30.5.3/api/v1/marriages/", json=payload)
    


channel.basic_consume(on_marriage_added,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
