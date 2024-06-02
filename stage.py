import random
import pygame

from enemy import Chaser, Shooter
from config import *


class Stage:
    def __init__(self, padding):
        self.padding = padding
        self.enemies = [
            Shooter(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            for _ in range(1)
        ]

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, self.padding))
        pygame.draw.rect(screen, BLACK, (0, 0, self.padding, SCREEN_HEIGHT))
        pygame.draw.rect(
            screen, BLACK, (0, SCREEN_HEIGHT - self.padding, SCREEN_WIDTH, self.padding)
        )
        pygame.draw.rect(
            screen, BLACK, (SCREEN_WIDTH - self.padding, 0, self.padding, SCREEN_HEIGHT)
        )

        for enemy in self.enemies:
            enemy.draw(screen)

    def update(self, player):
        for enemy in self.enemies:
            enemy.update(player.rect.center)
            if enemy.check_collision(player.rect):
                player.take_damage(1)
            for proj in player.projectiles:
                if enemy.check_collision(proj.rect):
                    enemy.take_damage(1)
                    proj.destroyed = True
            if enemy.x < self.padding or enemy.x > SCREEN_WIDTH - self.padding:
                enemy.direction.x *= -1
            if enemy.y < self.padding or enemy.y > SCREEN_HEIGHT - self.padding:
                enemy.direction.y *= -1
            if random.randint(0, 100) < 1:
                enemy.direction = pygame.Vector2(
                    random.randint(-1, 1), random.randint(-1, 1)
                )

        self.enemies = list(filter(lambda enemy: enemy.health > 0, self.enemies))