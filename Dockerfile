FROM python:3.7
COPY ./requirements.txt /dockerBuild/requirements.txt
WORKDIR /dockerBuild
RUN pip install --no-cache-dir -r requirements.txt
COPY . /dockerBuild
ENV DB_TYPE=postgresql
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=postgres
ENV DB_ENDPOINT=postgres:5432
ENV DB_TEST_ENDPOINT=test_postgres:5432 
ENV DB_TEST_NAME=bit_schema_test
ENV DB_NAME=bit_schema
ENV FLASK_APP=run.py
CMD ["flask", "run", "--host", "0.0.0.0"]
