from ultralytics import YOLO


def get_person_detection():
    """
    Предобученная модель детекции людей.
    """
    return YOLO('yolo_person.pt')
