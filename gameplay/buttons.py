class Button:
    def __init__(self, pos_x: int, pos_y: int, size_x: int, size_y: int, func):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.function = func

    @staticmethod
    def get_corners(pos_x: int, pos_y: int, size_x: int, size_y: int) -> tuple[tuple[int, int], tuple[int, int]]:
        bottom_left = (pos_x, pos_y)
        top_right = (pos_x + size_x, pos_y - size_y)
        return bottom_left, top_right

    def is_hover(self, mouse_x: int, mouse_y: int) -> bool:
        bottom_left, top_right = self.get_corners(self.pos_x, self.pos_y, self.size_x, self.size_y)
        return bottom_left[0] < mouse_x < top_right[0] and bottom_left[1] < mouse_y < top_right[1]
