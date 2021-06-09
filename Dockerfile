FROM python:3-alpine3.9
WORKDIR /opt/flask-tech-test
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY techtest/models/ techtest/models/
COPY techtest/. techtest/.
COPY setup_and_seed.py .
RUN python setup_and_seed.py
COPY app.py .
EXPOSE 5000/tcp
CMD python app.py
