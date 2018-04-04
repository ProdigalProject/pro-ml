FROM python:3.6

WORKDIR /app 
RUN apt update &&\
    apt install -y ssh
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/ 

ENV SSH_PASSWD "root:Docker!" 

COPY sshd_config /etc/ssh/ 
COPY init.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/init.sh
EXPOSE 8000 2222

ENTRYPOINT ["init.sh"]
