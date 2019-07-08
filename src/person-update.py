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
                    routing_key='personal')

print(' [*] Waiting for logs. To exit press CTRL+C')



def on_person_updated(ch, method, properties, body):
    # call rest person service and submit the update
    # body is json object with values
    # recordType: birth, death
    # recordDate: yyyy-MM-dd
    # person1: id
    # father: id - optional
    # mother: id - optional
    print(' [*] Processing message...')
    print(' [-] Received body:', body)
    record = json.loads(body)
    print('on_person_updated - parsed body...')
    print(body)
    # if record.recordType == "marriage":
    #     payload = {'groom_id': record.person1, 'bride_id': record.person2}
    #     r.request.post("http://localhost/api/v1/marriages/", )

    if record['recordType'] == 'birth':
        payload = { 'dateOfBirth': record['dateOfRecord'] }

        if 'father' in record or 'mother' in record:
            parents = []
            if 'father' in record:
                parents = parents + [{'id': record['father']}] 
            if 'mother' in record:
                parents = parents + [{'id': record['mother']}]
            payload['parents'] = parents
    elif record['recordType'] == 'death':
        payload = { 'dateOfDeath': record['dateOfRecord'] }
    else:
        return

    r = requests.patch("http://172.30.5.3/api/v1/persons/" + str(record['personId']), json=payload)


# def on_person_updated(ch, method, properties, body):
#     print(' [*] Processing message...')
#     print(' [-] Received body:', body)


channel.basic_consume(on_person_updated,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()









