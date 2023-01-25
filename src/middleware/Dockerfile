FROM python:3.9-alpine

COPY . /middleware
WORKDIR /middleware

RUN pip3 install -r requirements.txt

COPY . .
ENV PORT 5000
EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]