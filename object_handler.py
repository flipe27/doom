from npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.spriteList = []
        self.npcList = []
        self.npcSpritesPath = 'resources/sprites/npc/'
        self.staticSpritesPath = 'resources/sprites/static_sprites/'
        self.animSpritesPath = 'resources/sprites/animated_sprites/'
        addSprite = self.addSprite
        addNpc = self.addNpc
        self.npcPositions = {}

        addSprite(SpriteObject(game))
        addSprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        addSprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        addSprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        addSprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        addSprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        addSprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        addSprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        addSprite(AnimatedSprite(game, path=self.animSpritesPath + '/red_light/0.png', pos=(14.5, 7.5)))
        addSprite(AnimatedSprite(game, path=self.animSpritesPath + '/red_light/0.png', pos=(12.5, 7.5)))
        addSprite(AnimatedSprite(game, path=self.animSpritesPath + '/red_light/0.png', pos=(9.5, 7.5)))

        addNpc(SoldierNpc(game))
        addNpc(SoldierNpc(game, pos=(7, 4.5)))
        addNpc(SoldierNpc(game, pos=(11.5, 4.5)))
        addNpc(CacoDemonNpc(game))
        addNpc(CacoDemonNpc(game, pos=(7, 2.5)))
        addNpc(CyberDemonNpc(game))

    def update(self):
        self.npcPositions = {npc.mapPos for npc in self.npcList if npc.alive}
        [sprite.update() for sprite in self.spriteList]
        [npc.update() for npc in self.npcList]

    def addNpc(self, npc):
        self.npcList.append(npc)

    def addSprite(self, sprite):
        self.spriteList.append(sprite)
