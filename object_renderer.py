import pygame
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.wallTextures = self.loadWallTextures()
        self.skyImage = self.getTexture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.skyOffset = 0
        self.bloodScreen = self.getTexture('resources/textures/blood_screen.png', RES)
        self.digitSize = 90
        self.digitImages = [self.getTexture(f'resources/textures/digits/{i}.png', [self.digitSize] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digitImages))
        self.gameOverImage = self.getTexture('resources/textures/game_over.png', RES)

    def draw(self):
        self.drawBackground()
        self.renderGameObjects()
        self.drawPlayerHealth()

    def gameOver(self):
        self.screen.blit(self.gameOverImage, (0, 0))

    def drawPlayerHealth(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digitSize, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digitSize, 0))

    def playerDamage(self):
        self.screen.blit(self.bloodScreen, (0, 0))

    def drawBackground(self):
        self.skyOffset = (self.skyOffset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.skyImage, (-self.skyOffset, 0))
        self.screen.blit(self.skyImage, (-self.skyOffset + WIDTH, 0))

        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def renderGameObjects(self):
        listObjects = sorted(self.game.raycasting.objectsToRender, key=lambda t: t[0], reverse=True)
        for depth, image, pos in listObjects:
            self.screen.blit(image, pos)

    @staticmethod
    def getTexture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def loadWallTextures(self):
        return {
            1: self.getTexture('resources/textures/1.png'),
            2: self.getTexture('resources/textures/2.png'),
            3: self.getTexture('resources/textures/3.png'),
            4: self.getTexture('resources/textures/4.png'),
            5: self.getTexture('resources/textures/5.png')
        }
