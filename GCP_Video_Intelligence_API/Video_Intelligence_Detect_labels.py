from datetime import timedelta
from typing import Optional, Sequence, cast

from google.cloud import videointelligence_v1 as vi

import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'D:/VSCode/GitRepos/PythonHacks/GCP_Video_Intelligence_API/cloudquicklabs-8d3bc835ed23.json'

def detect_labels( video_uri: str,mode: vi.LabelDetectionMode,segments: Optional[Sequence[vi.VideoSegment]] = None,) -> vi.VideoAnnotationResults:
    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.LABEL_DETECTION]
    config = vi.LabelDetectionConfig(label_detection_mode=mode)
    context = vi.VideoContext(segments=segments, label_detection_config=config)
    request = vi.AnnotateVideoRequest(
        input_uri=video_uri,
        features=features,
        video_context=context,
    )

    print(f'Processing video "{video_uri}"...')
    operation = video_client.annotate_video(request)

    # Wait for operation to complete
    response = cast(vi.AnnotateVideoResponse, operation.result())
    # A single video is processed
    results = response.annotation_results[0]

    return results

video_uri = "gs://test_demo_storage_bucket/JaneGoodall.mp4"
mode = vi.LabelDetectionMode.SHOT_MODE
segment = vi.VideoSegment(
    start_time_offset=timedelta(seconds=0),
    end_time_offset=timedelta(seconds=37),
)

results = detect_labels(video_uri, mode, [segment])

def print_video_labels(results: vi.VideoAnnotationResults):
    labels = sorted_by_first_segment_confidence(results.segment_label_annotations)

    print(f" Video labels: {len(labels)} ".center(80, "-"))
    for label in labels:
        categories = category_entities_to_str(label.category_entities)
        for segment in label.segments:
            confidence = segment.confidence
            t1 = segment.segment.start_time_offset.total_seconds()
            t2 = segment.segment.end_time_offset.total_seconds()
            print(
                f"{confidence:4.0%}",
                f"{t1:7.3f}",
                f"{t2:7.3f}",
                f"{label.entity.description}{categories}",
                sep=" | ",
            )


def sorted_by_first_segment_confidence(
    labels: Sequence[vi.LabelAnnotation],
) -> Sequence[vi.LabelAnnotation]:
    def first_segment_confidence(label: vi.LabelAnnotation) -> float:
        return label.segments[0].confidence

    return sorted(labels, key=first_segment_confidence, reverse=True)


def category_entities_to_str(category_entities: Sequence[vi.Entity]) -> str:
    if not category_entities:
        return ""
    entities = ", ".join([e.description for e in category_entities])
    return f" ({entities})"

print_video_labels(results)

def print_shot_labels(results: vi.VideoAnnotationResults):
    labels = sorted_by_first_segment_start_and_confidence(
        results.shot_label_annotations
    )

    print(f" Shot labels: {len(labels)} ".center(80, "-"))
    for label in labels:
        categories = category_entities_to_str(label.category_entities)
        print(f"{label.entity.description}{categories}")
        for segment in label.segments:
            confidence = segment.confidence
            t1 = segment.segment.start_time_offset.total_seconds()
            t2 = segment.segment.end_time_offset.total_seconds()
            print(f"{confidence:4.0%} | {t1:7.3f} | {t2:7.3f}")


def sorted_by_first_segment_start_and_confidence(
    labels: Sequence[vi.LabelAnnotation],
) -> Sequence[vi.LabelAnnotation]:
    def first_segment_start_and_confidence(label: vi.LabelAnnotation):
        first_segment = label.segments[0]
        ms = first_segment.segment.start_time_offset.total_seconds()
        return (ms, -first_segment.confidence)

    return sorted(labels, key=first_segment_start_and_confidence)

print_shot_labels(results)