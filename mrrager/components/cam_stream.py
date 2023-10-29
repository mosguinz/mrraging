import reflex as rx


class CameraStream(rx.Component):
    """Camera"""

    library = "react-webcam"
    tag = "Webcam"
    is_default = True


camera = CameraStream.create


def cam_stream():
    return rx.center(camera())
