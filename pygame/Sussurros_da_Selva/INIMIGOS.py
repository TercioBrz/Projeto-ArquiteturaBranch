import pygame
import os 

# essa clase é destinada a tudo, que não seja o jogador e que percorre a tela de um lado a outro
#Como: Bolas de fogo, inimigos rastejantes e voadores outras magias dos bosses

def pathabs3(*partes):
    dir_atual = os.path.dirname(__file__)

    return os.path.join(dir_atual, *partes)

class Inimigos(pygame.sprite.Sprite):
    def __init__(self, nome_pasta, x, y, escala, velocidade, direcao,tela):
        pygame.sprite.Sprite.__init__(self)
        
        self.giro = False
        self.direcao = direcao
        self.velocidade = velocidade
        self.atualizar_time = pygame.time.get_ticks()
        self.nome_pasta = nome_pasta
        self.lista_animacoes = []
        self.indice_frame = 0
        self.acao = 0
        self.tela = tela
        self.carregar_animacoes(escala)


        self.img = self.lista_animacoes[self.indice_frame]
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def atualizar_animacao(self):
            
            INTERVALO_ANIMACAO = 200         # é o cooldown de uma animaçaõ para outra
            #atualizando o frame independente da frame tual 
            self.img = self.lista_animacoes[self.indice_frame]

            #vendo o horario atual novamente para saber quanto tempo passou desde a ultima checagem
            if pygame.time.get_ticks() - self.atualizar_time > INTERVALO_ANIMACAO:   #se o tempo for maior, passar para o rpoximo quadro
                self.atualizar_time = pygame.time.get_ticks()
                self.indice_frame += 1

            #se as animações acabaram, entao renicie do começo 
            if self.indice_frame >= len(self.lista_animacoes):
                self.indice_frame = 0
    
    def movimento(self): # direção é 1 ou 0 
        
        
        if self.direcao == 'direita':                 #movimento da esquerda para direita
            self.rect.x += self.velocidade
            self.giro = True
        
        elif self.direcao == 'esquerda':
            self.rect.x -= self.velocidade          #movimento da direita para esquerda 
            self.giro = False

    def carregar_animacoes(self,escala):

        for c in range(3):
            imagem = pygame.image.load(pathabs3(f'images/projeteis/{self.nome_pasta}/{c}.png'))
            imagem = pygame.transform.scale(imagem,
            (int(imagem.get_width() * escala), int(imagem.get_height() * escala)))
            self.lista_animacoes.append(imagem)

    def desenhar(self):
        #self.tela.blit(self.img ,self.rect)
        self.tela.blit(pygame.transform.flip(self.img, self.giro, False) ,self.rect)

