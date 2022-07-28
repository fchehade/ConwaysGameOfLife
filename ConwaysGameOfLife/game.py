import random
from collections import Counter
import pygame
import time


class GameManager:
    def __init__(
        self,
        starting_cells: int = 500,
        fps: int = 30,
        screen_width: int = 1000,
        screen_height: int = 1000,
    ) -> None:

        self.starting_cells = starting_cells
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.living_cells = self.generate_first_generation()

    def generate_first_generation(self) -> set[tuple[int, int]]:
        return {
            (random.randrange(200), random.randrange(200))
            for _ in range(self.starting_cells)
        }

    def calculate_neighboring_cells(self, cell: tuple[int, int]):
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
            yield cell[0] + dx, cell[1] + dy

    def generate_next_generation(
        self, cells: set[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        new_generation = Counter(
            (
                new_position
                for cell in cells
                for new_position in self.calculate_neighboring_cells(cell)
            )
        )
        return {
            tuple(cell_position)
            for cell_position, encounters in new_generation.items()
            if encounters == 3 or (encounters == 2 and cell_position in cells)
        }

    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        game_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        is_playing = True
        cycle = 0
        font = pygame.font.SysFont("Garamond", 30)
        while is_playing:
            start = time.time()
            self.living_cells = self.generate_next_generation(self.living_cells)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_playing = not is_playing

            game_screen.fill((0, 0, 0))

            for cell in self.living_cells:
                pygame.draw.rect(
                    game_screen,
                    (255, 0, 0),
                    (
                        (cell[0] * 5),
                        (cell[1] * 5),
                        5,
                        5,
                    ),
                )

            cycle += 1
            text = font.render(
                f"{len(self.living_cells)} living cells", True, (255, 255, 255)
            )
            textRect = text.get_rect()
            textRect.center = (self.screen_width / 2, 25)
            second_text = font.render(f"Generation: {cycle}", True, (255, 255, 255))
            second_textRect = text.get_rect()
            second_textRect.center = (self.screen_width / 5, 25)
            game_screen.blit(text, textRect)
            game_screen.blit(second_text, second_textRect)
            clock.tick(self.fps)
            pygame.display.flip()
            stop = time.time()
            print(f"Generation: {cycle} - {stop - start} seconds")

        pygame.quit()
