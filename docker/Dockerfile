FROM python:3.8

#COPY requirements.txt /opt/app/requirements.txt
#COPY lambda_function.py /opt/app/lambda_function.py

COPY . /opt/app/

RUN pip install --no-cache-dir -r /opt/app/requirements.txt

CMD [ "python3.8", "/opt/app/lambda_function.py" ]
