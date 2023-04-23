FROM python:3.11
WORKDIR /app
COPT requirements.txt requirements.txt
RUN pip3 install --updrade setuptools
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .

