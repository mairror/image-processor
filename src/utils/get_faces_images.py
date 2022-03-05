import os
import pickle

import cv2
import numpy as np  # noqa: F401
from pymongo import MongoClient


def get_faces(s3_object_key) -> None:
    client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    face = client["mairror"]
    face_col = face["faces"]

    f = face_col.find_one({"key": s3_object_key})

    for count, image in enumerate(f["faces"]):
        ar = pickle.loads(image)
        face = cv2.cvtColor(ar, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(r"test_{}.jpg".format(count), face)
