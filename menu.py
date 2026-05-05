import pygame
import cv2
import sys
import os

def carregar_som(caminho):
    """Função auxiliar para carregar sons sem travar o jogo se o arquivo não existir."""
    if os.path.exists(caminho):
        return pygame.mixer.Sound(caminho)
    else:
        print(f"Aviso: Arquivo de som não encontrado -> {caminho}")
        return None

def menu(tela):
    # --- CONFIGURAÇÃO DE VÍDEO ---
    video = "assets\\videos\\Intro.mp4"
    cap = cv2.VideoCapture(video)
    
    # Pega o tamanho atual da tela para não usar números fixos
    largura_tela, altura_tela = tela.get_size()

    # --- CONFIGURAÇÃO DE ÁUDIO ---
    pygame.mixer.init()
    
    # Música de fundo (Loop)
    caminho_musica = "assets\\audio\\musica_menu.mp3"
    if os.path.exists(caminho_musica):
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.4) # Volume entre 0.0 e 1.0
        pygame.mixer.music.play(-1) # -1 faz a música repetir infinitamente
    else:
        print("Aviso: Música de fundo não encontrada.")

    # Efeitos sonoros
    som_navegar = carregar_som("assets\\sounds\\escolha.mp3")
    som_selecionar = carregar_som("assets\\sounds\\resp.mp3")

    # --- CONFIGURAÇÃO VISUAL ---
    fonte = pygame.font.SysFont('Times New Roman', 42, bold=True)
    Branco = (255, 255, 255)
    Amarelo = (255, 200, 0)
    Sombra = (30, 30, 30)

    opcoes = ["Iniciar", "Opções", "Sair"] # Adicionei mais uma opção de exemplo
    selecionado = 0
    clock = pygame.time.Clock()

    # Camada escura semitransparente para melhorar a leitura do texto
    overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120)) # O último número (120) é a transparência (0-255)

    while True:
        # --- ATUALIZAÇÃO DO VÍDEO ---
        sucesso, frame = cap.read()
        if not sucesso:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            sucesso, frame = cap.read()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.transpose(frame_rgb)
        surf_video = pygame.surfarray.make_surface(frame_rgb)
        surf_video = pygame.transform.scale(surf_video, (largura_tela, altura_tela))
        
        # Desenha o vídeo e a camada escura por cima
        tela.blit(surf_video, (0, 0))
        tela.blit(overlay, (0, 0))

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                    if som_navegar: som_navegar.play() # Toca som ao mover
                    
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                    if som_navegar: som_navegar.play() # Toca som ao mover
                    
                elif event.key == pygame.K_RETURN:
                    if som_selecionar: som_selecionar.play() # Toca som ao confirmar
                    
                    # Pequeno delay para o som tocar antes de mudar de tela/fechar
                    pygame.time.delay(300) 
                    
                    if selecionado == 0: # Iniciar
                        cap.release()
                        pygame.mixer.music.stop() # Para a música do menu
                        return True
                    elif selecionado == 1: # Opções
                        print("Abrir menu de opções...") # Placeholder
                    elif selecionado == 2: # Sair
                        pygame.quit()
                        sys.exit()

        # --- DESENHO DO TEXTO COM SOMBRA ---
        for i, texto in enumerate(opcoes):
            cor = Amarelo if i == selecionado else Branco
            
            # Posição baseada no centro da tela
            pos_x = largura_tela // 2
            pos_y = (altura_tela // 2) + (i * 80) - 50 # Espaçamento dinâmico

            # Renderiza a sombra (deslocada levemente para a direita e para baixo)
            img_sombra = fonte.render(texto, True, Sombra)
            rect_sombra = img_sombra.get_rect(center=(pos_x + 3, pos_y + 3))
            tela.blit(img_sombra, rect_sombra)

            # Renderiza o texto principal
            img_texto = fonte.render(texto, True, cor)
            rect_texto = img_texto.get_rect(center=(pos_x, pos_y))
            tela.blit(img_texto, rect_texto)

        pygame.display.flip()
        clock.tick(30)