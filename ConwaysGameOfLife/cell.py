class LivingCell:
    def __init__(self, position: tuple[int, int], size: int = 5) -> None:
        self.position = position
        self.x, self.y = self.position
        self.color = (243, 156, 18)
        self.size = size
