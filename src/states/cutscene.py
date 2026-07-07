import pygame
import sys
import os
import json
import math
import random

def carregar_som(caminho):
    if os.path.exists(caminho):
        return pygame.mixer.Sound(caminho)
    return None

def carregar_finais_desbloqueados():
    caminho_save = "data\\save.json"
    if os.path.exists(caminho_save):
        try:
            with open(caminho_save, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados.get("finais_vistos", [])
        except Exception:
            return []
    return []

def criar_scanlines(largura, altura):
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for y in range(0, altura, 3):
        pygame.draw.line(surf, (0, 0, 0, 30), (0, y), (largura, y))
    return surf

def desenhar_fade(tela, alpha):
    """Cria uma sobreposição preta de acordo com o valor alpha para os efeitos de fade."""
    if alpha > 0:
        surf_fade = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        surf_fade.fill((0, 0, 0, min(max(int(alpha), 0), 255)))
        tela.blit(surf_fade, (0, 0))

def menu(tela):
    pygame.mixer.init()
    
    # --- MÚSICA DO MENU ---
    caminho_musica = "assets\\sounds\\musica_menu.mp3"
    if os.path.exists(caminho_musica):
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    # --- SOM DA CHUVA ---
    som_chuva = carregar_som("assets\\sounds\\chuva.mp3")
    if som_chuva:
        som_chuva.set_volume(0.3)  
        som_chuva.play(-1)         

    som_navegar = carregar_som("assets\\sounds\\click.mp3")
    som_selecionar = carregar_som("assets\\sounds\\menu.mp3")

    # --- CARREGAMENTO DO FUNDO ---
    try:
        fundo_img = pygame.image.load("assets\\image\\Fundo Menu.png").convert()
    except Exception as e:
        print(f"Aviso: 'Fundo Menu.png' não encontrado. Usando tela preta. ({e})")
        fundo_img = pygame.Surface((800, 600))
        fundo_img.fill((0, 0, 0))

    # --- CARREGAMENTO DA TV ---
    try:
        tv_img = pygame.image.load("assets\\image\\tv_transparente.png").convert_alpha()
    except Exception as e:
        print(f"Aviso: 'tv_transparente.png' não encontrado. ({e})")
        tv_img = pygame.Surface((800, 600), pygame.SRCALPHA)

    fonte = pygame.font.SysFont('Times New Roman', 36, bold=True)
    fonte_contador = pygame.font.SysFont('Times New Roman', 22, bold=True)
    
    Cor_Branca = (230, 255, 230)
    Cor_Amarela = (255, 210, 50) 
    Cor_Sombra = (10, 30, 10)    

    opcoes = ["Iniciar", "Opções", "Sair"]
    selecionado = 0
    clock = pygame.time.Clock()
    
    finais_vistos = carregar_finais_desbloqueados()
    total_finais = 18

    scanlines_surface = None
    tamanho_anterior = (0, 0)

    # --- CONTROLE DE FADE ---
    fade_alpha = 255.0  
    fade_in_ativo = True
    fade_out_ativo = False
    acao_selecionada = None  

    while True:
        largura_tela, altura_tela = tela.get_size()
        tempo = pygame.time.get_ticks()
        
        # --- LÓGICA DE FADE ---
        if fade_in_ativo:
            fade_alpha -= 3.0 
            if fade_alpha <= 0:
                fade_alpha = 0
                fade_in_ativo = False

        if fade_out_ativo:
            fade_alpha += 0.5  
            
            volume_atual = max(0, 1.0 - (fade_alpha / 255.0))
            pygame.mixer.music.set_volume(0.4 * volume_atual)
            if som_chuva:
                som_chuva.set_volume(0.3 * volume_atual)

            if fade_alpha >= 255:
                if som_chuva: 
                    som_chuva.stop()
                
                if acao_selecionada == 0:
                    pygame.mixer.music.stop()
                    return True
                elif acao_selecionada == 1:
                    fade_out_ativo = False
                    fade_in_ativo = True 
                    pygame.mixer.music.set_volume(0.4)
                    if som_chuva: som_chuva.set_volume(0.3)
                elif acao_selecionada == 2:
                    pygame.quit()
                    sys.exit()

        # --- MATEMÁTICA DO PARALLAX ---
        onda_fundo_y = math.sin(tempo * 0.0006) * 4 + math.sin(tempo * 0.0003) * 3
        onda_fundo_x = math.cos(tempo * 0.0005) * 3 + math.cos(tempo * 0.0002) * 2

        onda_tv_y = math.sin(tempo * 0.0008) * 1.5
        onda_tv_x = math.cos(tempo * 0.0007) * 1.5
        
        # --- DESENHA O FUNDO ---
        fundo_ajustado = pygame.transform.smoothscale(fundo_img, (largura_tela + 20, altura_tela + 20))
        tela.blit(fundo_ajustado, (-10 + onda_fundo_x, -10 + onda_fundo_y))

        # --- DESENHA A TV ---
        tv_ajustada = pygame.transform.smoothscale(tv_img, (largura_tela + 20, altura_tela + 20))
        tela.blit(tv_ajustada, (-10 + onda_tv_x, -10 + onda_tv_y))

        if tamanho_anterior != (largura_tela, altura_tela):
            scanlines_surface = criar_scanlines(largura_tela, altura_tela)
            tamanho_anterior = (largura_tela, altura_tela)

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and not fade_out_ativo and not fade_in_ativo:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            
                elif event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                    if som_navegar: som_navegar.play()
                    
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                    if som_navegar: som_navegar.play()
                    
                elif event.key == pygame.K_RETURN:
                    if som_selecionar: som_selecionar.play()
                    acao_selecionada = selecionado
                    fade_out_ativo = True  

        # --- MATEMÁTICA DE POSIÇÃO DINÂMICA DO TEXTO (CENTRALIZADO À DIREITA) ---
        # Multiplicar a largura por 0.85 empurra o texto para 85% do espaço da tela (lado direito)
        centro_tv_x = int(largura_tela * 0.85) + onda_tv_x
        y_inicial_botoes = int(altura_tela * 0.26) + onda_tv_y

        # --- EFEITOS DE CRT / TV ANTIGA ---
        flicker_alpha = int(225 + (math.sin(tempo * 0.01) * 30))
        deslocamento_glitch = math.sin(tempo * 0.05) * 1.5 

        for i, texto in enumerate(opcoes):
            cor = Cor_Amarela if i == selecionado else Cor_Branca
            
            pos_x = centro_tv_x
            pos_y = y_inicial_botoes + (i * 75) 

            # Sombra
            img_sombra = fonte.render(texto, True, Cor_Sombra)
            rect_sombra = img_sombra.get_rect(center=(pos_x + 3, pos_y + 3))
            tela.blit(img_sombra, rect_sombra)

            # Aberração Cromática Vermelha
            img_red = fonte.render(texto, True, (200, 0, 0))
            img_red.set_alpha(150)
            rect_red = img_red.get_rect(center=(pos_x - 2 + deslocamento_glitch, pos_y))
            tela.blit(img_red, rect_red)

            # Aberração Cromática Azul
            img_blue = fonte.render(texto, True, (0, 100, 255))
            img_blue.set_alpha(150)
            rect_blue = img_blue.get_rect(center=(pos_x + 2 - deslocamento_glitch, pos_y))
            tela.blit(img_blue, rect_blue)

            # Texto Principal
            img_texto = fonte.render(texto, True, cor)
            img_texto.set_alpha(flicker_alpha)
            rect_texto = img_texto.get_rect(center=(pos_x, pos_y))
            tela.blit(img_texto, rect_texto)

        # --- CONTADOR DE FINAIS ---
        texto_finais = f"Finais: {len(finais_vistos)}/{total_finais}"
        pos_finais_y = int(altura_tela * 0.60) + onda_tv_y
        
        img_contador_sombra = fonte_contador.render(texto_finais, True, Cor_Sombra)
        img_contador = fonte_contador.render(texto_finais, True, Cor_Branca)
        img_contador.set_alpha(flicker_alpha)
        
        rect_finais_sombra = img_contador_sombra.get_rect(center=(centro_tv_x + 2, pos_finais_y + 2))
        rect_finais = img_contador.get_rect(center=(centro_tv_x, pos_finais_y))
        
        tela.blit(img_contador_sombra, rect_finais_sombra)
        tela.blit(img_contador, rect_finais)

        # --- LINHAS DE VARREDURA (SCANLINES) ---
        if scanlines_surface:
            tela.blit(scanlines_surface, (0, 0))

        # --- APLICA O FADE (SEMPRE POR ÚLTIMO) ---
        desenhar_fade(tela, fade_alpha)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    tela_principal = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Menu Interativo com Efeitos")
    menu(tela_principal)