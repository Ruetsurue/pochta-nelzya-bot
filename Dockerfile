FROM python:3.10-alpine
ENV TZ="Asia/Yerevan"
WORKDIR /pochta_nelzya_bot
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["python", "run.py"]