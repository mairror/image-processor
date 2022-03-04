import pickle
from typing import Dict, List

import cv2
import face_recognition
import numpy as np
from aws_utils.s3 import get_object


def face_detection(s3_object: Dict, s3_client) -> List:
    """
    Name: face_detection
    Description:
        Function to get the numpy array detected in a image.
    Inputs:
        :s3_object: type(dict) -> dictionary with the s3 object key, bucket and checksum.
        :s3_client: -> Client to connect to s3.
    Outputs:
        List(faces) -> list of faces on numpy array saved as type(bytes).
    """
    image = get_object(s3_object, s3_client)

    image_np = cv2.imdecode(np.asarray(bytearray(image)), cv2.IMREAD_UNCHANGED)

    face_locations = face_recognition.face_locations(image_np)

    faces = []
    for count, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        face_image = image_np[top:bottom, left:right]
        pck = pickle.dumps(face_image, protocol=5)
        faces.append(("files", (f"face_{count+1}", pck)))

    return faces
