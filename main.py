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
from src.states.intro import *
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

def tocar_video(caminho_video, tela , caminho_audio):
    cap = cv2.VideoCapture(caminho_video)
    relogio = pygame.time.Clock()
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: 
        fps = 30
    if os.path.exists(caminho_audio):
        audio_video = pygame.mixer.Sound(caminho_audio)
        audio_video.set_volume(0.8)
        pygame.mixer.music.pause()
        audio_video.play(0)
    rodando = True
    som_video = None
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
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
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

def carregar_volumes():
    try:
        with open("data\\config.json", 'r', encoding='utf-8') as f:
            config_salva = json.load(f)
            return config_salva.get("vol_musica", 0.4), config_salva.get("vol_ambiente", 0.3)
    except Exception:
        return 0.4, 0.3

pygame.init()
pygame.mixer.init()

tamanho_tela = (800, 600)
podeclicar = True
espera = 2000
ultimo_click = 0
tela = pygame.display.set_mode(tamanho_tela, pygame.SCALED)

try:
    icone_jogo = pygame.image.load("assets\\image\\icone.png").convert_alpha()
    pygame.display.set_icon(icone_jogo)
except:
    pass

caminho_imagem = "assets\\image\\background.png" 
imagem_fundo = pygame.image.load(caminho_imagem).convert()
img_papel = pygame.image.load("assets\\image\\papel.png").convert_alpha()
img_botao_verde = pygame.image.load("assets\\image\\sim.png").convert_alpha()
img_botao_vermelho = pygame.image.load("assets\\image\\nao.png").convert_alpha()

img_fundo_cutscene = pygame.image.load("assets\\image\\fundocutscene.png").convert()
img_papel_cutscene = pygame.image.load("assets\\image\\papelcutscene.png").convert_alpha()

# --- CARREGA O ÍCONE DE PAUSA ---
try:
    img_pause = pygame.image.load("assets\\image\\pause.png").convert_alpha()
except Exception:
    # Se não encontrar a imagem, desenha o ícone usando Pygame!
    img_pause = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(img_pause, (200, 200, 200), (8, 5, 10, 30), border_radius=3)
    pygame.draw.rect(img_pause, (200, 200, 200), (22, 5, 10, 30), border_radius=3)

pygame.display.set_caption("Ponto sem volta")

if menu(tela):
    exibir_intro(tela)

def aplicar_volumes():
    global vol_musica, vol_ambiente, som_clique, som_respiracao, som_papel_entrada, som_papel_saida
    vol_musica, vol_ambiente = carregar_volumes()
    musica = "assets\\sounds\\intro.mp3"
    if os.path.exists(musica):
        pygame.mixer.music.load(musica)
        pygame.mixer.music.set_volume(vol_musica)
        pygame.mixer.music.play(-1)
    try:
        som_clique = pygame.mixer.Sound("assets\\sounds\\escolha.mp3")
        som_clique.set_volume(vol_ambiente)
    except:
        som_clique = None
    try:
        som_respiracao = pygame.mixer.Sound("assets\\sounds\\resp.mp3") 
        som_respiracao.set_volume(vol_ambiente) 
    except:
        som_respiracao = None
    try:
        som_papel_entrada = pygame.mixer.Sound("assets\\sounds\\papel_desliza.mp3")
        if som_papel_entrada: som_papel_entrada.set_volume(vol_ambiente)
    except:
        som_papel_entrada = None
    try:
        som_papel_saida = pygame.mixer.Sound("assets\\sounds\\papel_amassa.mp3")
        if som_papel_saida: som_papel_saida.set_volume(vol_ambiente)
    except:
        som_papel_saida = None

aplicar_volumes()

ultimo_toque_respiracao = 0
intervalo_respiracao = random.randint(10000, 20000) 

motor = Engine()

btn_sim = None
btn_nao = None
btn_opcoes = None

esperando_animacao_saida = False
escolha_pendente = None

resetar_papel_nova_pergunta()

while True:
    tempo = pygame.time.get_ticks()
    largura_atual, altura_atual = tela.get_size()
    
    if som_respiracao and tempo - ultimo_toque_respiracao > intervalo_respiracao:
        som_respiracao.play()
        ultimo_toque_respiracao = tempo
        intervalo_respiracao = random.randint(15000, 40000)
        
    onda_y = math.sin(tempo * 0.0015) * 4 + math.sin(tempo * 0.0006) * 3
    onda_x = math.cos(tempo * 0.0010) * 2 + math.cos(tempo * 0.0004) * 2
    
    fundo_ajustado = pygame.transform.scale(imagem_fundo, (largura_atual + 20, altura_atual + 20))
    tela.blit(fundo_ajustado, (-10 + onda_x, -10 + onda_y))
    
    pergunta_atual = motor.obter_pergunta_atual()
    btn_nao, btn_sim = criar_elementos(
        tela, 
        img_botao_vermelho, 
        img_botao_verde, 
        img_papel, 
        pergunta_atual,
        som_papel_entrada,
        som_papel_saida
    )
    
    # Renderiza o Botão de Pausa e passa a imagem do ícone!
    btn_opcoes = desenhar_botao_opcoes(tela, img_pause)
    
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

        if event.type == pygame.MOUSEBUTTONDOWN and podeclicar and not esperando_animacao_saida:
            if btn_opcoes.collidepoint(event.pos):
                menu_opcoes_jogo(tela)
                aplicar_volumes()
                
            elif btn_sim and btn_sim.collidepoint(event.pos):
                escolha_pendente = "sim"
                if som_clique: som_clique.play()
                podeclicar = False
                disparar_saida_papel()
                esperando_animacao_saida = True
                
            elif btn_nao and btn_nao.collidepoint(event.pos):
                escolha_pendente = "nao"
                if som_clique: som_clique.play()
                podeclicar = False
                disparar_saida_papel()
                esperando_animacao_saida = True

    if esperando_animacao_saida:
        if papel_saiu_da_tela(largura_atual):
            resultado = motor.processar_escolha(escolha_pendente)
            if resultado == "fim_mes":
                historia = motor.obter_texto_mes()
                exibir_relatorio_mensal(tela, img_fundo_cutscene, img_papel_cutscene, historia, motor.status, motor.mes_atual - 1)
                ultimo_toque_respiracao = pygame.time.get_ticks()
            elif resultado != "jogando":
                salvar_progresso_final(resultado)
                caminho_video = f"assets\\videos\\finals\\{resultado}.mp4"
                caminho_audio = f"assets\\sounds\\finals_reformulado\\{resultado}.mp3"
                tocar_video(caminho_video, tela , caminho_audio)
                if menu(tela):
                    exibir_intro(tela)
                aplicar_volumes()
                motor = Engine()
                ultimo_toque_respiracao = pygame.time.get_ticks()

            resetar_papel_nova_pergunta()
            esperando_animacao_saida = False
            ultimo_click = pygame.time.get_ticks()

    if not podeclicar and not esperando_animacao_saida:
        if tempo - ultimo_click > espera:
            podeclicar = True        

    pygame.display.flip()