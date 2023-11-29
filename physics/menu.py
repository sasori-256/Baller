import tkinter as tk
from tkinter.simpledialog import askfloat
import pygame, config

# メニューバー作成を定義
def create_menu_bar(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BAR_HEIGHT, MENU_BAR_COLOR, button_color, gravity_acceleration):
    return MenuBar(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BAR_HEIGHT, MENU_BAR_COLOR, button_color, gravity_acceleration)

class MenuBar:
    def __init__(self, screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BAR_HEIGHT, MENU_BAR_COLOR, button_color, gravity_acceleration):
        self.screen = screen
        self.font = font
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.MENU_BAR_HEIGHT = MENU_BAR_HEIGHT
        self.MENU_BAR_COLOR = MENU_BAR_COLOR
        self.button_color = button_color
        self.gravity_acceleration = gravity_acceleration

        # メニューバー
        self.rect = pygame.Rect(0, self.SCREEN_HEIGHT - self.MENU_BAR_HEIGHT, self.SCREEN_WIDTH, self.MENU_BAR_HEIGHT)

        # ボタン
        self.button_rect = pygame.Rect(20, self.SCREEN_HEIGHT - self.MENU_BAR_HEIGHT + 10, 200, 30)
        self.button_text = "Change Gravity"

    # メニューバー描画
    def draw_menu_bar(self):
        pygame.draw.rect(self.screen, self.MENU_BAR_COLOR, self.rect)
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        text = self.font.render(self.button_text, True, (255, 255, 255))
        self.screen.blit(text, (self.button_rect.centerx - text.get_width() / 2, self.button_rect.centery - text.get_height() / 2))

    def handle_events(self, event):
        # イベント処理
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_x, mouse_y):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.show_gravity_dialog()

    # 重力変更
    def show_gravity_dialog(self):
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示にする

        new_gravity_x = askfloat("Gravity Input", "Enter new gravity x:")
        new_gravity_y = askfloat("Gravity Input", "Enter new gravity y:")

        if new_gravity_x is not None and new_gravity_y is not None:
            config.gravity_acceleration = pygame.math.Vector2(new_gravity_x / 10, new_gravity_y / 10)
        else:
            print("Invalid input. Please enter a valid number for gravity.")
