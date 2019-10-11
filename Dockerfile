FROM python:3.7
 ENV PYTHONUNBUFFERED 1

ADD requirements.txt /requirements.txt
# ADD requirements_server.txt /requirements_server.txt
RUN pip3 install --default-timeout=100 -i https://pypi.douban.com/simple -r requirements.txt

ADD . /sparrow_cloud
WORKDIR /sparrow_cloud

EXPOSE 8001
