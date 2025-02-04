from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceDetectionModel,
    FaceRecognitionModel,
    FaceAttributeTypeDetection03,
    FaceAttributeTypeRecognition04,
)

endpoint = "<>"
key = "<>"

with FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key)) as face_client:
    sample_file_path = "1.jpg"
    with open(sample_file_path, "rb") as fd:
        file_content = fd.read()

    result = face_client.detect(
        file_content,
        detection_model=FaceDetectionModel.DETECTION03,  # The latest detection model.
        recognition_model=FaceRecognitionModel.RECOGNITION04,  # The latest recognition model.
        return_face_id=True,
        return_face_attributes=[
            FaceAttributeTypeDetection03.HEAD_POSE,
            FaceAttributeTypeDetection03.MASK,
            FaceAttributeTypeRecognition04.QUALITY_FOR_RECOGNITION,
        ],
        return_face_landmarks=True,
        return_recognition_model=True,
        face_id_time_to_live=120,
    )

    print(f"Detect faces from the file: {sample_file_path}")
    for idx, face in enumerate(result):
        print(f"----- Detection result: #{idx+1} -----")
        print(f"Face: {face.as_dict()}")