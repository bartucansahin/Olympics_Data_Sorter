import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import json

load_dotenv()

def get_secret():
    secret_name = "olympics_db_credentials"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

secret = get_secret()

user = secret.get('DB_USER')
password = secret.get('DB_PASSWORD')
host = secret.get('DB_HOST')
db_name = secret.get('DB_NAME')
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
