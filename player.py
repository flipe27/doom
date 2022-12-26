import pygame
from settings import *
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.healthRecoveryDelay = 700
        self.timePrev = pygame.time.get_ticks()

    def recoverHealth(self):
        if self.checkHealthRecoveryDelay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def checkHealthRecoveryDelay(self):
        timeNow = pygame.time.get_ticks()
        if timeNow - self.timePrev > self.healthRecoveryDelay:
            self.timePrev = timeNow

            return True

    def checkGameOver(self):
        if self.health < 1:
            self.game.objectRenderer.gameOver()
            pygame.display.flip()
            pygame.time.delay(1500)
            self.game.newGame()

    def getDamage(self, damage):
        self.health -= damage
        self.game.objectRenderer.playerDamage()
        self.game.sound.playerPain.play()
        self.checkGameOver()

    def singleFireEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        sinA = math.sin(self.angle)
        cosA = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.deltaTime
        speedSin = speed * sinA
        speedCos = speed * cosA

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speedCos
            dy += speedSin
        if keys[pygame.K_s]:
            dx += -speedCos
            dy += -speedSin
        if keys[pygame.K_a]:
            dx += speedSin
            dy += -speedCos
        if keys[pygame.K_d]:
            dx += -speedSin
            dy += speedCos

        self.checkWallCollision(dx, dy)

        # if keys[pygame.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.deltaTime
        # if keys[pygame.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.deltaTime
        self.angle %= math.tau

    def checkWall(self, x, y):
        return (x, y) not in self.game.map.worldMap

    def checkWallCollision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.deltaTime

        if self.checkWall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.checkWall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        # pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100), (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouseControl(self):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.deltaTime

    def update(self):
        self.movement()
        self.mouseControl()
        self.recoverHealth()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def mapPos(self):
        return int(self.x), int(self.y)
