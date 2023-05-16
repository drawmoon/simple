import os
import pygame

from pygame.locals import QUIT, KEYDOWN, KEYUP


# 获取图形
def get_img(surf: pygame.Surface, x, y, w, h, color, scale):
    # 创建一个指定宽度和高度的 Surface 对象
    img = pygame.Surface([w, h])

    img.blit(surf, (0, 0), (x, y, w, h))
    img.set_colorkey(color)

    rect = img.get_rect()
    img = pygame.transform.scale(img, (rect.width * scale, rect.height * scale))
    return img


def load_gfx(dir, color=(255, 0, 255), accept=(".png", ".jpg")):
    assets = {}
    for pic in os.listdir(dir):
        name, ext = os.path.splitext(pic)
        if str.lower(ext) in accept:
            img = pygame.image.load(os.path.join(dir, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(color)
            assets[name] = img
    return assets


class _Black(pygame.sprite.Sprite):
    def __init__(self, surf, img_rect_list, x, y, *groups) -> None:
        super().__init__(*groups)

        self.surf_list: list[pygame.Surface] = []
        for rect in img_rect_list:
            self.surf_list.append(get_img(surf, *rect, (0, 0, 0), 2.69))

        self.image = self.surf_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# 砖头
class _Brick(_Black):
    def __init__(self, rect_list, x, y, *groups):
        super().__init__(GFX["tileset"], rect_list, x, y, *groups)

    def update(self):
        pass


# 橙色的砖头
class OrangeBrick(_Brick):
    def __init__(self, x, y, *groups):
        super().__init__([(16, 0, 10, 10), (432, 0, 10, 10)], x, y, *groups)


# 绿色的砖头
class GreenBrick(_Brick):
    def __init__(self, x, y, *groups):
        super().__init__([(208, 32, 10, 10), (48, 32, 10, 10)], x, y, *groups)


# 地图
class Map:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.deno = False
        self.setup_bg()
        self.setup_brick()

    def setup_bg(self):
        self.bg = pygame.Surface([X, Y])
        self.bg.set_colorkey((0, 0, 0))

        rect = self.bg.get_rect()

        self.bg = pygame.transform.scale(
            self.bg, (rect.width * 2.679, rect.height * 2.679)
        )

        self.map = pygame.Surface((rect.width, rect.height)).convert()
        self.viewport = SCREEN.get_rect(bottom=rect.bottom)

    def setup_brick(self):
        self.brick_group = pygame.sprite.Group()

        map_data = [(220, 100, 0)]

        for data in map_data:
            x, y, t = data[0], data[1], data[2]
            self.brick_group.add(OrangeBrick(x, y, pygame.sprite.Group()))

    def draw(self):
        # 绘制背景
        self.map.blit(self.bg, self.viewport, self.viewport)
        # 绘制砖头
        self.brick_group.draw(self.map)
        # 绘制到屏幕
        SCREEN.blit(self.map, (0, 0), self.viewport)

    def update(self):
        self.draw()


# 初始化 pygame
pygame.init()

# 用于获取帧数
CLOCK = pygame.time.Clock()

# 用于设置屏幕的宽度和高度
X = 800
Y = 600

# 创建屏幕对象
SCREEN = pygame.display.set_mode([X, Y])

# 加载所有图形资源文件
GFX: dict[str, pygame.Surface] = load_gfx(os.path.join("assets"))

# 创建新的游戏对象
GAME = Map()

# 用于获取用户的键盘输入情况
PRESSED_KEYS = pygame.key.get_pressed()

while not GAME.deno:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            GAME.deno = True
        elif ev.type == KEYDOWN:
            PRESSED_KEYS = pygame.key.get_pressed()
        elif ev.type == KEYUP:
            PRESSED_KEYS = pygame.key.get_pressed()

    GAME.update()
    pygame.display.update()

    # 确保程序保持 30 的帧数
    CLOCK.tick(60)

pygame.quit()
