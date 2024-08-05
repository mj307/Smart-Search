FROM python:3.11.4

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["uvicorn","main:app","--host","0.0.0.0"]
