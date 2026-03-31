import pygame, cv2, sys

def menu(tela):
    video = "assets\\videos\\Intro.mp4"
    cap = cv2.VideoCapture(video)

    fonte = pygame.font.SysFont('Times New Roman', 36, bold=True)
    Branco = (255, 255, 255)
    Amarelo = (255, 255, 0)

    opcoes = ["Iniciar", "Sair"]
    selecionado = 0
    clock = pygame.time.Clock()

    while True:
        sucesso, frame = cap.read()
        
        # CORREÇÃO DO TRAVAMENTO: Se o vídeo acabar, volta para o início
        if not sucesso:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            sucesso, frame = cap.read()

        # Conversão e desenho do frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.transpose(frame_rgb)
        surf_video = pygame.surfarray.make_surface(frame_rgb)
        surf_video = pygame.transform.scale(surf_video, (800, 600))
        tela.blit(surf_video, (0, 0))

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    if selecionado == 0: 
                        cap.release() 
                        return True
                    else:
                        pygame.quit()
                        sys.exit()

        # --- DESENHO DO TEXTO (Fora do loop de eventos) ---
        for i, texto in enumerate(opcoes):
            cor = Amarelo if i == selecionado else Branco
            img_texto = fonte.render(texto, True, cor)
            rect_texto = img_texto.get_rect(center=(400, 250 + i * 100))
            tela.blit(img_texto, rect_texto)

        pygame.display.flip()
        clock.tick(30)