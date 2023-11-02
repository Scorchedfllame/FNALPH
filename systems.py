class System:
    def __init__(self, name: str):
        self.name = name


class Cameras(System):
    def __init__(self, name: str):
        super().__init__(name)


class Camera:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path


class Vents(System):
    def __init__(self, name: str):
        super().__init__(name)


class Ducts(System):
    def __init__(self, name: str):
        super().__init__(name)


class Repairs(System):
    def __init__(self, name: str):
        super().__init__(name)
