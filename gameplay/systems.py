import json


class System:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path


class Camera:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.active = False


class Cameras(System):
    def __init__(self):
        super().__init__("Cameras", 'resources/background/test.png')
        self.camera_list = Cameras.load_cameras('Appdata/GameData/cameras.json')
        self.enabled = True
        self.active = False

    @staticmethod
    def load_cameras(load_path: str) -> list[Camera]:
        cameras = []
        with open(load_path, 'r') as f:
            cameras_list = json.load(f)
            for camera in cameras_list:
                cameras.append(Camera(camera[0], camera[1]))
            return cameras

    def disable_cameras(self):
        for camera in self.camera_list:
            camera.active = False

    def activate_camera(self, camera_index: int):
        self.disable_cameras()
        self.camera_list[camera_index].active = True


class Vents(System):
    def __init__(self):
        super().__init__("Vents", 'resources/background/test.png')


class Repairs(System):
    def __init__(self):
        super().__init__("Repairs", 'resources/background/test.png')
