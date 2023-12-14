import sys
import pygame, random
from pygame.locals import *
from balls import create_ball, remove_ball, balls
from menu import create_menu_bar
import config


def main():
    # pygameの初期化
    pygame.init()

    # 初期化エラー判定
    if not pygame.get_init():
        print("Pygameの初期化に失敗しました。")
        pygame.quit()
        sys.exit()

    # ウィンドウ作成エラー判定
    try:
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    except pygame.error as e:
        print("ウィンドウの作成に失敗しました:", e)
        pygame.quit()
        sys.exit()

    # メイン画面のタイトル
    pygame.display.set_caption("2D Physics Engine")

    font = pygame.font.Font(None, 36)

    # 外枠の設定

    # 上枠
    top_ground = pygame.Rect(0, 0, config.SCREEN_WIDTH, config.GROUND_HEIGHT)

    # 下枠
    bottom_ground = pygame.Rect(0, config.SCREEN_HEIGHT - config.GROUND_HEIGHT - config.MENU_BAR_HEIGHT, config.SCREEN_WIDTH, config.GROUND_HEIGHT)

    # 左枠
    left_ground = pygame.Rect(0, 0, config.GROUND_HEIGHT, config.SCREEN_HEIGHT - config.MENU_BAR_HEIGHT)

    # 右枠
    right_ground = pygame.Rect(config.SCREEN_WIDTH - config.GROUND_HEIGHT, 0, config.GROUND_HEIGHT, config.SCREEN_HEIGHT - config.MENU_BAR_HEIGHT)

    # メニューバーを作成
    menu_bar = create_menu_bar(screen, font, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.MENU_BAR_HEIGHT, config.MENU_BAR_COLOR, config.button_color, config.gravity_acceleration)

    # ボールを生成
    for i in range(config.balls_number):
        # ボールの属性を決定
        position = pygame.math.Vector2(random.randint(50, config.SCREEN_WIDTH - 50), random.randint(50, config.SCREEN_HEIGHT - 50))  # ボールの位置
        velocity = pygame.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))  # ボールの速度
        mass = random.randint(1, 8)  # ボールの質量
        radius = 7 + 3 * mass  # ボールの半径(質量に依存)
        color = (15 + 30 * mass, 203, 255)  # ボールの色(軽い→青, 重い→赤)

        create_ball(position, velocity, radius, mass, color, top_ground, bottom_ground, left_ground, right_ground)

    # ループ
    clock = pygame.time.Clock()
    running = True
    paused = False

    selected_ball = None

    # 終了イベント発生までループをまわす
    while running:
        for event in pygame.event.get():
            # 終了イベント
            if event.type == pygame.QUIT:
                running = False

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # メニューバーのイベント処理
            menu_bar.handle_events(event)

            if event.type == pygame.KEYDOWN:
                # kキーで時間の一時停止を切り替え
                if event.key == K_t:
                    paused = not paused

                # スペースキーでボールを新たに生成
                elif event.key == K_SPACE:
                    # 新しいボールの属性を決定
                    position = pygame.math.Vector2(mouse_x, mouse_y)  # ボールの位置(カーソルの位置)
                    velocity = pygame.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))  # 新しいボールの速度
                    mass = random.randint(1, 8)  # 新しいボールの質量
                    radius = (7 + 3 * mass)  # 新しいボールの半径(質量に依存)
                    color = (15 + 30 * mass, 203, 255)  # 新しいボールの色(軽い→青, 重い→赤)

                    create_ball(position, velocity, radius, mass, color, top_ground, bottom_ground, left_ground, right_ground)

            # 左クリックでボールを選択
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for ball in balls:
                        mouse_distance = (mouse_pos[0] - ball.position.x) ** 2 + (mouse_pos[1] - ball.position.y) ** 2
                        if mouse_distance <= ball.radius ** 2:  # 二乗の値同士で比較し計算量削減
                            selected_ball = ball

            # 左マウスボタンを離したら選択解除
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected_ball = None

            # 右クリックでボールを消去
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    mouse_pos = event.pos
                    for ball in balls:
                        mouse_distance = (mouse_pos[0] - ball.position.x) ** 2 + (mouse_pos[1] - ball.position.y) ** 2
                        if mouse_distance <= ball.radius ** 2:
                            remove_ball(ball)

        # 選択されたボールをマウスで移動
        if selected_ball is not None:
            selected_ball.velocity = pygame.math.Vector2((mouse_x - selected_ball.position.x) / 4, (mouse_y - selected_ball.position.y) / 4)
            selected_ball.position.x, selected_ball.position.y = mouse_x, mouse_y

        # 時間が停止していないときボールの処理を行う
        if not paused:
            for ball in balls:
                ball.update()  # ボールの位置更新
                ball.flame_collision()  # ボールと枠の衝突

            # ボールの組み合わせ{(ball)_C_2 = (ball)! / 2! * (ball - 2)!}
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    # ボール同士の衝突
                    balls[i].ball_collision(balls[j])

        # 画面をクリア
        screen.fill(config.SCREEN_COLOR)

        # ボールの描画
        for ball in balls:
            # ボール
            ball.draw(screen)

        # 外枠の描写
        pygame.draw.rect(screen, config.GROUND_COLOR, top_ground)
        pygame.draw.rect(screen, config.GROUND_COLOR, bottom_ground)
        pygame.draw.rect(screen, config.GROUND_COLOR, left_ground)
        pygame.draw.rect(screen, config.GROUND_COLOR, right_ground)

        # メニューバーの描画
        menu_bar.draw_menu_bar()

        # 画面をアップデート
        pygame.display.update()

        # フレームレート
        clock.tick(120)

    # 終了処理
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
