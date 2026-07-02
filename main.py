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

def tocar_video(caminho_video, tela , caminho_audio):
    cap = cv2.VideoCapture(caminho_video)
    relogio = pygame.time.Clock()
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: 
        fps = 30
    print(f"caminho_audio: {caminho_audio}")
    
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
                # Adicionando o F11 nos vídeos:
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


pygame.init()
pygame.mixer.init()

tamanho_tela = (800, 600)
podeclicar = True
espera = 2000
ultimo_click = 0
tela = pygame.display.set_mode(tamanho_tela, pygame.SCALED)
try:
    icone_jogo = pygame.image.load("assets\\image\\seu_icone.png").convert_alpha()
    pygame.display.set_icon(icone_jogo)
except:
    print("Aviso: Ícone não encontrado.")
# --- CARREGAMENTO DAS IMAGENS ---
caminho_imagem = "assets\\image\\background.png" 
imagem_fundo = pygame.image.load(caminho_imagem).convert()
img_papel = pygame.image.load("assets\\image\\papel.png").convert_alpha()
img_botao_verde = pygame.image.load("assets\\image\\sim.png").convert_alpha()
img_botao_vermelho = pygame.image.load("assets\\image\\nao.png").convert_alpha()

# Imagens da Cutscene do Relatório Mensal
img_fundo_cutscene = pygame.image.load("assets\\image\\fundocutscene.png").convert()
img_papel_cutscene = pygame.image.load("assets\\image\\papelcutscene.png").convert_alpha()

pygame.display.set_caption("Ponto sem volta")

if menu(tela):
    pass

musica = "assets\\sounds\\intro.mp3"
if os.path.exists(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

# --- CARREGAMENTO DE EFEITOS SONOROS ---
try:
    som_clique = pygame.mixer.Sound("assets\\sounds\\escolha.mp3")
    som_clique.set_volume(0.2)
except:
    som_clique = None

try:
    som_respiracao = pygame.mixer.Sound("assets\\sounds\\resp.mp3") 
    som_respiracao.set_volume(0.3) 
except:
    som_respiracao = None

# Tenta carregar os novos sons do papel. Se não existirem, não irá crashar.
try:
    som_papel_entrada = pygame.mixer.Sound("assets\\sounds\\papel_desliza.mp3")
except:
    som_papel_entrada = None

try:
    som_papel_saida = pygame.mixer.Sound("assets\\sounds\\papel_amassa.mp3")
except:
    som_papel_saida = None


ultimo_toque_respiracao = 0
intervalo_respiracao = random.randint(10000, 20000) 

motor = Engine()

btn_sim = None
btn_nao = None

# Variáveis de controle de fluxo de animação
esperando_animacao_saida = False
escolha_pendente = None

# Resetar o papel logo no início para garantir que ele chegue animado da esquerda
resetar_papel_nova_pergunta()

while True:
    tempo = pygame.time.get_ticks()
    largura_atual, altura_atual = tela.get_size()
    
    # Efeito sonoro aleatório de respiração
    if som_respiracao and tempo - ultimo_toque_respiracao > intervalo_respiracao:
        som_respiracao.play()
        ultimo_toque_respiracao = tempo
        intervalo_respiracao = random.randint(15000, 40000)
        
    # Animação de flutuação do fundo
    onda_y = math.sin(tempo * 0.0015) * 4 + math.sin(tempo * 0.0006) * 3
    onda_x = math.cos(tempo * 0.0010) * 2 + math.cos(tempo * 0.0004) * 2
    
    fundo_ajustado = pygame.transform.scale(imagem_fundo, (largura_atual + 20, altura_atual + 20))
    tela.blit(fundo_ajustado, (-10 + onda_x, -10 + onda_y))
    
    # Renderização da Carta e Botões (agora passando os sons de entrada/saída do papel)
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
    
    # Processamento de Eventos
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

        # O clique só é registrado se NÃO estivermos esperando o papel sair
        if event.type == pygame.MOUSEBUTTONDOWN and podeclicar and not esperando_animacao_saida:
            
            if btn_sim and btn_sim.collidepoint(event.pos):
                escolha_pendente = "sim"
                if som_clique: som_clique.play()
                
                # Desativa cliques e inicia a animação de saída da folha
                podeclicar = False
                disparar_saida_papel()
                esperando_animacao_saida = True
                
            elif btn_nao and btn_nao.collidepoint(event.pos):
                escolha_pendente = "nao"
                if som_clique: som_clique.play()
                
                # Desativa cliques e inicia a animação de saída da folha
                podeclicar = False
                disparar_saida_papel()
                esperando_animacao_saida = True

    # --- LÓGICA DE TRANSIÇÃO (Dispara somente quando a folha some da tela) ---
    if esperando_animacao_saida:
        if papel_saiu_da_tela(largura_atual):
            
            # Agora sim, processamos a escolha que estava pendente
            resultado = motor.processar_escolha(escolha_pendente)
            
            if resultado == "fim_mes":
                # Chama a cutscene bloqueante do relatório
                historia = motor.obter_texto_mes()
                exibir_relatorio_mensal(tela, img_fundo_cutscene, img_papel_cutscene, historia, motor.status, motor.mes_atual - 1)
                ultimo_toque_respiracao = pygame.time.get_ticks()
                
            elif resultado != "jogando":
                # Fim de Jogo
                salvar_progresso_final(resultado)
                caminho_video = f"assets\\videos\\finals\\{resultado}.mp4"
                caminho_audio = f"assets\\sounds\\finals_reformulado\\{resultado}.mp3"
                tocar_video(caminho_video, tela , caminho_audio)
                
                if menu(tela):
                    pass
                motor = Engine()
                ultimo_toque_respiracao = pygame.time.get_ticks()

            # Ao fim do processamento (seja jogando, fim de mês ou restart após o final)
            # Limpamos a tela, puxamos o papel de volta da esquerda e liberamos o clique
            resetar_papel_nova_pergunta()
            esperando_animacao_saida = False
            ultimo_click = pygame.time.get_ticks()

    # Controle de cooldown do clique por segurança
    if not podeclicar and not esperando_animacao_saida:
        if tempo - ultimo_click > espera:
            podeclicar = True        

    pygame.display.flip()