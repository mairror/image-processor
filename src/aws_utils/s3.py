from typing import Dict


def get_object(s3_object: Dict, s3_client) -> bytes:
    """
    Name: get_object
    Description:
        Function to get the image and returned as bytes.
    Inputs:
        :s3_object: type(dict) -> dictionary with the s3 object key, bucket and checksum.
        :s3_client: -> Client to connect to s3.
    Outputs:
        type(bytes) -> Return the object content as bytes.
    """
    s3_response_object = s3_client.get_object(
        Bucket=s3_object["bucket_name"], Key=s3_object["key"]
    )
    object_content = s3_response_object["Body"].read()

    return object_content
