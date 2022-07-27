class LivingCell:
    def __init__(self, position: tuple[int, int], size: int = 5) -> None:
        self.position = position
        self.x, self.y = self.position
        self.size = size
