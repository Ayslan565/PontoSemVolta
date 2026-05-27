import pygame
import math
import random
import sys
import os
import json
import cv2
import numpy as np

from src.ui.ui import *
from src.states.menu import *
from src.core.engine import *

def salvar_progresso_final(nome_do_final):
    caminho_save = "data\\save.json"
    dados = {"finais_vistos": []}
    
    os.makedirs(os.path.dirname(caminho_save), exist_ok=True)
    
    if os.path.exists(caminho_save):
        try:
            with open(caminho_save, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except Exception:
            pass
            
    if nome_do_final not in dados.get("finais_vistos", []):
        if "finais_vistos" not in dados:
            dados["finais_vistos"] = []
        dados["finais_vistos"].append(nome_do_final)
        
        with open(caminho_save, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)

def tocar_video(caminho_video, tela):
    cap = cv2.VideoCapture(caminho_video)
    relogio = pygame.time.Clock()
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: 
        fps = 30
        
    pygame.mixer.music.pause()
    caminho_audio = caminho_video.replace(".mp4", ".mp3")
    rodando = True
    som_video = None
    if os.path.exists(caminho_audio):
        som_video = pygame.mixer.Sound(caminho_audio)
        som_video.play()
    else:
        print(f"Aviso: Áudio não funciona, deu ruim {caminho_audio}")

    while rodando and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if som_video: som_video.stop()
                cap.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
        frame_surface = pygame.transform.scale(frame_surface, tela.get_size())
        
        tela.blit(frame_surface, (0, 0))
        pygame.display.flip()
        relogio.tick(fps)
        
        if som_video: 
            som_video.stop()
    cap.release()
    pygame.mixer.music.unpause()

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

som_respiracao = pygame.mixer.Sound("assets\\sounds\\resp.mp3") 
som_respiracao.set_volume(0.4) 
ultimo_toque_respiracao = 0
intervalo_respiracao = random.randint(10000, 20000) 
motor = Engine()
mostrar_status = False

while True:
    tempo = pygame.time.get_ticks()
    largura_atual, altura_atual = tela.get_size()
    
    if tempo - ultimo_toque_respiracao > intervalo_respiracao:
        som_respiracao.play()
        ultimo_toque_respiracao = tempo
        intervalo_respiracao = random.randint(15000, 40000)
        
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
                    salvar_progresso_final(estado_jogo)
                    caminho_video = f"assets\\videos\\finals\\{estado_jogo}.mp4" 
                    tocar_video(caminho_video, tela)
                    
                    if menu(tela):
                        pass
                    motor = Engine()
                    ultimo_toque_respiracao = pygame.time.get_ticks()

            elif btn_nao.collidepoint(event.pos):
                estado_jogo = motor.processar_escolha("nao")
                podeclicar = False
                ultimo_click = tempo
                som_clique.play()
                
                if estado_jogo != "jogando":
                    salvar_progresso_final(estado_jogo)
                    caminho_video = f"assets\\videos\\finals\\{estado_jogo}.mp4"
                    tocar_video(caminho_video, tela)
                    
                    if menu(tela):
                        pass
                    motor = Engine()
                    ultimo_toque_respiracao = pygame.time.get_ticks()
                    
    if not podeclicar:
        if tempo - ultimo_click > espera:
            podeclicar = True        

    pygame.display.flip()