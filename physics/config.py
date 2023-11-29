import pygame

# スクリーン
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_COLOR = (40, 40, 40)

# 枠
GROUND_HEIGHT = 10
GROUND_COLOR = (0, 150, 20)  # 緑

# メニューバー
MENU_BAR_HEIGHT = 40
MENU_BAR_COLOR = (200, 200, 200)

button_color = (170, 170, 170)

# ボール関連
gravity_acceleration = pygame.math.Vector2(0, 0.15)  # 重力加速度

balls_number = 25  # 個数

repulsion_coefficient = 0.98  # 反発係数
