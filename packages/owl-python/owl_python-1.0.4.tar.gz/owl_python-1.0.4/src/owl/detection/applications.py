from ultralytics import YOLO
import urllib.request


def get_person_detection():
    """
    Предобученная модель детекции людей.
    """
    urllib.request.urlretrieve("https://huggingface.co/lazylearn/yolo_person_detection/resolve/main/yolo_person.pt", "yolo_person.pt")
    return YOLO('yolo_person.pt')
