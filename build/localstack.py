import time
from json import loads

import boto3
import requests

ENDPOINT_URL = "http://localhost:4566"
REGION_NAME = "eu-central-1"


def client(service: str):
    return boto3.client(service, endpoint_url=ENDPOINT_URL, region_name=REGION_NAME)


def wait_docker_run():
    while True:
        try:
            r = requests.get(F"{ENDPOINT_URL}/health")
            if r.ok:
                localstack_response = loads(r.content)
                if all(status in ("available", "running")
                       for status in localstack_response["services"].values()):
                    break
        except Exception:
            ...
        time.sleep(1.5)


print("LocalStack: Setting up the infrastructure")
wait_docker_run()
print("LocalStack: All services are available")

print("LocalStack: Creating the S3 bucket")
s3 = client("s3")
s3.create_bucket(Bucket="s3-workshop-unit-testing",
                 CreateBucketConfiguration={'LocationConstraint': REGION_NAME})
print("LocalStack: S3 bucket created")

print("LocalStack: Setup done, let's rock")
