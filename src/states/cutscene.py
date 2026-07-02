import pygame
import cv2
import sys
import os

def tocar_cutscene(tela, caminho_video, caminho_audio=None):
    # Carrega o vídeo
    cap = cv2.VideoCapture(caminho_video)
    largura_tela, altura_tela = tela.get_size()
    clock = pygame.time.Clock()

    # Como o OpenCV não lê áudio, carregamos o som via Pygame (se existir)
    if caminho_audio and os.path.exists(caminho_audio):
        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0) # O 0 significa tocar apenas UMA vez

    rodando = True
    while rodando:
        sucesso, frame = cap.read()
        
        # Se o vídeo acabar (sucesso for False), encerra o loop da cutscene
        if not sucesso:
            break
            
        # Processamento de imagem do OpenCV para o Pygame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.transpose(frame_rgb)
        surf_video = pygame.surfarray.make_surface(frame_rgb)
        surf_video = pygame.transform.scale(surf_video, (largura_tela, altura_tela))
        
        tela.blit(surf_video, (0, 0))
        
        # Sistema de eventos: permite fechar o jogo ou PULAR a cutscene
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Se apertar ENTER, ESPAÇO ou ESC, pula o vídeo
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                    rodando = False 
        
        pygame.display.flip()
        
        # Ajuste o FPS (30 ou 24) dependendo de como seu vídeo foi renderizado
        clock.tick(30) 

    # Limpeza após o fim do vídeo
    cap.release()
    pygame.mixer.music.stop()