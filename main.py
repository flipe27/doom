from pygame.locals import *
import sys
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.deltaTime = 1
        self.globalTrigger = False
        self.globalEvent = pygame.USEREVENT + 0
        pygame.time.set_timer(self.globalEvent, 40)
        self.newGame()

    def newGame(self):
        self.map = Map(self)
        self.player = Player(self)
        self.objectRenderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.objectHandler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathFinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.objectHandler.update()
        self.weapon.update()
        pygame.display.flip()
        self.deltaTime = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.objectRenderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def checkEvents(self):
        self.globalTrigger = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_SPACE):
                pygame.quit()
                sys.exit()
            elif event.type == self.globalEvent:
                self.globalTrigger = True
            self.player.singleFireEvent(event)

    def run(self):
        while True:
            self.checkEvents()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
