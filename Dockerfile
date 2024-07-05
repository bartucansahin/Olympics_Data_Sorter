FROM python:3.8-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /code/wait-for-it.sh

CMD ["./wait-for-it.sh", "db:3306", "--", "flask", "run", "--host=0.0.0.0"]