from typing import cast

from google.cloud import videointelligence_v1 as vi

import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'D:/VSCode/GitRepos/PythonHacks/GCP_Video_Intelligence_API/cloudquicklabs-8d3bc835ed23.json'



def detect_shot_changes(video_uri: str) -> vi.VideoAnnotationResults:
    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.SHOT_CHANGE_DETECTION]
    request = vi.AnnotateVideoRequest(input_uri=video_uri, features=features)

    print(f'Processing video: "{video_uri}"...')
    operation = video_client.annotate_video(request)

    # Wait for operation to complete
    response = cast(vi.AnnotateVideoResponse, operation.result())
    # A single video is processed
    results = response.annotation_results[0]

    return results
video_uri = "gs://cloud-samples-data/video/JaneGoodall.mp4"

results = detect_shot_changes(video_uri)

def print_video_shots(results: vi.VideoAnnotationResults):
    shots = results.shot_annotations
    print(f" Video shots: {len(shots)} ".center(40, "-"))
    for i, shot in enumerate(shots):
        t1 = shot.start_time_offset.total_seconds()
        t2 = shot.end_time_offset.total_seconds()
        print(f"{i+1:>3} | {t1:7.3f} | {t2:7.3f}")

print_video_shots(results)