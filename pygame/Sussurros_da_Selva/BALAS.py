import pygame
import os

def pathabs2(*partes):
    dir_atual = os.path.dirname(__file__)

    return os.path.join(dir_atual, *partes)

class Balas(pygame.sprite.Sprite):

    STATIC = {
        "dardo": "assets/images/arana/dardo/dardo.png",
        "flecha": "assets/images/arana/flecha/dardo.png"
    }

    def __init__(self,x,y,direcao,tela):
        super().__init__()
        self.tela = tela
        self.giro = False
        self.dardo = pygame.image.load(pathabs2(Balas.STATIC["dardo"]))
        self.rect = self.dardo.get_rect()
        self.rect.center = (x, y)
        
        
        if direcao == 1:
            self.giro = True
        else:
            self.giro = False

        
        self.velocidade = 15 * direcao
    
    def atualizar(self):
        self.rect.x += self.velocidade
    
    def desenhar(self):
        self.tela.blit(pygame.transform.flip(self.dardo, self.giro, False) ,self.rect)