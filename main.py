import pygame
import math
import random # Importação para gerar tempos aleatórios
from ui import *
from menu import *
import sys
from engine import *

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
    pass

musica = "assets\\sounds\\intro.mp3"
pygame.mixer.music.load(musica)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

som_clique = pygame.mixer.Sound("assets\\sounds\\escolha.mp3")
som_clique.set_volume(0.8)

# --- Configuração do som de respiração ---
som_respiracao = pygame.mixer.Sound("assets\\sounds\\resp.mp3") # Substitua pelo nome exato do seu arquivo
som_respiracao.set_volume(0.4) 
ultimo_toque_respiracao = 0
intervalo_respiracao = random.randint(10000, 20000) # Começa tocando entre 10 a 20 segundos

motor = Engine()
mostrar_status = False

while True:
    tempo = pygame.time.get_ticks()
    largura_atual, altura_atual = tela.get_size()
    
    # --- Toca o som de respiração aleatoriamente ---
    if tempo - ultimo_toque_respiracao > intervalo_respiracao:
        som_respiracao.play()
        ultimo_toque_respiracao = tempo
        intervalo_respiracao = random.randint(15000, 40000) # Sorteia o próximo suspiro (entre 15 e 40 seg)
        
    onda_y = math.sin(tempo * 0.0015) * 4 + math.sin(tempo * 0.0006) * 3
    onda_x = math.cos(tempo * 0.0010) * 2 + math.cos(tempo * 0.0004) * 2
    
    fundo_ajustado = pygame.transform.scale(imagem_fundo, (largura_atual + 20, altura_atual + 20))
    tela.blit(fundo_ajustado, (-10 + onda_x, -10 + onda_y))
    
    pergunta_atual = motor.obter_pergunta_atual()
    btn_nao, btn_sim = criar_elementos(tela, img_botao_vermelho, img_botao_verde, img_papel, pergunta_atual)
    btn_status = desenhar_painel_status(tela, motor.status, mostrar_status)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and podeclicar:
            if btn_status.collidepoint(event.pos):
                mostrar_status = not mostrar_status 
                som_clique.play()
                
            elif btn_sim.collidepoint(event.pos):
                estado_jogo = motor.processar_escolha("sim")
                podeclicar = False
                ultimo_click = tempo
                som_clique.play()
                if estado_jogo != "jogando":
                    pygame.quit()
                    sys.exit()

            elif btn_nao.collidepoint(event.pos):
                estado_jogo = motor.processar_escolha("nao")
                podeclicar = False
                ultimo_click = tempo
                som_clique.play()
                if estado_jogo != "jogando":
                    pygame.quit()
                    sys.exit()
                    
    if not podeclicar:
        if tempo - ultimo_click > espera:
            podeclicar = True        

    pygame.display.flip()