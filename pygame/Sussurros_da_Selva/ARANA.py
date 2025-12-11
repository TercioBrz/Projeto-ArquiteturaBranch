import pygame
from pygame.locals import *
import os

def pathabs(*partes):
    dir_atual = os.path.dirname(__file__)

    return os.path.join(dir_atual, *partes)

class Arana(pygame.sprite.Sprite):
    def __init__(self, nome, x, y, escala, chao_Y, largura, vida=3):
        super().__init__()
        self.nome = nome
        self.vida = vida
        self.vivo = True

        self.largura = largura
        self.chao_Y = chao_Y
        #self.rect = pygame.Rect(x,y,40,80)
        self.velocidade_x = 6.5
        self.velocidade_y = 0
        self.gravidade = 1
        self.esta_no_ar = False
        self.direcao = 1

        self.invulneravel = False
        self.tempo_ultimo_dano = 0
        self.tempo_invulnerabilidade = 1000
        self.intervalo_piscar = 100
        self.mostrar_sprite = True

        self.giro = False 
        self.atualizar_time = pygame.time.get_ticks()       # pega o horario atual,em q foi criado a instancia, essencial para trabalhar com as animações
        self.lista_animacoes = []
        self.indice_frame = 0
        self.acao = 0

        self.atirando = False
        self.tempo_inicio_tiro = 0
        self.duracao_tiro = 300
        self.carregar_animacoes(escala)

        self.img = self.lista_animacoes[self.acao][self.indice_frame]    #primeira imagem carregada, ou seja o presonagem começa com a imagem padrão
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)


    def carregar_animacoes(self, escala):

        animacoes = [
            ('arana_normal', 5),
            ('arana_correndo', 4),
            ('arana_pulando', 9),
            ('arana_atirando_parado', 3),
            ('arana_atirando_correndo', 3),
            ('arana_atirando_pulando', 6),
            ('arana_morrendo', 6)
        ]

        for pasta, quantidade in animacoes:
            frames = []
            for i in range(quantidade):
                caminho = pathabs(f'assets/images/arana/{pasta}/{i}.png')
                imagem = pygame.image.load(caminho)
                imagem = pygame.transform.scale(
                    imagem,
                    (int(imagem.get_width() * escala), int(imagem.get_height() * escala))
                )
                frames.append(imagem)
            self.lista_animacoes.append(frames)


    def desenhar(self, tela):

        if self.mostrar_sprite == True:
            tela.blit(pygame.transform.flip(self.img, self.giro, False) ,self.rect)
        
    def atualizar(self):

        #condicao para o arana pular e voltar para o chao
        if self.esta_no_ar:
            self.velocidade_y += self.gravidade
            self.rect.y += self.velocidade_y
            
        #condicao para arana ao pular, ele voltar e parar no chao
        if self.rect.bottom >= self.chao_Y:
            self.rect.bottom = self.chao_Y
            self.velocidade_y = 0
            self.esta_no_ar = False

        tempo_atual = pygame.time.get_ticks()

        #condicao em que arana nao pode tomar dano

        if self.invulneravel == True:
            if (tempo_atual - self.tempo_ultimo_dano) // self.intervalo_piscar % 2 == 0:
                self.mostrar_sprite = False
            else:
                self.mostrar_sprite = True

            if tempo_atual - self.tempo_ultimo_dano >= self.tempo_invulnerabilidade:
                self.invulneravel = False
                self.mostrar_sprite = True

        #condicao para tiro do arana

        if self.atirando and tempo_atual - self.tempo_inicio_tiro >= self.duracao_tiro:
            self.atirando = False
            if not self.esta_no_ar:
                self.atualizar_acoes(0)

    def atualizar_acoes(self, nova_acao):
        #checar se a vova ação é diferente da anterior
        if nova_acao != self.acao:
            self.acao = nova_acao                                         #uma nova ação vai ser definida 
            self.indice_frame = 0                                           #atualiza para o primeiro frame de volta, para ficar mais fluido
            self.atualizar_time = pygame.time.get_ticks()

    def atualizar_animacao(self):
        #atualizando animação
        INTERVALO_ANIMACAO = 110                       # é o cooldown de uma animaçaõ para outra, é uma constante
        #atualizando o frame independente da frame tual 
        self.img = self.lista_animacoes[self.acao][self.indice_frame]

        #vendo o horario atual novamente para saber quanto tempo passou desde a ultima checagem
        if pygame.time.get_ticks() - self.atualizar_time > INTERVALO_ANIMACAO:              #se o tempo for maior, passar para o rpoximo quadro
            self.atualizar_time = pygame.time.get_ticks()
            self.indice_frame += 1

        #se as animações acabaram, entao renicie do começo 
        if self.indice_frame >= len(self.lista_animacoes[self.acao]):
            self.indice_frame = 0
    
    def movimento(self,teclas):
        movendo = False

        if teclas[K_a]:
            self.direcao = -1
            self.rect.x -= self.velocidade_x
            self.giro = True
            movendo = True
    
            if self.rect.x < -15:
                self.rect.x = -15
        if teclas[K_d]:
            self.direcao = 1
            self.rect.x += self.velocidade_x
            self.giro = False
            movendo = True
            
            if self.rect.x > self.largura - 108:
                self.rect.x = self.largura - 108

        if teclas[K_w]:
            self.pular()   
            

        if self.esta_no_ar and self.atirando:
            self.atualizar_acoes(5)

        elif self.esta_no_ar:
            self.atualizar_acoes(2)

        elif self.atirando:

            if movendo:
                self.atualizar_acoes(4)

            else:
                self.atualizar_acoes(3)

        elif movendo:
            self.atualizar_acoes(1)

        else:
            self.atualizar_acoes(0)

    def pular(self):
        if not self.esta_no_ar:
            self.velocidade_y = -20
            self.esta_no_ar = True
            self.atualizar_acoes(2)

    def atirar(self):
        if self.atirando == False:
            self.atirando = True
            self.tempo_inicio_tiro = pygame.time.get_ticks()
            self.atualizar_acoes(3)


    def tomar_dano(self, dano = 1):

        tempo_atual = pygame.time.get_ticks()

        if self.vivo and self.invulneravel == False:
            self.vida -= dano
            if self.vida == 0:
                self.vivo = False

            self.invulneravel = True
            self.tempo_ultimo_dano = tempo_atual