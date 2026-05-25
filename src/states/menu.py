import pygame
import cv2
import sys
import os

def carregar_som(caminho):
    if os.path.exists(caminho):
        return pygame.mixer.Sound(caminho)
    else:
        print(f"Aviso: Arquivo de som não encontrado -> {caminho}")
        return None

def menu(tela):
    video = "assets\\videos\\Intro.mp4"
    cap = cv2.VideoCapture(video)
    
    largura_tela, altura_tela = tela.get_size()

    pygame.mixer.init()
    
    caminho_musica = "assets\\audio\\musica_menu.mp3"
    if os.path.exists(caminho_musica):
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    else:
        print("Aviso: Música de fundo não encontrada.")

    som_navegar = carregar_som("assets\\sounds\\escolha.mp3")
    som_selecionar = carregar_som("assets\\sounds\\resp.mp3")

    fonte = pygame.font.SysFont('Times New Roman', 42, bold=True)
    Branco = (255, 255, 255)
    Amarelo = (255, 200, 0)
    Sombra = (30, 30, 30)

    opcoes = ["Iniciar", "Opções", "Sair"]
    selecionado = 0
    clock = pygame.time.Clock()

    overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))

    while True:
        sucesso, frame = cap.read()
        if not sucesso:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            sucesso, frame = cap.read()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.transpose(frame_rgb)
        surf_video = pygame.surfarray.make_surface(frame_rgb)
        surf_video = pygame.transform.scale(surf_video, (largura_tela, altura_tela))
        
        tela.blit(surf_video, (0, 0))
        tela.blit(overlay, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                    if som_navegar: som_navegar.play()
                    
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                    if som_navegar: som_navegar.play()
                    
                elif event.key == pygame.K_RETURN:
                    if som_selecionar: som_selecionar.play()
                    
                    pygame.time.delay(300)
                    
                    if selecionado == 0:
                        cap.release()
                        pygame.mixer.music.stop()
                        return True
                    elif selecionado == 1:
                        print("Abrir menu de opções...")
                    elif selecionado == 2:
                        pygame.quit()
                        sys.exit()

        for i, texto in enumerate(opcoes):
            cor = Amarelo if i == selecionado else Branco
            
            pos_x = largura_tela // 2
            pos_y = (altura_tela // 2) + (i * 80) - 50

            img_sombra = fonte.render(texto, True, Sombra)
            rect_sombra = img_sombra.get_rect(center=(pos_x + 3, pos_y + 3))
            tela.blit(img_sombra, rect_sombra)

            img_texto = fonte.render(texto, True, cor)
            rect_texto = img_texto.get_rect(center=(pos_x, pos_y))
            tela.blit(img_texto, rect_texto)

        pygame.display.flip()
        clock.tick(30)