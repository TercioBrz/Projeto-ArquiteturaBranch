import pygame
import os

def pathabs6(*partes):
    dir_atual = os.path.dirname(__file__)

    return os.path.join(dir_atual, *partes)

class Vilao(pygame.sprite.Sprite):
    def __init__(self, nome_pasta, x, y, escala, tela, vida = 100):
        
        pygame.sprite.Sprite.__init__(self)
        self.vida = vida
        self.vivo = True
        self.giro = False
        self.atualizar_time = pygame.time.get_ticks()
        self.nome_pasta = nome_pasta
        self.lista_animacoes = []
        self.indice_frame = 0
        self.acao = 0
        self.tela = tela
        self.carregar_animacoes(escala)

        
        #sprites obsoleto
        lista_temporaria = []
        for c in range (3):
            imagem = pygame.image.load(pathabs6(f'images/{self.nome_pasta}/obsoleto/{c}.png'))
            imagem = pygame.transform.scale(imagem, (int(imagem.get_width() * escala), int(imagem.get_height() * escala)) )
            lista_temporaria.append(imagem)
        self.lista_animacoes.append(lista_temporaria)

        #sprites dele lancando magia 
        lista_temporaria = []
        for c in range (4):
            imagem = pygame.image.load(pathabs6(f'images/{self.nome_pasta}/lancar_magia/{c}.png'))
            imagem = pygame.transform.scale(imagem, (int(imagem.get_width() * escala), int(imagem.get_height() * escala)) )
            lista_temporaria.append(imagem)
        self.lista_animacoes.append(lista_temporaria)

        self.img = self.lista_animacoes[self.acao][self.indice_frame]
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

#--------------------------------------

    def atualizar_animacao(self):
        #atualizando animação
        INTERVALO_ANIMACAO = 200                        # é o cooldown de uma animaçaõ para outra, é uma constante
        #atualizando o frame independente da frame tual 
        self.img = self.lista_animacoes[self.acao][self.indice_frame]

        #vendo o horario atual novamente para saber quanto tempo passou desde a ultima checagem
        if pygame.time.get_ticks() - self.atualizar_time > INTERVALO_ANIMACAO:              #se o tempo for maior, passar para o rpoximo quadro
            self.atualizar_time = pygame.time.get_ticks()
            self.indice_frame += 1

        #se as animações acabaram, entao renicie do começo 
        if self.indice_frame >= len(self.lista_animacoes[self.acao]):
            self.indice_frame = 0


    def atualizar_acoes(self, nova_acao):
        #checar se a vova ação é diferente da anterior
        if nova_acao != self.acao:
            self.acao = nova_acao                                         #uma nova ação vai ser definida 
            self.indice_frame = 0                                           #atualiza para o primeiro frame de volta, para ficar mais fluido
            self.atualizar_time = pygame.time.get_ticks()                   #atualiza o relogio de transição de frames tbm
    
    def desenhar(self):
        if self.vivo == True:
            #self.tela.blit(self.img ,self.rect)
            self.tela.blit(pygame.transform.flip(self.img, self.giro, False) ,self.rect)

    def tomar_dano(self, dano = 1):
        if self.vivo:
            self.vida -= dano
            if self.vida <= 0:
                self.vivo = False

    def carregar_animacoes(self, escala):

        for c in range(3):
            imagem = pygame.image.load(pathabs6(f'images/projeteis/{self.nome_pasta}/{c}.png'))
            imagem = pygame.transform.scale(imagem,
            (int(imagem.get_width() * escala), int(imagem.get_height() * escala)))
            self.lista_animacoes.append(imagem)

#============================================================================================================
