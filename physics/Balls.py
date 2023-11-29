import pygame, math
import config


# ボールの設定
balls = []  # 全ボールを格納

# ボールの生成を定義
def create_ball(position, velocity, radius, mass, color, top_ground, bottom_ground, left_ground, right_ground):
    ball = Ball(position, velocity, radius, mass, color, top_ground, bottom_ground, left_ground, right_ground)
    balls.append(ball)

# ボールの除去を定義
def remove_ball(ball):
    balls.remove(ball)

class Ball:
    # ボールの属性を定義
    def __init__(self, position, velocity, radius, mass, color, top_ground, bottom_ground, left_ground, right_ground):
        self.position = position  # 位置ベクトル
        self.velocity = velocity  # 速度ベクトル
        self.radius = radius  # 半径
        self.mass = mass  # 質量
        self.color = color  # 色

        # Ballsモジュール内でmainの枠の情報を使えるようにする
        self.top_ground = top_ground
        self.bottom_ground = bottom_ground
        self.left_ground = left_ground
        self.right_ground = right_ground

    # ボールの描画を定義
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    # ボールの位置更新を定義
    def update(self):
        self.position += self.velocity
        self.velocity += config.gravity_acceleration

    def ball_collision(self, other_ball):
        # 2つのボールの距離
        distance = math.sqrt((self.position.x - other_ball.position.x) ** 2 + (self.position.y - other_ball.position.y) ** 2)
        depth = self.radius + other_ball.radius - distance
        
        # 衝突した場合
        if depth > 0:
            # 衝突軸
            normal_vector = pygame.math.Vector2(other_ball.position - self.position).normalize()
            # 重なりの解消
            self.position -= depth / 2 * normal_vector
            other_ball.position += depth / 2 * normal_vector

            # 衝突軸方向の速度
            projection1 = self.velocity.dot(normal_vector)  # 単位ベクトルとのドット積
            projection2 = other_ball.velocity.dot(normal_vector)
            # 反射
            self.velocity = (other_ball.mass / (self.mass + other_ball.mass)) * (1 + config.repulsion_coefficient) * (projection2 - projection1) * normal_vector + self.velocity
            other_ball.velocity = (self.mass / (self.mass + other_ball.mass)) * (1 + config.repulsion_coefficient) * (projection1 - projection2) * normal_vector + other_ball.velocity


    def flame_collision(self):
        # 枠に対する速度を絶対値で変換し、速度ベクトルをウィンドウ内に向ける
        # 上枠
        if self.position.y - self.radius <= self.top_ground.bottom:
            self.velocity.y = config.repulsion_coefficient * abs(self.velocity.y)

        # 下枠
        if self.position.y + self.radius >= self.bottom_ground.top:
            self.velocity.y = - config.repulsion_coefficient * abs(self.velocity.y)

        # 左枠
        if self.position.x - self.radius <= self.left_ground.right:
            self.velocity.x = config.repulsion_coefficient * abs(self.velocity.x)

        # 右枠
        if self.position.x + self.radius >= self.right_ground.left:
            self.velocity.x = - config.repulsion_coefficient * abs(self.velocity.x)
