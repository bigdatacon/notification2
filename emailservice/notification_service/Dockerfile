FROM python:3.9-slim

ADD requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install --upgrade pip --no-cache && pip install -r requirements.txt --no-cache
ADD src .

RUN useradd -ms /bin/bash web && chown -R web /var/log && chown -R web /var/tmp && chown -R web /opt/app
USER web

RUN chmod 777 ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
