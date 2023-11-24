import pygame
import os

from theme import Theme

class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)

    def set_theme(self, theme):
        self.idx = theme % len(self.themes)
        self.theme = self.themes[self.idx]

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes) # [t1, t2, t3, t4]
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#64D264', '#46C846')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#64D264', '#46C846')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#64D264', '#46C846')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#64D264', '#46C846')

        self.themes = [green, brown, blue, gray]
