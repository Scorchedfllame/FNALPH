import json


class System:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path


class Cameras(System):
    def __init__(self):
        super().__init__("Cameras", 'resources/background/test.png')
        self.camera_list = []

    @staticmethod
    def load_cameras(load_path: str):
        cameras = []
        with open(load_path, 'r') as f:
            cameras_list = json.load(f)
            for camera in cameras_list:
                cameras.append(Camera(camera[0], camera[1]))
            return cameras

    def activate_camera(self, camera_index: int):
        pass


class Camera:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.active = False


class Vents(System):
    def __init__(self):
        super().__init__("Vents", 'resources/background/test.png')


class Ducts(System):
    def __init__(self):
        super().__init__("Ducts", 'resources/background/test.png')


class Repairs(System):
    def __init__(self):
        super().__init__("Repairs", 'resources/background/test.png')
