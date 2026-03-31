import pygame
from design import *

animacao = {'nao': 0.0, 'sim': 0.0}

def arredondar_img(imagem, tamanho, raio):
    imgRedimensionada = pygame.transform.smoothscale(imagem, tamanho).convert_alpha()
    mascara = pygame.Surface(tamanho, pygame.SRCALPHA)
    pygame.draw.rect(mascara, (255, 255, 255, 255), (0, 0, *tamanho), border_radius=raio)
    imgRedimensionada.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return imgRedimensionada

def criar_elementos(tela, img_nao, img_sim, img_papel, texto_pergunta):
    global animacao
    suavidade = 0.15
    crescimento = 20

    mouse_olha = pygame.mouse.get_pos()
    largura, altura = tela.get_size()

    largura_papel = 600
    altura_papel = 120
    x_papel = (largura // 2) - (largura_papel // 2)
    y_papel = 20 
    
    img_papel_ajustada = pygame.transform.smoothscale(img_papel, (largura_papel, altura_papel))
    tela.blit(img_papel_ajustada, (x_papel, y_papel))
    
    cor_texto_pergunta = (93, 49, 36)
    fonte_pergunta = pygame.font.SysFont('Stencil', 22) 
    
    super_texto = fonte_pergunta.render(texto_pergunta, True, cor_texto_pergunta)
    rect_papel = pygame.Rect(x_papel, y_papel, largura_papel, altura_papel) 
    tela.blit(super_texto, super_texto.get_rect(center=rect_papel.center)) 
    
    largura_base = 250 
    altura_base = 150
    margem = 50
    espaco_entre_botoes = 50 
    
    y_botoes = altura - altura_base - margem 
    x_nao = (largura // 2) - (espaco_entre_botoes // 2) - largura_base 
    x_sim = (largura // 2) + (espaco_entre_botoes // 2) 
    
    escNao = pygame.Rect(x_nao, y_botoes, largura_base, altura_base)
    escSim = pygame.Rect(x_sim, y_botoes, largura_base, altura_base)

    if escNao.collidepoint(mouse_olha):
        animacao['nao'] += (crescimento - animacao['nao']) * suavidade
    else:
        animacao['nao'] += (0 - animacao['nao']) * suavidade

    tam_nao = (int(largura_base + animacao['nao']), int(altura_base + animacao['nao']))
    img_nao_final = arredondar_img(img_nao, tam_nao, 15)
    tela.blit(img_nao_final, (x_nao - (animacao['nao']/2), y_botoes - (animacao['nao']/2)))

    if escSim.collidepoint(mouse_olha):
        animacao['sim'] += (crescimento - animacao['sim']) * suavidade
    else:
        animacao['sim'] += (0 - animacao['sim']) * suavidade

    tam_sim = (int(largura_base + animacao['sim']), int(altura_base + animacao['sim']))
    img_sim_final = arredondar_img(img_sim, tam_sim, 15)
    tela.blit(img_sim_final, (x_sim - (animacao['sim']/2), y_botoes - (animacao['sim']/2)))

    return escNao, escSim

def desenhar_painel_status(tela, status_dit, mostrar_status=True):
    largura_tela, altura_tela = tela.get_size()
    
    BotaoStatus = pygame.Rect(largura_tela - 70, 20, 50, 50) 
    pygame.draw.rect(tela, (50, 50, 50), BotaoStatus, border_radius=15) 
    pygame.draw.rect(tela, (255, 255, 255), BotaoStatus, border_radius=15, width=2) 

    fonte_icone = pygame.font.SysFont('Times New Roman', 24, bold=True)
    txt_icone = fonte_icone.render('i', True, (255, 255, 255))
    tela.blit(txt_icone, txt_icone.get_rect(center=BotaoStatus.center)) 
    
    if mostrar_status:
        larg_painel = 220
        alt_painel = 400
        x_painel = largura_tela - larg_painel - 20 
        y_painel = 80 

        pygame.draw.rect(tela, (25, 25, 25), (x_painel, y_painel, larg_painel, alt_painel), border_radius=15) 

        fonte_titulo = pygame.font.SysFont('Times New Roman', 26)
        txt_titulo = fonte_titulo.render('INFORMAÇÕES', True, (255, 255, 255))
        centro_x_painel = x_painel + (larg_painel // 2)
        rect_titulo = txt_titulo.get_rect(centerx=centro_x_painel, top=y_painel + 15)
        tela.blit(txt_titulo, rect_titulo)

        atributos = [
            ('POP', 'Popularidade', (50, 200, 50)),
            ('TES', 'Tesouro', (220, 180, 50)),
            ('FOR', 'Forças Armadas', (200, 50, 50)),
            ('CON', 'Congresso', (50, 100, 200)),
            ('JUD', 'Judiciário', (200, 200, 200))
        ]

        fonte_labels = pygame.font.SysFont('Times New Roman', 16, bold=True)
        y_atual = y_painel + 60 

        for chave, nome, cor in atributos:
            valor = status_dit.get(chave, 50) 
            
            txt = fonte_labels.render(nome, True, (180, 180, 180))
            tela.blit(txt, (x_painel + 20, y_atual))
            
            largura_barra_max = 180
            altura_barra = 15
            pygame.draw.rect(tela, (60, 60, 60), (x_painel + 20, y_atual + 20, largura_barra_max, altura_barra), border_radius=5) 
            
            largura_preenchida = (valor / 100) * largura_barra_max
            if largura_preenchida > 0: 
                pygame.draw.rect(tela, cor, (x_painel + 20, y_atual + 20, int(largura_preenchida), altura_barra), border_radius=5) 
            
            y_atual += 65
            
    return BotaoStatus