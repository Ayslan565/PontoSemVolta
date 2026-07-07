import pygame
import sys
import os

def exibir_intro(tela):
    largura, altura = tela.get_size()
    fonte_texto = pygame.font.SysFont('timesnewroman', 24)
    fonte_dica = pygame.font.SysFont('timesnewroman', 16, bold=True)
    fonte_pular = pygame.font.SysFont('timesnewroman', 16, bold=True)
    
    # --- CARREGAMENTO DO SOM DE DIGITAÇÃO ---
    caminho_som = "assets\\sounds\\escrita.mp3" 
    if os.path.exists(caminho_som):
        som_digitacao = pygame.mixer.Sound(caminho_som)
        som_digitacao.set_volume(0.2) 
    else:
        som_digitacao = None

    # --- HISTÓRIA DIVIDIDA EM TELAS (SLIDES) ---
    slides = [
        [
            "Há exatas 48 horas, o Presidente da República trancou-se",
            "no Gabinete 04 e disparou um tiro contra a própria cabeça,",
            "deixando apenas uma fita cassete inaudível sobre a mesa."
        ],
        [
            "A morte dele foi a faísca no barril de pólvora.",
            "O Vice-Presidente fugiu do país na mesma madrugada.",
            "As ruas estão tomadas pelo caos, com extremistas",
            "de Esquerda e Direita em conflito aberto."
        ],
        [
            "Nenhuma ala política aceita que a outra assuma o poder.",
            "Se um general sentar na cadeira, o povo queima o país.",
            "Se um político sentar, os militares dão o golpe."
        ],
        [
            "Eles precisavam de um 'bode expiatório limpo'.",
            "Alguém que não fosse odiado por ninguém, mas que também",
            "não tivesse poder real para ameaçar as elites."
        ],
        [
            "Você era o Reitor da Universidade Nacional. Uma figura",
            "acadêmica e técnica, respeitada pelas massas por sua ética,",
            "mas considerada 'ingênua' pelas raposas da política."
        ],
        [
            "Em uma reunião tensa de madrugada, em um bunker",
            "subterrâneo iluminado por luzes fluorescentes,",
            "os generais e líderes do Congresso chegaram a um acordo."
        ],
        [
            "Eles te arrancaram da sua vida civil e te forçaram a",
            "assumir o cargo máximo sob a justificativa de",
            "'Dever Patriótico'."
        ],
        [
            "O Mandato de Sobrevivência: 365 Dias.",
            "",
            "Você não é um monarca nem um herói de guerra;",
            "você é o Presidente de Transição."
        ],
        [
            "",
            "Bem-vindo à República de Vesper."
        ]
    ]
    
    rodando = True
    slide_atual = 0
    linha_atual = 0
    indice_letra = 0
    esperando_clique = False
    
    tempo_ultima = pygame.time.get_ticks()
    velocidade_texto = 30 # Milissegundos por letra
    
    txt_pular = fonte_pular.render("[ PULAR INTRO (ESC) ]", True, (100, 100, 100))
    rect_pular = txt_pular.get_rect(topright=(largura - 20, 20))
    clock = pygame.time.Clock()

    # --- CONTROLE DO ÁUDIO INICIAL ---
    som_tocando = False
    if som_digitacao:
        # Toca em loop infinito (-1) e faz um fade in de 300ms
        som_digitacao.play(loops=-1, fade_ms=300) 
        som_tocando = True
    
    while rodando:
        tempo = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    rodando = False 
                    if som_digitacao and som_tocando:
                        som_digitacao.fadeout(500) # Fade out ao sair
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if rect_pular.collidepoint(event.pos):
                        rodando = False
                        if som_digitacao and som_tocando:
                            som_digitacao.fadeout(500) # Fade out ao pular
                        break
                    
                    if esperando_clique:
                        # AVANÇA PARA O PRÓXIMO TEXTO
                        if slide_atual < len(slides) - 1:
                            slide_atual += 1
                            linha_atual = 0
                            indice_letra = 0
                            esperando_clique = False
                            
                            # Inicia o som de digitação para o novo slide
                            if som_digitacao:
                                som_digitacao.play(loops=-1, fade_ms=300)
                                som_tocando = True
                        else:
                            rodando = False 
                            if som_digitacao and som_tocando:
                                som_digitacao.fadeout(500)
                    else:
                        # PULA A DIGITAÇÃO (Completa o texto instantaneamente)
                        linha_atual = len(slides[slide_atual])
                        esperando_clique = True
                        
                        # Para o som com fade out pois o texto já apareceu inteiro
                        if som_digitacao and som_tocando:
                            som_digitacao.fadeout(300)
                            som_tocando = False
                        
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if esperando_clique:
                    # AVANÇA PARA O PRÓXIMO TEXTO
                    if slide_atual < len(slides) - 1:
                        slide_atual += 1
                        linha_atual = 0
                        indice_letra = 0
                        esperando_clique = False
                        
                        # Inicia o som de digitação para o novo slide
                        if som_digitacao:
                            som_digitacao.play(loops=-1, fade_ms=300)
                            som_tocando = True
                    else:
                        rodando = False
                        if som_digitacao and som_tocando:
                            som_digitacao.fadeout(500)
                else:
                    # PULA A DIGITAÇÃO (Completa o texto instantaneamente)
                    linha_atual = len(slides[slide_atual])
                    esperando_clique = True
                    
                    # Para o som com fade out pois o texto já apareceu inteiro
                    if som_digitacao and som_tocando:
                        som_digitacao.fadeout(300)
                        som_tocando = False

        # --- LÓGICA DE ATUALIZAÇÃO DA DIGITAÇÃO ---
        if not esperando_clique and tempo - tempo_ultima > velocidade_texto:
            if linha_atual < len(slides[slide_atual]):
                if indice_letra < len(slides[slide_atual][linha_atual]):
                    indice_letra += 1
                else:
                    linha_atual += 1
                    indice_letra = 0
            else:
                # O TEXTO TERMINOU DE SER DIGITADO NATURALMENTE
                esperando_clique = True
                if som_digitacao and som_tocando:
                    som_digitacao.fadeout(300) # Fade out suave ao terminar de escrever
                    som_tocando = False
                    
            tempo_ultima = tempo
            
        # --- RENDERIZAÇÃO ---
        tela.fill((15, 15, 15))
        
        pos_mouse = pygame.mouse.get_pos()
        if rect_pular.collidepoint(pos_mouse):
            txt_pular_hover = fonte_pular.render("[ PULAR INTRO (ESC) ]", True, (200, 200, 200))
            tela.blit(txt_pular_hover, rect_pular)
        else:
            tela.blit(txt_pular, rect_pular)
        
        altura_total_bloco = len(slides[slide_atual]) * 35
        y_desenho = (altura // 2) - (altura_total_bloco // 2) - 20
        
        for l in range(len(slides[slide_atual])):
            texto_linha = ""
            
            if l < linha_atual:
                texto_linha = slides[slide_atual][l]
            elif l == linha_atual:
                texto_linha = slides[slide_atual][l][:indice_letra]
                
            if texto_linha:
                img = fonte_texto.render(texto_linha, True, (200, 200, 200))
                tela.blit(img, (largura // 2 - img.get_width() // 2, y_desenho))
            
            y_desenho += 35 
        
        if esperando_clique:
            if (tempo // 500) % 2 == 0:
                if slide_atual < len(slides) - 1:
                    msg = "[ CLIQUE PARA CONTINUAR ]"
                else:
                    msg = "[ CLIQUE PARA ASSUMIR O CARGO ]"
                    
                img_continue = fonte_dica.render(msg, True, (150, 40, 40))
                tela.blit(img_continue, (largura // 2 - img_continue.get_width() // 2, altura - 80))
        
        pygame.display.flip()
        clock.tick(60)

    # --- FADE OUT ANTES DE IR PARA O JOGO ---
    fade_alpha = 0.0
    velocidade_fade = 0.3 
    escurecer = pygame.Surface((largura, altura))
    escurecer.fill((0, 0, 0))
    
    while fade_alpha < 255.0:
        fade_alpha += velocidade_fade
        escurecer.set_alpha(min(int(fade_alpha), 255)) 
        tela.blit(escurecer, (0, 0))
        pygame.display.flip()
        clock.tick(60)