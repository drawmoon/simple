import os
from abc import abstractmethod
from enum import Enum

import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, QUIT


# 获取图形
def load_img(surf: pygame.Surface, x, y, w, h, color, scale):
    # 创建一个指定宽度和高度的 Surface 对象
    img = pygame.Surface([w, h])

    img.blit(surf, (0, 0), (x, y, w, h))
    img.set_colorkey(color)

    # 修改图片的尺寸
    if scale != 1:
        rect = img.get_rect()
        img = pygame.transform.scale(img, (rect.width * scale, rect.height * scale))
    return img


def load_gfx(dir, color=(255, 0, 255), accept=(".png", ".jpg")):
    gfx_dict = {}
    for pic in os.listdir(dir):
        name, ext = os.path.splitext(pic)
        if str.lower(ext) in accept:
            img = pygame.image.load(os.path.join(dir, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(color)
            gfx_dict[name] = img
    return gfx_dict


class _Game:
    def __init__(self):
        self.deno = False
        self.sprites = pygame.sprite.Group()
        self.new_game()

    @abstractmethod
    def new_game():
        """抽象方法

        初始化新的游戏对象

        """

    @abstractmethod
    def draw(self):
        """抽象方法

        将游戏绘制到屏幕上

        """

    def update(self):
        """抽象方法

        更新当前游戏状态

        """
        # 更新全部 Sprite 的状态
        self.sprites.update()


class _Black(pygame.sprite.Sprite):
    def __init__(self, gfx, pos_rect_list, x, y, frame, scale, *groups):
        super().__init__(*groups)

        self.images: list[pygame.Surface] = []
        for rect in pos_rect_list:
            self.images.append(load_img(gfx, *rect, (0, 0, 0), scale))

        # 设置显示的图形
        self.frame = frame
        self.image = self.images[self.frame]
        # 设置显示的位置
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # 设置表示移动的参数
        self.ani = 3
        self.movex = 0
        self.movey = 0

    def control(self, x, y):
        """控制 Sprite 行动"""
        self.movex += x
        self.movey += y
        self.rect.move_ip(x, y)


# 爱心
class Heart(_Black):
    def __init__(self, x, y, *groups):
        super().__init__(
            GFX["heart"],
            [
                (0, 0, 22, 19),
                (22, 0, 21, 19),
                (43, 0, 17, 17),
                (60, 0, 19, 18),
                (79, 0, 12, 11),
            ],
            x,
            y,
            0,
            1,
            *groups
        )


# 角色
class _Character(_Black):
    class State(Enum):
        """角色状态"""

        STAND = 0  # 站立
        WALK = 1  # 行走
        WALK_AUTO = 2  # 自动行走
        JUMP = 3  # 跳跃
        FALL = 4  # 跌倒
        FLY = 5  # 飞
        FIRE = 6  # 开火
        SLEEP = 7  # 睡眠
        DIZZY = 8  # 眩晕
        DEAD = 9  # 死亡

    class Sight(Enum):
        """角色视线"""

        FACING_LEFT = 0  # 向左
        FACING_RIGHT = 1  # 向右
        FACING_FORWARD = 2  # 向前
        FACING_BACKWARD = 3  # 向后

    def __init__(self, gfx, gfx_rect_list, x, y, frame, scale, *groups):
        super().__init__(gfx, gfx_rect_list, x, y, frame, scale, *groups)

        # 设置角色状态
        self.state = _Character.State.STAND
        # 设置角色视线
        self.sight = _Character.Sight.FACING_FORWARD

    @abstractmethod
    def get_frame_scope(self):
        """虚拟方法

        获取一组图片的起始索引和结束索引
        """


# 玩家
class _Player(_Character):
    pass


# Wanda
class Wanda(_Player):
    def __init__(self, x, y, *groups):
        super().__init__(
            GFX["charsets"],
            [
                (0, 0, 12, 15),
                (13, 0, 10, 15),
                (24, 0, 10, 15),
                (35, 0, 10, 15),
                (46, 0, 10, 15),
                (57, 0, 10, 15),
                (68, 0, 12, 15),
                (81, 0, 10, 15),
                (92, 0, 10, 15),
                (103, 0, 10, 15),
                (114, 0, 10, 15),
                (125, 0, 10, 15),
            ],
            x,
            y,
            3,
            4.25,
            *groups
        )

    def get_frame_scope(self):
        if self.sight == _Character.Sight.FACING_FORWARD:
            return 0, 2
        if self.sight == _Character.Sight.FACING_RIGHT:
            return 3, 5
        if self.sight == _Character.Sight.FACING_BACKWARD:
            return 6, 8
        if self.sight == _Character.Sight.FACING_LEFT:
            return 9, 11

    def update(self):
        self.standing()

    def standing(self):
        if self.state == _Character.State.STAND:
            if PRESSED_KEYS[K_SPACE]:
                return

            if PRESSED_KEYS[K_UP]:
                self.sight = _Character.Sight.FACING_BACKWARD
                self.control(0, -2)
            elif PRESSED_KEYS[K_DOWN]:
                self.sight = _Character.Sight.FACING_FORWARD
                self.control(0, 2)
            elif PRESSED_KEYS[K_LEFT]:
                self.sight = _Character.Sight.FACING_LEFT
                self.control(-2, 0)
            elif PRESSED_KEYS[K_RIGHT]:
                self.sight = _Character.Sight.FACING_RIGHT
                self.control(2, 0)
            else:
                return

            s, e = self.get_frame_scope()
            if self.frame < s or self.frame >= e:
                self.frame = s
            else:
                self.frame += 1
            self.image = self.images[self.frame]


# Alice
class Alice(_Character):
    def __init__(self, x, y, *groups):
        super().__init__(
            GFX["charsets"],
            [
                (0, 48, 14, 17),
                (15, 48, 14, 17),
                (29, 48, 13, 17),
                (43, 48, 12, 17),
                (56, 48, 12, 17),
                (69, 48, 12, 17),
                (82, 48, 14, 17),
                (97, 48, 14, 17),
                (112, 48, 13, 17),
                (126, 48, 12, 17),
                (139, 48, 12, 17),
                (152, 48, 12, 17),
            ],
            x,
            y,
            9,
            3.25,
            *groups
        )


# 标签
class Label(_Black):
    def __init__(self, x, y, *groups):
        super().__init__(GFX["text"], [(0, 0, 301, 248)], x, y, 0, 1, *groups)


# 菜单
class Menu(_Game):
    class Wanda(Wanda):
        pass

    class Alice(Alice):
        def update(self):
            pass

    def new_game(self):
        self.background = pygame.Surface([X, Y])
        self.background.fill((0, 0, 0))
        self.background_rect = self.background.get_rect()

        self.menu = pygame.Surface((self.background_rect.w, self.background_rect.h))
        self.viewport = SCREEN.get_rect(bottom=self.background_rect.bottom)

        # 设置标题
        label_data = [((X / 2) - (301 / 2), (Y / 2) - (248 / 2) - 75)]
        for x, y in label_data:
            self.sprites.add(Label(x, y, pygame.sprite.Group()))

        # 设置 Wanda 到屏幕的左下角
        wanda_data = [(25, Y - 80)]
        for x, y in wanda_data:
            self.sprites.add(Menu.Wanda(x, y, pygame.sprite.Group()))

        # 设置 Alice 到屏幕的右下角
        alice_data = [(X - (12 * 3.25) - 25, Y - 75)]
        for x, y in alice_data:
            self.sprites.add(Menu.Alice(x, y, pygame.sprite.Group()))

    def draw(self):
        # 重新绘制背景，这里主要是处理图片移动后会留下残影的问题
        self.menu.blit(self.background, self.viewport, self.viewport)
        # 绘制全部 Sprite 到背景中
        self.sprites.draw(self.menu)
        # 绘制背景到屏幕中
        SCREEN.blit(self.menu, (0, 0), self.viewport)


# 砖头
class _Brick(_Black):
    def __init__(self, img_rect_list, x, y, i, *groups):
        super().__init__(GFX["tileset"], img_rect_list, x, y, i, 2.65, *groups)


# 橙色的砖头
class OrangeBrick(_Brick):
    def __init__(self, x, y, *groups):
        super().__init__([(16, 0, 10, 10), (432, 0, 10, 10)], x, y, 0, *groups)


# 绿色的砖头
class GreenBrick(_Brick):
    def __init__(self, x, y, *groups):
        super().__init__([(208, 32, 10, 10), (48, 32, 10, 10)], x, y, 0, *groups)


BRICK_DICT = {0: OrangeBrick, 1: GreenBrick}


# 地图
class Map(_Game):
    def new_game(self):
        # 设置地图
        self.map = pygame.Surface([X, Y])
        self.map.fill((0, 0, 0))

        # 设置砖头
        brick_data = [(220, 100, 0), (246, 100, 0)]
        for x, y, t in brick_data:
            self.sprites.add(BRICK_DICT[t](x, y, pygame.sprite.Group()))

    def draw(self):
        # 绘制全部 Sprite 到地图中
        self.sprites.draw(self.map)
        # 绘制地图到屏幕
        SCREEN.blit(self.map, (0, 0))


# 初始化 pygame
pygame.init()

# 用于获取帧数
CLOCK = pygame.time.Clock()

# 用于设置屏幕的宽度和高度
X = 800
Y = 600
FPS = 16

# 创建屏幕对象
SCREEN = pygame.display.set_mode([X, Y])

# 加载所有图形资源文件
GFX: dict[str, pygame.Surface] = load_gfx(os.path.join("gfx"))

# 创建新的游戏对象
GAME = Menu()

# 用于获取用户的键盘输入情况
PRESSED_KEYS = pygame.key.get_pressed()

while not GAME.deno:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            GAME.deno = True
        else:
            PRESSED_KEYS = pygame.key.get_pressed()

    GAME.update()
    GAME.draw()
    pygame.display.update()

    # 确保程序保持指定的帧数
    CLOCK.tick(FPS)

pygame.quit()
