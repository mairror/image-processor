import json
from typing import Dict, Union

from config.settings import NUM_MESSAGES, QUEUE_NAME, WAIT_TIME_SECONDS


def get_queue_url(sqs_client) -> str:
    """
    Name: get_queue_url
    Description:
        Function to get the url to connect to sqs.
    Inputs:
        :sqs_client: -> Client to connect to sqs.
    Outputs:
        type(str) -> Return the sqs url.
    """
    response = sqs_client.get_queue_url(
        QueueName=QUEUE_NAME,
    )
    return response["QueueUrl"]


def receive_message(sqs_client, queue_url: str) -> Union[Dict, str, str]:
    """
    Name: receive_message
    Description:
        Function to get events from sqs.
    Inputs:
        :queue_url: type(str) -> SQS Url.
        :sqs_client: -> Client to connect to sqs.
    Outputs:
        type(dict) -> Return three values: a dict with key, bucket name and checksum of the image,
        the receipt handle and the messageid.
    """
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=NUM_MESSAGES,
        WaitTimeSeconds=WAIT_TIME_SECONDS,
    )

    for message in response["Messages"]:

        message_body = json.loads(message["Body"])
        if message_body["Records"][0]["eventName"] == "ObjectCreated:Put":
            return (
                {
                    "key": message_body["Records"][0]["s3"]["object"]["key"],
                    "bucket_name": message_body["Records"][0]["s3"]["bucket"]["name"],
                    "checksum": message_body["Records"][0]["s3"]["object"]["eTag"],
                },
                message["ReceiptHandle"],
                message["MessageId"],
            )


def delete_message(sqs_client, queue_url: str, receipt_handle: str) -> int:
    """
    Name: delete_message
    Description:
        Function to delete events from sqs.
    Inputs:
        :receipt_handle: type(str) -> Required. Used to remove the event from the queue.
        :queue_url: type(str) -> SQS Url.
        :sqs_client: -> Client to connect to sqs.
    Outputs:
        type(int) -> Return the http code of the delete operation.
    """
    response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]
