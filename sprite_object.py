import pygame
from settings import *
import os
from collections import deque

class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png', pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = self.game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screenX, self.dist, self.normDist = 0, 0, 0, 0, 1, 1
        self.spriteHalfWidth = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def getSpriteProjection(self):
        proj = SCREEN_DIST / self.normDist * self.SPRITE_SCALE
        projWidth, projHeight = proj * self.IMAGE_RATIO, proj

        image = pygame.transform.scale(self.image, (projWidth, projHeight))

        self.spriteHalfWidth = projWidth // 2
        heightShift = projHeight * self.SPRITE_HEIGHT_SHIFT
        pos = self.screenX - self.spriteHalfWidth, HALF_HEIGHT - projHeight // 2 + heightShift

        self.game.raycasting.objectsToRender.append((self.normDist, image, pos))

    def getSprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        deltaRays = delta / DELTA_ANGLE
        self.screenX = (HALF_NUM_RAYS + deltaRays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.normDist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screenX < (WIDTH + self.IMAGE_HALF_WIDTH) and self.normDist > 0.5:
            self.getSpriteProjection()

    def update(self):
        self.getSprite()

class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png', pos=(11.5, 3.5), scale=0.8, shift=0.15, animationTime=120):
        super().__init__(game, path, pos, scale, shift)
        self.animationTime = animationTime
        self.path = path.rsplit('/', 1)[0]
        self.images = self.getImages(self.path)
        self.animationTimePrev = pygame.time.get_ticks()
        self.animationTrigger = False

    def update(self):
        super().update()
        self.checkAnimationTime()
        self.animate(self.images)

    def animate(self, images):
        if self.animationTrigger:
            images.rotate(-1)
            self.image = images[0]

    def checkAnimationTime(self):
        self.animationTrigger = False
        timeNow = pygame.time.get_ticks()
        if timeNow - self.animationTimePrev > self.animationTime:
            self.animationTimePrev = timeNow
            self.animationTrigger = True

    def getImages(self, path):
        images = deque()
        for fileName in os.listdir(path):
            if os.path.isfile(os.path.join(path, fileName)):
                img = pygame.image.load(path + '/' + fileName).convert_alpha()
                images.append(img)

        return images
