import pygame
import sys
from src.ui.design import *

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
    fonte_pergunta = pygame.font.SysFont('timesnewroman', 26, bold=True)      
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

def quebrar_texto(texto, fonte, largura_maxima):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        if fonte.size(teste_linha)[0] < largura_maxima:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    
    if linha_atual:
        linhas.append(linha_atual)
        
    return linhas

def exibir_relatorio_mensal(tela, img_fundo, img_papel, texto_historia, status_dit, mes_numero):
    largura_tela, altura_tela = tela.get_size()
    relogio = pygame.time.Clock()
    
    fundo_ajustado = pygame.transform.scale(img_fundo, (largura_tela, altura_tela))
    
    larg_papel = 850 
    alt_papel = 500  
    x_papel = (largura_tela // 2) - (larg_papel // 2)
    y_papel = (altura_tela // 2) - (alt_papel // 2)
    papel_ajustado = pygame.transform.smoothscale(img_papel, (larg_papel, alt_papel))

    fonte_titulo = pygame.font.SysFont('timesnewroman', 24, bold=True)
    fonte_historia = pygame.font.SysFont('timesnewroman', 18, bold=False)
    fonte_labels = pygame.font.SysFont('timesnewroman', 15, bold=True)
    
    linhas_completas = quebrar_texto(texto_historia, fonte_historia, 400)
    
    indice_letra = 0
    total_letras = len(texto_historia)
    animacao_concluida = False
    rodando = True
    
    tempo_ultima_letra = pygame.time.get_ticks()
    velocidade_digito = 30 
    
    atributos = [
        ('POP', 'Popularidade', (40, 110, 40)),   
        ('TES', 'Tesouro', (150, 120, 30)),       
        ('FOR', 'Forças Armadas', (120, 40, 40)), 
        ('CON', 'Congresso', (40, 70, 120)),      
        ('JUD', 'Judiciário', (100, 100, 100)),   
        ('DIP', 'Diplomacia', (100, 50, 100)),    
        ('AP_ESQ', 'Esquerda', (140, 50, 50)),    
        ('AP_DIR', 'Direita', (50, 60, 130))      
    ]
    
    # ---------------------------------------------------------
    # VARIÁVEL DE CONTROLE DA ANIMAÇÃO DAS BARRAS
    # ---------------------------------------------------------
    valores_animados = {chave: 0.0 for chave, _, _ in atributos}
    suavidade_barras = 0.05
    
    while rodando:
        tempo_atual = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_RETURN:
                    if not animacao_concluida:
                        indice_letra = total_letras
                        animacao_concluida = True
                        # Ao pular a animação, preenche as barras imediatamente
                        for chave in valores_animados:
                            valores_animados[chave] = float(status_dit.get(chave, 50))
                    else:
                        rodando = False

        if not animacao_concluida and tempo_atual - tempo_ultima_letra > velocidade_digito:
            if indice_letra < total_letras:
                indice_letra += 1
                tempo_ultima_letra = tempo_atual
            else:
                animacao_concluida = True

        # Inicia a animação de preenchimento quando um terço do texto já foi digitado
        if indice_letra > total_letras // 3:
            for chave, _, _ in atributos:
                alvo = status_dit.get(chave, 50)
                valores_animados[chave] += (alvo - valores_animados[chave]) * suavidade_barras

        tela.blit(fundo_ajustado, (0, 0))
        tela.blit(papel_ajustado, (x_papel, y_papel))
        
        titulo = f"PROTOCOLO: RELATÓRIO DE SOBREVIVÊNCIA - MÊS {mes_numero}"
        txt_titulo = fonte_titulo.render(titulo, True, (100, 30, 30)) 
        tela.blit(txt_titulo, (x_papel + 50, y_papel + 50))
        
        letras_desenhadas = 0
        y_linha = y_papel + 110
        
        for linha in linhas_completas:
            tamanho_linha = len(linha)
            
            if letras_desenhadas + tamanho_linha <= indice_letra:
                texto_para_renderizar = linha
                letras_desenhadas += tamanho_linha
            else:
                letras_restantes = indice_letra - letras_desenhadas
                if letras_restantes > 0:
                    texto_para_renderizar = linha[:letras_restantes]
                    letras_desenhadas += letras_restantes
                else:
                    texto_para_renderizar = ""
            
            if texto_para_renderizar:
                img_texto = fonte_historia.render(texto_para_renderizar, True, (30, 30, 30))
                tela.blit(img_texto, (x_papel + 50, y_linha))
                
            y_linha += (fonte_historia.get_linesize() + 3)
            
        x_status = x_papel + 520
        y_inicial_status = y_papel + 110
        largura_barra_max = 240 
        altura_barra = 14
        tamanho_ponta = 10 
        
        for i, (chave, nome, cor) in enumerate(atributos):
            valor_atual = valores_animados[chave]
            y_atual = y_inicial_status + (i * 42)
            
            txt_label = fonte_labels.render(nome, True, (40, 40, 40))
            tela.blit(txt_label, (x_status, y_atual - 15))
            
            x_fim_fundo = x_status + largura_barra_max
            pontos_fundo = [
                (x_status, y_atual + 5), 
                (x_fim_fundo, y_atual + 5), 
                (x_fim_fundo + tamanho_ponta, y_atual + 5 + (altura_barra / 2)), 
                (x_fim_fundo, y_atual + 5 + altura_barra),
                (x_status, y_atual + 5 + altura_barra)
            ]
            pygame.draw.polygon(tela, (160, 160, 160), pontos_fundo) 
            
            # ---------------------------------------------------------
            # DESENHO DA BARRA ANIMADA
            # ---------------------------------------------------------
            if valor_atual > 0.5: # Evita desenhar se for menor que meio pixel
                largura_preenchida = (valor_atual / 1000) * largura_barra_max
                x_fim_preenchido = x_status + largura_preenchida
                
                pontos_preenchidos = [
                    (x_status, y_atual + 5), 
                    (x_fim_preenchido, y_atual + 5), 
                    (x_fim_preenchido + tamanho_ponta, y_atual + 5 + (altura_barra / 2)), 
                    (x_fim_preenchido, y_atual + 5 + altura_barra),
                    (x_status, y_atual + 5 + altura_barra)
                ]
                pygame.draw.polygon(tela, cor, pontos_preenchidos)

        if animacao_concluida:
            if (tempo_atual // 500) % 2 == 0: 
                txt_rodape = fonte_labels.render("[ PRESSIONE ENTER PARA ARQUIVAR ]", True, (50, 50, 50))
                tela.blit(txt_rodape, (x_papel + 280, y_papel + alt_papel - 40))

        pygame.display.flip()
        relogio.tick(60)