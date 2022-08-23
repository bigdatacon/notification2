import smtplib

class GetPullConnection:
    def __init__(
        self,
        smtpStr: str,

        smtpPort: int
    ):
        """
        Функция инициализации экземпляра класса.
        Args:
            topics_names: Имена топиков.
            host: Хост kafka.
            port: Порт kafka.
            sleeping_time: Частота занесения данных.
            max_comment_len: Максимальная длина комментария.
        """
        self.smtpStr = smtpStr
        self.smtpPort = smtpPort

    def connect(self):
        """
        Функция подключения к Kafka.
        Returns:
            KafkaProducer: подключение
        """
        return smtplib.SMTP(self.smtpStr, self.smtpPort)

    def smtp_serv_custom(self) ->smtplib.SMTP:
        smtp_serv = self.connect()
        smtp_serv.ehlo_or_helo_if_needed()
        smtp_serv.starttls()
        smtp_serv.ehlo()
        return smtp_serv


def sendmail(recepient: str,  msg: str, smtp_serv: GetPullConnection):
    sender = 'yandextest@bk.ru'
    password = 'mnVyhzAgRwGM5GBnf8CD'
    # smtpStr = 'smtp.mail.ru'
    # smtpPort = 587
    # smtp_serv = smtplib.SMTP(smtpStr, smtpPort)

    # smtp_serv.ehlo_or_helo_if_needed()
    # smtp_serv.starttls()
    # smtp_serv.ehlo()

    smtp_serv.login(sender, password)
    try:
        smtp_serv.sendmail(sender, recepient, msg)
    except smtplib.SMTPException:
        print('cannot send email')

    smtp_serv.quit()

if __name__ == '__main__':
    # recepient = 'yandextest@bk.ru'
    recepient = 'link17892020@gmail.com'
    name_user = 'Johnson'
    msg = f'your recomendation + {name_user}'
    # msg = 'your recomendation'
    smtpStr = 'smtp.mail.ru'
    smtpPort = 587
    smtp_serv = GetPullConnection(smtpStr, smtpPort).smtp_serv_custom()
    print(f' smtp_serv: {smtp_serv}, type : {type(smtp_serv)}')
    sendmail(recepient,  msg, smtp_serv)
    print('ALL DONE')