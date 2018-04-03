FROM centos/python-36-centos7
USER root
WORKDIR /app 
ADD . /app 

RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
