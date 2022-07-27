from base64 import encode
import random
import pygame
from collections import Counter
from .cell import LivingCell


class GameManager:
    def __init__(
        self,
        starting_cells: int = 500,
        screen_width: int = 1000,
        screen_height: int = 1000,
    ) -> None:

        self.starting_cells = starting_cells
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.living_cells = self.generate_first_generation()

    def generate_first_generation(self) -> set[LivingCell]:
        return {
            LivingCell((random.randrange(200), random.randrange(200)))
            for _ in range(self.starting_cells)
        }

    def calculate_neighboring_cells(self, cell: LivingCell):
        for dx, dy in [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]:
            yield cell.position[0] + dx, cell.position[1] + dy

    def generate_next_generation(self, cells: set[LivingCell]) -> set[LivingCell]:
        all_positions = [cell.position for cell in cells]
        new_generation = Counter(
            [
                new_position
                for cell in cells
                for new_position in self.calculate_neighboring_cells(cell)
            ]
        )
        return {
            LivingCell(cell_position)
            for cell_position, encounters in new_generation.items()
            if encounters == 3 or (encounters == 2 and cell_position in all_positions)
        }

    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        game_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        is_playing = True
        while is_playing:
            self.living_cells = self.generate_next_generation(self.living_cells)
            clock.tick(144)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_playing = not is_playing

            game_screen.fill((0, 0, 0))
            for cell in self.living_cells:
                pygame.draw.rect(
                    game_screen,
                    (255, 0, 0),
                    (
                        (cell.position[0] * 5),
                        (cell.position[1] * 5),
                        cell.size,
                        cell.size,
                    ),
                )
            print(len(self.living_cells))
            pygame.display.flip()

        pygame.quit()
