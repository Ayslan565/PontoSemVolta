import pygame
from design import *

animacao = {'nao': 0.0, 'sim': 0.0}

def arredondar_img(imagem, tamanho, raio):
    imgRedimensionada = pygame.transform.smoothscale(imagem, tamanho).convert_alpha()
    mascara = pygame.Surface(tamanho, pygame.SRCALPHA)
    pygame.draw.rect(mascara, (255, 255, 255, 255), (0, 0, *tamanho), border_radius=raio)
    imgRedimensionada.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return imgRedimensionada

# ATENÇÃO: A função agora pede 5 informações!
def criar_elementos(tela, img_nao, img_sim, img_papel, texto_pergunta):
    global animacao
    suavidade = 0.15
    crescimento = 20

    mouse_olha = pygame.mouse.get_pos()
    largura, altura = tela.get_size()

    # =======================================================
    # 1. O PAPEL E A PERGUNTA
    # =======================================================
    largura_papel = 600
    altura_papel = 120
    x_papel = (largura // 2) - (largura_papel // 2)
    y_papel = 20 
    
    img_papel_ajustada = pygame.transform.smoothscale(img_papel, (largura_papel, altura_papel))
    tela.blit(img_papel_ajustada, (x_papel, y_papel))
    
    cor_texto_pergunta = (93, 49, 36) # Vermelho escuro
    fonte_pergunta = pygame.font.SysFont('Stencil', 22) 
    
    super_texto = fonte_pergunta.render(texto_pergunta, True, cor_texto_pergunta)
    rect_papel = pygame.Rect(x_papel, y_papel, largura_papel, altura_papel)
    tela.blit(super_texto, super_texto.get_rect(center=rect_papel.center))

    # =======================================================
    # 2. OS BOTÕES ANIMADOS
    # =======================================================
    largura_base = 250 # Voltei para o tamanho maior do seu print!
    altura_base = 150
    margem = 50
    espaco_entre_botoes = 50 
    y_botoes = altura - altura_base - margem

    fonte = pygame.font.SysFont('Arial', 36, bold=True) 

    x_nao = (largura // 2) - (espaco_entre_botoes // 2) - largura_base
    x_sim = (largura // 2) + (espaco_entre_botoes // 2)
    
    escNao = pygame.Rect(x_nao, y_botoes, largura_base, altura_base)
    escSim = pygame.Rect(x_sim, y_botoes, largura_base, altura_base)

    # --- Lógica botão NÃO ---
    if escNao.collidepoint(mouse_olha):
        animacao['nao'] += (crescimento - animacao['nao']) * suavidade
    else:
        animacao['nao'] += (0 - animacao['nao']) * suavidade

    tam_nao = (int(largura_base + animacao['nao']), int(altura_base + animacao['nao']))
    img_nao_final = arredondar_img(img_nao, tam_nao, 15)
    tela.blit(img_nao_final, (x_nao - (animacao['nao']/2), y_botoes - (animacao['nao']/2)))



    # --- Lógica botão SIM ---
    if escSim.collidepoint(mouse_olha):
        animacao['sim'] += (crescimento - animacao['sim']) * suavidade
    else:
        animacao['sim'] += (0 - animacao['sim']) * suavidade

    tam_sim = (int(largura_base + animacao['sim']), int(altura_base + animacao['sim']))
    img_sim_final = arredondar_img(img_sim, tam_sim, 15)
    tela.blit(img_sim_final, (x_sim - (animacao['sim']/2), y_botoes - (animacao['sim']/2)))



    # GARANTINDO O RETORNO PARA O MAIN.PY
    return escNao, escSim