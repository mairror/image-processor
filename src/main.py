from http.client import HTTPException

import boto3
import requests
from aws_utils.sqs import (
    delete_message,
    get_queue_url,
    produce_message,
    receive_message,
)
from config.settings import (
    API_KEY,
    API_KEY_HEADER,
    API_PATH,
    API_URL,
    SQS_CROPPED_QUEUE_NAME,
    SQS_PREDICT_QUEUE_NAME,
)
from faces_recon.get_faces import face_detection
from utils.logging import image_processor


def main() -> None:
    """
    Name: main
    Description:
        Main principal function to run the event listener and send the faces images generated.
    Inputs:
        None
    Outputs:
        None
    """

    image_processor.debug("Start sqs and s3 clients")
    sqs_client = boto3.client("sqs")
    s3_client = boto3.client("s3")
    image_processor.debug("Get the cropped queue url")
    crop_queue_url = get_queue_url(sqs_client, SQS_CROPPED_QUEUE_NAME)
    image_processor.debug("Get the predict queue url")
    predict_queue_url = get_queue_url(sqs_client, SQS_PREDICT_QUEUE_NAME)

    image_processor.info("Start the sqs listener to get events")
    while True:
        try:
            s3_object, receipt_handle, message_id = receive_message(
                sqs_client, crop_queue_url
            )
            s3_deleted_object = delete_message(
                sqs_client, crop_queue_url, receipt_handle
            )

            if s3_deleted_object == 200:
                print(f"Deleted from queue event {message_id}")
                faces = face_detection(s3_object, s3_client)
                response = requests.post(
                    API_URL + API_PATH,
                    files=faces,
                    data={"key": s3_object["key"]},
                    headers={API_KEY_HEADER: API_KEY},
                )

                if response.status_code == 200:
                    print(f"{response.text}")

                    status_code, message_id = produce_message(
                        sqs_client, predict_queue_url, s3_object
                    )
                    if status_code == 200:
                        print(f"Produced to queue event {message_id}")
                else:
                    raise HTTPException(
                        {"status_code": response.status_code, "detail": response.text}
                    )
        except KeyError as key_error:
            print(f"KeyError: No key {key_error} found")
            continue
        except HTTPException as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
