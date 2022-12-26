from sprite_object import *
from random import randint, random

class Npc(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animationTime=180):
        super().__init__(game, path, pos, scale, shift, animationTime)
        self.attackImages = self.getImages(self.path + '/attack')
        self.deathImages = self.getImages(self.path + '/death')
        self.idleImages = self.getImages(self.path + '/idle')
        self.painImages = self.getImages(self.path + '/pain')
        self.walkImages = self.getImages(self.path + '/walk')

        self.attackDist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attackDamage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.rayCastValue = False
        self.frameCounter = 0
        self.playerSearchTrigger = False

    def update(self):
        self.checkAnimationTime()
        self.getSprite()
        self.runLogic()
        # self.drawRayCast()

    def checkWall(self, x, y):
        return (x, y) not in self.game.map.worldMap

    def checkWallCollision(self, dx, dy):
        if self.checkWall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.checkWall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        nextPos = self.game.pathFinding.getPath(self.mapPos, self.game.player.mapPos)
        nextX, nextY = nextPos

        # pygame.draw.rect(self.game.screen, 'blue', (100 * nextX, 100 * nextY, 100, 100))
        if nextPos not in self.game.objectHandler.npcPositions:
            angle = math.atan2(nextY + 0.5 - self.y, nextX + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.checkWallCollision(dx, dy)

    def attack(self):
        if self.animationTrigger:
            self.game.sound.npcShot.play()
            if random() < self.accuracy:
                self.game.player.getDamage(self.attackDamage)

    def animateDeath(self):
        if not self.alive:
            if self.game.globalTrigger and self.frameCounter < len(self.deathImages) - 1:
                self.deathImages.rotate(-1)
                self.image = self.deathImages[0]
                self.frameCounter += 1

    def animatePain(self):
        self.animate(self.painImages)
        if self.animationTrigger:
            self.pain = False

    def checkHitInNpc(self):
        if self.rayCastValue and self.game.player.shot:
            if HALF_WIDTH - self.spriteHalfWidth < self.screenX < HALF_WIDTH + self.spriteHalfWidth:
                self.game.sound.npcPain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.checkHealth()

    def checkHealth(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npcDeath.play()

    def runLogic(self):
        if self.alive:
            self.rayCastValue = self.rayCastPlayerNpc()
            self.checkHitInNpc()

            if self.pain:
                self.animatePain()
            elif self.rayCastValue:
                self.playerSearchTrigger = True

                if self.dist < self.attackDist:
                    self.animate(self.attackImages)
                    self.attack()
                else:
                    self.animate(self.walkImages)
                    self.movement()
            elif self.playerSearchTrigger:
                self.animate(self.walkImages)
                self.movement()
            else:
                self.animate(self.idleImages)
        else:
            self.animateDeath()

    @property
    def mapPos(self):
        return int(self.x), int(self.y)

    def rayCastPlayerNpc(self):
        if self.game.player.mapPos == self.mapPos:
            return True

        wallDistV, wallDistH = 0, 0
        playerDistV, playerDistH = 0, 0

        ox, oy = self.game.player.pos
        xMap, yMap = self.game.player.mapPos

        rayAngle = self.theta

        sinA = math.sin(rayAngle)
        cosA = math.cos(rayAngle)

        yHor, dy = (yMap + 1, 1) if sinA > 0 else (yMap - 1e-6, -1)

        depthHor = (yHor - oy) / sinA
        xHor = ox + depthHor * cosA

        deltaDepth = dy / sinA
        dx = deltaDepth * cosA

        for i in range(MAX_DEPTH):
            tileHor = int(xHor), int(yHor)
            if tileHor == self.mapPos:
                playerDistH = depthHor
                break
            if tileHor in self.game.map.worldMap:
                wallDistH = depthHor
                break
            xHor += dx
            yHor += dy
            depthHor += deltaDepth

        xVert, dx = (xMap + 1, 1) if cosA > 0 else (xMap - 1e-6, -1)

        depthVert = (xVert - ox) / cosA
        yVert = oy + depthVert * sinA

        deltaDepth = dx / cosA
        dy = deltaDepth * sinA

        for i in range(MAX_DEPTH):
            tileVert = int(xVert), int(yVert)
            if tileVert == self.mapPos:
                playerDistV = depthVert
                break
            if tileVert in self.game.map.worldMap:
                wallDistV = depthVert
                break
            xVert += dx
            yVert += dy
            depthVert += deltaDepth

        playerDist = max(playerDistV, playerDistH)
        wallDist = max(wallDistV, wallDistH)

        if 0 < playerDist < wallDist or not wallDist:
            return True
        return False

    def drawRayCast(self):
        pygame.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.rayCastPlayerNpc():
            pygame.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y), (100 * self.x, 100 * self.y), 2)

class SoldierNpc(Npc):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animationTime=180):
        super().__init__(game, path, pos, scale, shift, animationTime)

class CacoDemonNpc(Npc):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos=(10.5, 6.5), scale=0.7, shift=0.27, animationTime=250):
        super().__init__(game, path, pos, scale, shift, animationTime)
        self.attackDist = 1
        self.health = 150
        self.attackDamage = 25
        self.speed = 0.05
        self.accuracy = 0.35

class CyberDemonNpc(Npc):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6), scale=1, shift=0.04, animationTime=210):
        super().__init__(game, path, pos, scale, shift, animationTime)
        self.attackDist = 6
        self.health = 200
        self.attackDamage = 15
        self.speed = 0.055
        self.accuracy = 0.25
