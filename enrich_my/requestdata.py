import requests
import time
from kafka_my.kafka_consumer import KafkaConsumerMy
from sending.sending_app import GetPullConnection, sendmail
from kafka_my.kafka_producer_ext_class import KafkaProducersender

"""Получаю данные из api"""
answer = requests.get("http://127.0.0.1:8000/user/", params={'db_name' : 'auth', 'user_id' : 'a61846cf-8882-4213-a471-f763000d1147'})
print(f' eto answer one user: {answer.json()}')
answer_many = requests.get("http://127.0.0.1:8000/get_all_users_info_from_table/", params={'db_name' : 'auth'})
print(f' eto answer all users : {answer_many.json()}')



"""пишу данные из того что прочитал в кафку"""
# for i in answer_many.json().get("user_info"):
for i in answer_many.json().get("user_info"):
    p = KafkaProducersender()
    topic_name = 'example_topic'
    id = i[0]
    first_name= i[1]
    last_name = i[2]
    p.send(topic_name, f'{id},{first_name},{last_name}')
    print(f'ALL SEND TO Kafka : {i}')

"""читаю данные из кафки и отправляю сообщения на почту """
consumer = KafkaConsumerMy('example_topic', 'localhost', '9092')
while True:
    consume_from_kafka =consumer.read()
    # print(f'consume_from_kafka " {consume_from_kafka}, {consume_from_kafka.decode("utf-8") }')
    id = list(consume_from_kafka.decode("utf-8").split(","))[0]
    first_name = list(consume_from_kafka.decode("utf-8").split(","))[1]
    last_name = list(consume_from_kafka.decode("utf-8").split(","))[2]
    print(f'"consume_from_kafka:", {id, first_name, last_name}')
    recepient = 'link17892020@gmail.com'
    msg = f'your grateful recomendation {id} + {first_name, last_name}'
    smtpStr = 'smtp.mail.ru'
    smtpPort = 587
    smtp_serv = GetPullConnection(smtpStr, smtpPort).smtp_serv_custom()
    sendmail(recepient,  msg, smtp_serv)
    print('ALL SEND TO EMAIL')
    time.sleep(50)


# """отправляю письма именные, все на свой ящик пока """
# for i in answer_many.json().get("user_info"):
#     first_name = i[1]
#     last_name = i[2]
#     recepient = 'link17892020@gmail.com'
#     msg = f'your recomendation + {first_name, last_name}'
#     smtpStr = 'smtp.mail.ru'
#     smtpPort = 587
#     smtp_serv = GetPullConnection(smtpStr, smtpPort).smtp_serv_custom()
#     sendmail(recepient,  msg, smtp_serv)
#     print('ALL SEND TO EMAIL')
