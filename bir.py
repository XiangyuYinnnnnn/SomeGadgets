import pygame
import random
import math
import win32gui
import win32con
import win32api

# 初始化 Pygame
pygame.init()

# 获取屏幕分辨率
screen_info = pygame.display.Info()
screen_width = win32api.GetSystemMetrics(0) * 2  # 扩大到屏幕宽度的两倍
screen_height = win32api.GetSystemMetrics(1) * 2  # 扩大到屏幕高度的两倍
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("生日快乐！")

# 获取窗口句柄
hwnd = pygame.display.get_wm_info()["window"]
# 设置窗口为分层窗口
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# 设置透明颜色（这里以黑色为例）
win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)
# 设置窗口始终置顶
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# 定义更多颜色
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
          (255, 165, 0), (128, 0, 128), (0, 128, 0), (0, 255, 127)]

# 烟花粒子类
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(1, 5)  # 随机粒子大小
        # 随机生成角度和速度
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.gravity = random.uniform(0.05, 0.15)  # 随机重力影响
        self.lifetime = random.randint(20, 60)
        self.rotation = random.uniform(0, 360)  # 随机初始旋转角度
        self.rotation_speed = random.uniform(-2, 2)  # 随机旋转速度

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.rotation += self.rotation_speed  # 更新旋转角度
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# 烟花类
class Firework:
    def __init__(self, x=None, y=None):
        if x is None:
            self.x = random.randint(0, screen_width)
            self.y = screen_height
        else:
            self.x = x
            self.y = y
        self.color = random.choice(COLORS)
        self.speed = random.randint(5, 10)
        self.exploded = False
        self.particles = []
        if y is not None:
            self.explode()

    def update(self):
        if not self.exploded:
            self.y -= self.speed
            # 让烟花爆炸高度更高且随机
            min_height = screen_height // 8
            max_height = screen_height // 2
            if self.y <= random.randint(min_height, max_height):
                self.explode()
        else:
            for particle in self.particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)
            if len(self.particles) == 0:
                return True
        return False

    def explode(self):
        self.exploded = True
        num_particles = random.randint(80, 150)  # 增加粒子数量
        for _ in range(num_particles):
            self.particles.append(Particle(self.x, self.y, self.color))

        # 多层烟花效果
        if random.random() < 0.2:  # 20% 的概率产生多层烟花
            inner_firework = Firework(self.x, self.y)
            inner_firework.explode()
            self.particles.extend(inner_firework.particles)

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
        else:
            for particle in self.particles:
                particle.draw(screen)

# 主循环
clock = pygame.time.Clock()
fireworks = []

# 使用绝对路径指定字体（以 Windows 系统黑体为例，你可根据实际修改）
font_path = "C:/Windows/Fonts/simhei.ttf"
font = pygame.font.Font(font_path, 74)

# 将文字颜色改为黄色
text = font.render("生日快乐！", True, (255, 255, 0))
text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 提高随机生成烟花的概率
    if random.random() < 0.05:
        fireworks.append(Firework())

    screen.fill((0, 0, 0))  # 填充黑色背景，黑色将被设置为透明色
    screen.blit(text, text_rect)

    for firework in fireworks[:]:
        if firework.update():
            fireworks.remove(firework)
        firework.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# 退出 Pygame
pygame.quit()
    