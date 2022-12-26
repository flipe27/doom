import pygame

class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pygame.mixer.Sound(self.path + 'shotgun.wav')
        self.npcPain = pygame.mixer.Sound(self.path + 'npc_pain.wav')
        self.npcDeath = pygame.mixer.Sound(self.path + 'npc_death.wav')
        self.npcShot = pygame.mixer.Sound(self.path + 'npc_attack.wav')
        self.playerPain = pygame.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pygame.mixer.Sound(self.path + 'theme.mp3')
