import pygame
from ui import *
from menu import *
import sys
from engine import *

#Configs
pygame.init()
tamanho_tela = (800, 600)
podeclicar = True
espera = 1000
ultimo_click = 0
tela = pygame.display.set_mode(tamanho_tela, pygame.SCALED)

caminho_imagem = "assets\\image\\background.png" 
imagem_fundo = pygame.image.load(caminho_imagem).convert()
img_papel = pygame.image.load("assets\\image\\papel.png").convert_alpha()
img_botao_verde = pygame.image.load("assets\\image\\sim.png").convert_alpha()
img_botao_vermelho = pygame.image.load("assets\\image\\nao.png").convert_alpha()

pygame.display.set_caption("Ponto sem volta")
tela_cheia = False

if menu(tela):
    print("Iniciando o jogo...")

musica = "assets\\sounds\\intro.mp3"
pygame.mixer.music.load(musica)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
som_clique = pygame.mixer.Sound("assets\\sounds\\escolha.mp3")
som_clique.set_volume(0.8) # Um pouco mais alto que a música para dar impacto
motor = Engine()

while True:

    #tempo e medição tela   
    tempo = pygame.time.get_ticks()
    largura_atual, altura_atual = tela.get_size()
    fundo_ajustado = pygame.transform.scale(imagem_fundo, (largura_atual, altura_atual))
    tela.blit(fundo_ajustado, (0, 0))
    pergunta_atual = motor.obter_pergunta_atual()
    btn_nao, btn_sim = criar_elementos(tela, img_botao_vermelho, img_botao_verde, img_papel, pergunta_atual) #Tras os botoes para a tela

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            #F11
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            #ESQ
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and podeclicar: #Ações desbloqueadas para clicar
            #Caminho sim
            if btn_sim.collidepoint(event.pos):
                print("Clicou no VERDE (Sim)!")
                estado_jogo = motor.processar_escolha("sim")
                podeclicar = False
                ultimo_click = tempo
                som_clique.play()
                if estado_jogo != "jogando":
                    print(f"Jogo Acabou, {estado_jogo}")
                    pygame.quit()
                    sys.exit()

            #Caminho não
            if btn_nao.collidepoint(event.pos):
                print("Clicou no VERMELHO (Não)!")
                estado_jogo = motor.processar_escolha("nao")
                podeclicar = False
                ultimo_click = tempo
                som_clique.play()
                if estado_jogo != "jogando":
                    print(f"Jogo Acabou, {estado_jogo}")
                    pygame.quit()
                    sys.exit()
    if not podeclicar:
        if tempo - ultimo_click > espera: #Tempo de espera para clicar novamente
            podeclicar = True        

    pygame.display.flip()