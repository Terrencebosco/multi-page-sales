# creat python instance for docker image
FROM python:3.8-slim-buster

# install pip in image
RUN python -m pip install --upgrade pip

# create dir in imade
WORKDIR /app

#copy current dir data to image dir
COPY . /app

# install dependency to image
RUN pip3 install -r requirements.txt

# expose local port
EXPOSE 5000

# run flask app
ENTRYPOINT ["python"]

CMD ["index.py"]