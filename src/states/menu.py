import pygame
import sys
import os
import json
import math

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

def carregar_config():
    caminho = "data\\config.json"
    if os.path.exists(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"vol_musica": 0.4, "vol_ambiente": 0.3}

def salvar_config(vol_musica, vol_ambiente):
    caminho = "data\\config.json"
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump({"vol_musica": vol_musica, "vol_ambiente": vol_ambiente}, f, indent=4)

def criar_scanlines(largura, altura):
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for y in range(0, altura, 3):
        pygame.draw.line(surf, (0, 0, 0, 30), (0, y), (largura, y))
    return surf

def desenhar_fade(tela, alpha):
    if alpha > 0:
        surf_fade = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        surf_fade.fill((0, 0, 0, min(max(int(alpha), 0), 255)))
        tela.blit(surf_fade, (0, 0))

def atualizar_volumes_sons(som_chuva, som_navegar, som_selecionar, vol_ambiente):
    if som_chuva: som_chuva.set_volume(vol_ambiente)
    if som_navegar: som_navegar.set_volume(vol_ambiente)
    if som_selecionar: som_selecionar.set_volume(vol_ambiente)

def menu_opcoes_jogo(tela):
    config = carregar_config()
    vol_musica = config.get("vol_musica", 0.4)
    vol_ambiente = config.get("vol_ambiente", 0.3)
    som_navegar = carregar_som("assets\\sounds\\click.mp3")
    som_selecionar = carregar_som("assets\\sounds\\menu.mp3")
    atualizar_volumes_sons(None, som_navegar, som_selecionar, vol_ambiente)
    fonte = pygame.font.SysFont('timesnewroman', 36, bold=True)
    selecionado = 0
    rodando = True
    overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    
    while rodando:
        largura_tela, altura_tela = tela.get_size()
        centro_x = largura_tela // 2
        y_inicial = altura_tela // 2 - 50
        
        textos = [
            f"< Música: {int(vol_musica * 100)}% >",
            f"< Ambiente: {int(vol_ambiente * 100)}% >",
            "Voltar ao Jogo"
        ]
        
        rects_botoes = []
        for i, txt in enumerate(textos):
            img_temp = fonte.render(txt, True, (255, 255, 255))
            rects_botoes.append(img_temp.get_rect(center=(centro_x, y_inicial + i * 60)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salvar_config(vol_musica, vol_ambiente)
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(rects_botoes):
                    if rect.collidepoint(event.pos):
                        if selecionado != i:
                            selecionado = i
                            if som_navegar: som_navegar.play()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects_botoes):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            if event.pos[0] < centro_x:
                                vol_musica = round(max(0.0, vol_musica - 0.1), 1)
                            else:
                                vol_musica = round(min(1.0, vol_musica + 0.1), 1)
                            pygame.mixer.music.set_volume(vol_musica)
                            if som_navegar: som_navegar.play()
                        elif i == 1:
                            if event.pos[0] < centro_x:
                                vol_ambiente = round(max(0.0, vol_ambiente - 0.1), 1)
                            else:
                                vol_ambiente = round(min(1.0, vol_ambiente + 0.1), 1)
                            atualizar_volumes_sons(None, som_navegar, som_selecionar, vol_ambiente)
                            if som_navegar: som_navegar.play()
                        elif i == 2:
                            if som_selecionar: som_selecionar.play()
                            salvar_config(vol_musica, vol_ambiente)
                            rodando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(textos)
                    if som_navegar: som_navegar.play()
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(textos)
                    if som_navegar: som_navegar.play()
                elif event.key == pygame.K_LEFT:
                    if selecionado == 0:
                        vol_musica = round(max(0.0, vol_musica - 0.1), 1)
                        pygame.mixer.music.set_volume(vol_musica)
                        if som_navegar: som_navegar.play()
                    elif selecionado == 1:
                        vol_ambiente = round(max(0.0, vol_ambiente - 0.1), 1)
                        atualizar_volumes_sons(None, som_navegar, som_selecionar, vol_ambiente)
                        if som_navegar: som_navegar.play()
                elif event.key == pygame.K_RIGHT:
                    if selecionado == 0:
                        vol_musica = round(min(1.0, vol_musica + 0.1), 1)
                        pygame.mixer.music.set_volume(vol_musica)
                        if som_navegar: som_navegar.play()
                    elif selecionado == 1:
                        vol_ambiente = round(min(1.0, vol_ambiente + 0.1), 1)
                        atualizar_volumes_sons(None, som_navegar, som_selecionar, vol_ambiente)
                        if som_navegar: som_navegar.play()
                elif event.key == pygame.K_RETURN:
                    if selecionado == 2:
                        if som_selecionar: som_selecionar.play()
                        salvar_config(vol_musica, vol_ambiente)
                        rodando = False
                    else:
                        if som_navegar: som_navegar.play()
                        
        tela.blit(overlay, (0, 0))
        for i, txt in enumerate(textos):
            cor = (255, 210, 50) if i == selecionado else (230, 255, 230)
            img = fonte.render(txt, True, cor)
            rect = img.get_rect(center=(centro_x, y_inicial + i * 60))
            tela.blit(img, rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def menu(tela):
    pygame.mixer.init()
    config = carregar_config()
    vol_musica = config.get("vol_musica", 0.4)
    vol_ambiente = config.get("vol_ambiente", 0.3)
    
    caminho_musica = "assets\\sounds\\musica_menu.mp3"
    if os.path.exists(caminho_musica):
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(vol_musica)
        pygame.mixer.music.play(-1)
        
    som_chuva = carregar_som("assets\\sounds\\chuva.mp3")
    if som_chuva:
        som_chuva.set_volume(vol_ambiente)
        som_chuva.play(-1)
        
    som_navegar = carregar_som("assets\\sounds\\click.mp3")
    som_selecionar = carregar_som("assets\\sounds\\menu.mp3")
    
    # Carregando o som do tiro
    som_tiro = carregar_som("assets\\sounds\\tiro.mp3")
    if som_tiro:
        som_tiro.set_volume(0.8) 
        
    atualizar_volumes_sons(som_chuva, som_navegar, som_selecionar, vol_ambiente)
    
    try:
        fundo_img = pygame.image.load("assets\\image\\Fundo Menu.png").convert()
    except Exception:
        fundo_img = pygame.Surface((800, 600))
        fundo_img.fill((0, 0, 0))
        
    try:
        tv_img = pygame.image.load("assets\\image\\tv_transparente.png").convert_alpha()
    except Exception:
        tv_img = pygame.Surface((800, 600), pygame.SRCALPHA)
        
    fonte = pygame.font.SysFont('timesnewroman', 36, bold=True)
    fonte_contador = pygame.font.SysFont('timesnewroman', 22, bold=True)
    Cor_Branca = (230, 255, 230)
    Cor_Amarela = (255, 210, 50)
    Cor_Sombra = (10, 30, 10)
    
    estado_tela = "PRINCIPAL"
    selecionado = 0
    clock = pygame.time.Clock()
    finais_vistos = carregar_finais_desbloqueados()
    total_finais = 18
    scanlines_surface = None
    tamanho_anterior = (0, 0)
    
    fade_alpha = 255.0
    fade_in_ativo = True
    fade_out_ativo = False
    acao_pendente = None
    
    velocidade_fade_in = 3.0
    velocidade_fade_out = 0.5 
    
    while True:
        largura_tela, altura_tela = tela.get_size()
        tempo = pygame.time.get_ticks()
        
        onda_tv_y = math.sin(tempo * 0.0008) * 1.5
        onda_tv_x = math.cos(tempo * 0.0007) * 1.5
        centro_tv_x = int(largura_tela * 0.75) + onda_tv_x
        y_inicial_botoes = int(altura_tela * 0.26) + onda_tv_y
        
        if estado_tela == "PRINCIPAL":
            textos_exibicao = ["Iniciar", "Opções", "Sair"]
        else:
            textos_exibicao = [
                f"< Música: {int(vol_musica * 100)}% >",
                f"< Ambiente: {int(vol_ambiente * 100)}% >",
                "Voltar"
            ]
            
        rects_botoes = []
        for i, texto in enumerate(textos_exibicao):
            img_temp = fonte.render(texto, True, (255, 255, 255))
            rects_botoes.append(img_temp.get_rect(center=(centro_tv_x, y_inicial_botoes + (i * 75))))
            
        if fade_in_ativo:
            fade_alpha -= velocidade_fade_in
            if fade_alpha <= 0:
                fade_alpha = 0
                fade_in_ativo = False
                
        if fade_out_ativo:
            fade_alpha += velocidade_fade_out
            proporcao_volume = max(0, 1.0 - (fade_alpha / 255.0))
            pygame.mixer.music.set_volume(vol_musica * proporcao_volume)
            if som_chuva:
                som_chuva.set_volume(vol_ambiente * proporcao_volume)
                
            # Verifica se o fade_out terminou (tela totalmente preta)
            if fade_alpha >= 255:
                if acao_pendente == "INICIAR":
                    if som_chuva: som_chuva.stop()
                    pygame.mixer.music.stop()
                    
                    # Toca o som do tiro apenas quando a tela escurece totalmente
                    if som_tiro: som_tiro.play()
                    
                    # Atualiza a tela para preto total e congela por 1.5 segundos
                    desenhar_fade(tela, 255)
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    
                    salvar_config(vol_musica, vol_ambiente)
                    return True
                    
                elif acao_pendente == "SAIR":
                    salvar_config(vol_musica, vol_ambiente)
                    pygame.quit()
                    sys.exit()
                elif acao_pendente == "IR_OPCOES":
                    estado_tela = "OPCOES"
                    selecionado = 0
                    fade_out_ativo = False
                    fade_in_ativo = True
                    velocidade_fade_in = 15.0
                    pygame.mixer.music.set_volume(vol_musica)
                    if som_chuva: som_chuva.set_volume(vol_ambiente)
                elif acao_pendente == "VOLTAR_PRINCIPAL":
                    salvar_config(vol_musica, vol_ambiente)
                    estado_tela = "PRINCIPAL"
                    selecionado = 0
                    fade_out_ativo = False
                    fade_in_ativo = True
                    velocidade_fade_in = 15.0
                    pygame.mixer.music.set_volume(vol_musica)
                    if som_chuva: som_chuva.set_volume(vol_ambiente)
                    
        onda_fundo_y = math.sin(tempo * 0.0006) * 4 + math.sin(tempo * 0.0003) * 3
        onda_fundo_x = math.cos(tempo * 0.0005) * 3 + math.cos(tempo * 0.0002) * 2
        
        fundo_ajustado = pygame.transform.smoothscale(fundo_img, (largura_tela + 20, altura_tela + 20))
        tela.blit(fundo_ajustado, (-10 + onda_fundo_x, -10 + onda_fundo_y))
        tv_ajustada = pygame.transform.smoothscale(tv_img, (largura_tela + 20, altura_tela + 20))
        tela.blit(tv_ajustada, (-10 + onda_tv_x, -10 + onda_tv_y))
        
        if tamanho_anterior != (largura_tela, altura_tela):
            scanlines_surface = criar_scanlines(largura_tela, altura_tela)
            tamanho_anterior = (largura_tela, altura_tela)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salvar_config(vol_musica, vol_ambiente)
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION and not fade_out_ativo and not fade_in_ativo:
                for i, rect in enumerate(rects_botoes):
                    if rect.collidepoint(event.pos):
                        if selecionado != i:
                            selecionado = i
                            if som_navegar: som_navegar.play()
                            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not fade_out_ativo and not fade_in_ativo:
                for i, rect in enumerate(rects_botoes):
                    if rect.collidepoint(event.pos):
                        if estado_tela == "PRINCIPAL":
                            if som_selecionar: som_selecionar.play()
                            fade_out_ativo = True
                            if i == 0: 
                                acao_pendente = "INICIAR"
                                velocidade_fade_out = 0.5 
                            elif i == 1: 
                                acao_pendente = "IR_OPCOES"
                                velocidade_fade_out = 15.0 
                            elif i == 2: 
                                acao_pendente = "SAIR"
                                velocidade_fade_out = 15.0 
                                
                        elif estado_tela == "OPCOES":
                            if i == 2:
                                if som_selecionar: som_selecionar.play()
                                fade_out_ativo = True
                                acao_pendente = "VOLTAR_PRINCIPAL"
                                velocidade_fade_out = 15.0 
                            elif i == 0:
                                if event.pos[0] < centro_tv_x:
                                    vol_musica = round(max(0.0, vol_musica - 0.1), 1)
                                else:
                                    vol_musica = round(min(1.0, vol_musica + 0.1), 1)
                                pygame.mixer.music.set_volume(vol_musica)
                                if som_navegar: som_navegar.play()
                            elif i == 1:
                                if event.pos[0] < centro_tv_x:
                                    vol_ambiente = round(max(0.0, vol_ambiente - 0.1), 1)
                                else:
                                    vol_ambiente = round(min(1.0, vol_ambiente + 0.1), 1)
                                atualizar_volumes_sons(som_chuva, som_navegar, som_selecionar, vol_ambiente)
                                if som_navegar: som_navegar.play()
                                
            if event.type == pygame.KEYDOWN and not fade_out_ativo and not fade_in_ativo:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(textos_exibicao)
                    if som_navegar: som_navegar.play()
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(textos_exibicao)
                    if som_navegar: som_navegar.play()
                elif event.key == pygame.K_LEFT and estado_tela == "OPCOES":
                    if selecionado == 0:
                        vol_musica = round(max(0.0, vol_musica - 0.1), 1)
                        pygame.mixer.music.set_volume(vol_musica)
                        if som_navegar: som_navegar.play()
                    elif selecionado == 1:
                        vol_ambiente = round(max(0.0, vol_ambiente - 0.1), 1)
                        atualizar_volumes_sons(som_chuva, som_navegar, som_selecionar, vol_ambiente)
                        if som_navegar: som_navegar.play()
                elif event.key == pygame.K_RIGHT and estado_tela == "OPCOES":
                    if selecionado == 0:
                        vol_musica = round(min(1.0, vol_musica + 0.1), 1)
                        pygame.mixer.music.set_volume(vol_musica)
                        if som_navegar: som_navegar.play()
                    elif selecionado == 1:
                        vol_ambiente = round(min(1.0, vol_ambiente + 0.1), 1)
                        atualizar_volumes_sons(som_chuva, som_navegar, som_selecionar, vol_ambiente)
                        if som_navegar: som_navegar.play()
                elif event.key == pygame.K_RETURN:
                    if estado_tela == "PRINCIPAL":
                        if som_selecionar: som_selecionar.play()
                        fade_out_ativo = True
                        if selecionado == 0: 
                            acao_pendente = "INICIAR"
                            velocidade_fade_out = 0.5 
                        elif selecionado == 1: 
                            acao_pendente = "IR_OPCOES"
                            velocidade_fade_out = 15.0 
                        elif selecionado == 2: 
                            acao_pendente = "SAIR"
                            velocidade_fade_out = 15.0 
                    elif estado_tela == "OPCOES":
                        if selecionado == 2:
                            if som_selecionar: som_selecionar.play()
                            fade_out_ativo = True
                            acao_pendente = "VOLTAR_PRINCIPAL"
                            velocidade_fade_out = 15.0 
                        else:
                            if som_navegar: som_navegar.play()
                            
        flicker_alpha = int(225 + (math.sin(tempo * 0.01) * 30))
        deslocamento_glitch = math.sin(tempo * 0.05) * 1.5
        
        for i, texto in enumerate(textos_exibicao):
            cor = Cor_Amarela if i == selecionado else Cor_Branca
            pos_x = centro_tv_x
            pos_y = y_inicial_botoes + (i * 75)
            
            img_sombra = fonte.render(texto, True, Cor_Sombra)
            rect_sombra = img_sombra.get_rect(center=(pos_x + 3, pos_y + 3))
            tela.blit(img_sombra, rect_sombra)
            
            img_red = fonte.render(texto, True, (200, 0, 0))
            img_red.set_alpha(150)
            rect_red = img_red.get_rect(center=(pos_x - 2 + deslocamento_glitch, pos_y))
            tela.blit(img_red, rect_red)
            
            img_blue = fonte.render(texto, True, (0, 100, 255))
            img_blue.set_alpha(150)
            rect_blue = img_blue.get_rect(center=(pos_x + 2 - deslocamento_glitch, pos_y))
            tela.blit(img_blue, rect_blue)
            
            img_texto = fonte.render(texto, True, cor)
            img_texto.set_alpha(flicker_alpha)
            rect_texto = img_texto.get_rect(center=(pos_x, pos_y))
            tela.blit(img_texto, rect_texto)
            
        if estado_tela == "PRINCIPAL":
            texto_finais = f"Finais: {len(finais_vistos)}/{total_finais}"
            pos_finais_y = int(altura_tela * 0.60) + onda_tv_y
            img_contador_sombra = fonte_contador.render(texto_finais, True, Cor_Sombra)
            img_contador = fonte_contador.render(texto_finais, True, Cor_Branca)
            img_contador.set_alpha(flicker_alpha)
            rect_finais_sombra = img_contador_sombra.get_rect(center=(centro_tv_x + 2, pos_finais_y + 2))
            rect_finais = img_contador.get_rect(center=(centro_tv_x, pos_finais_y))
            tela.blit(img_contador_sombra, rect_finais_sombra)
            tela.blit(img_contador, rect_finais)
            
        if scanlines_surface:
            tela.blit(scanlines_surface, (0, 0))
            
        desenhar_fade(tela, fade_alpha)
        pygame.display.flip()
        clock.tick(60)