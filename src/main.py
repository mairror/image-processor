import boto3
import json
from config.settings import QUEUE_NAME, NUM_MESSAGES, WAIT_TIME_SECONDS
from face_recognition.get_faces import face_recognition


def get_queue_url(sqs_client) -> str:
    response = sqs_client.get_queue_url(
        QueueName=QUEUE_NAME,
    )
    return response["QueueUrl"]


def receive_message(sqs_client, queue_url: str):
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=NUM_MESSAGES,
        WaitTimeSeconds=WAIT_TIME_SECONDS,
    )

    # print(response)
    # print(dir(response))


    for message in response["Messages"]:
        print(message.keys())
        print(message["Body"])
        
        message_body = json.loads(message["Body"])
        if message_body["Records"][0]["eventName"] == "ObjectCreated:Put":
            return {
              "key": message_body["Records"][0]["s3"]["object"]["key"],
              "bucket_name": f's3://{message_body["Records"][0]["s3"]["bucket"]["name"]}',
              "checksum": message_body["Records"][0]["s3"]["object"]["eTag"]
            }, message["ReceiptHandle"], message["MessageId"]


def delete_message(sqs_client, queue_url: str, receipt_handle: str):
    response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]





if __name__ == "__main__":
    sqs_client = boto3.client("sqs")
    queue_url = get_queue_url(sqs_client)
    while True:
        try:
            s3_object, receipt_handle, message_id = receive_message(sqs_client, queue_url)
            s3_deleted_object = delete_message(sqs_client, queue_url, receipt_handle)

            if s3_deleted_object == 200:
                print(f"Deleted from queue event {message_id}")
                faces_recognition(s3_object)
        except KeyError as key_error:
            print(f"KeyError: No key {key_error} found")
            continue
