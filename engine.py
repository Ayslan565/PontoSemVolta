import json
import pandas as pd
import os
import random 
try:
    df = pd.read_excel("jogo.xlsx")
    df.to_json("data/event.json", orient="records", force_ascii=False, indent=4)
    print("Arquivo JSON atualizado com sucesso!")
except Exception as e:
    print("Aviso: Não foi possível ler o Excel. Tentando usar o JSON existente.")


class Engine:
    def __init__(self):
        self.status = {
            'POP': 50, 'TES': 50, 'DIP': 50, 'FOR': 50, 
            'CON': 50, 'JUD': 50, 'AP_ESQ': 50, 'AP_DIR': 50
        }
        self.eventos = self.carregar_eventos()
        # MÁGICA: Não precisamos mais da variável self.evento_atual!

    def carregar_eventos(self):
        with open("data/event.json", "r", encoding="utf-8") as f:
            eventos_carregados = json.load(f)
            random.shuffle(eventos_carregados) 
            return eventos_carregados

    def obter_pergunta_atual(self):
        # Se ainda tem cartas no baralho, lê o texto da primeira carta (índice 0)
        if len(self.eventos) > 0:
            return self.eventos[0].get('texto_crise', 'Erro ao ler pergunta')
        return "Fim do mandato!"

    def processar_escolha(self, escolha):
        if len(self.eventos) == 0:
            return "vitoria"

        # AQUI ESTÁ A MÁGICA: .pop(0) pega a primeira carta e DELETA ela do baralho!
        evento = self.eventos.pop(0) 
        
        if escolha == "sim":
            self.status['POP'] += evento.get('sim_pop', 0)
            self.status['TES'] += evento.get('sim_tes', 0)
            self.status['CON'] += evento.get('sim_con', 0)
            self.status['FOR'] += evento.get('sim_for', 0)
            self.status['JUD'] += evento.get('sim_jud', 0)
            self.status['DIP'] += evento.get('sim_dip', 0)
            self.status['AP_ESQ'] += evento.get('sim_esq', 0)
            self.status['AP_DIR'] += evento.get('sim_dir', 0)

        elif escolha == "nao":
            self.status['POP'] += evento.get('nao_pop', 0)
            self.status['TES'] += evento.get('nao_tes', 0)
            self.status['CON'] += evento.get('nao_con', 0)
            self.status['FOR'] += evento.get('nao_for', 0)
            self.status['JUD'] += evento.get('nao_jud', 0)
            self.status['DIP'] += evento.get('nao_dip', 0)
            self.status['AP_ESQ'] += evento.get('nao_esq', 0)
            self.status['AP_DIR'] += evento.get('nao_dir', 0)
            
        for k in self.status:
            self.status[k] = max(0, min(1000, self.status[k]))
        
        return self.verificar_finais()
    
    def verificar_finais(self):
        if self.status['TES'] >= 1000: return "final_tesouro_100"
        if self.status['TES'] <= 0:   return "final_tesouro_0"
        
        if self.status['FOR'] >= 1000: return "final_forca_100"
        if self.status['FOR'] <= 0:   return "final_forca_0"
        
        if self.status['CON'] >= 1000: return "final_congresso_100"
        if self.status['CON'] <= 0:   return "final_congresso_0"
        
        if self.status['JUD'] >= 1000: return "final_judiciario_100"
        if self.status['JUD'] <= 0:   return "final_judiciario_0"
        
        if self.status['DIP'] >= 1000: return "final_diplomacia_100"
        if self.status['DIP'] <= 0:   return "final_diplomacia_0"
        
        if self.status['AP_ESQ'] >= 1000: return "final_esquerda_100"
        if self.status['AP_ESQ'] <= 0:   return "final_esquerda_0"
        
        if self.status['AP_DIR'] >= 1000: return "final_direita_100"
        if self.status['AP_DIR'] <= 0:   return "final_direita_0"
        
        if self.status['POP'] >= 1000: return "final_popularidade_100"
        if self.status['POP'] <= 0:   return "final_popularidade_0"

        # Mudamos a verificação aqui também: se a lista não está vazia, o jogo continua!
        if len(self.eventos) > 0:
            return "jogando"
        else:
            return "vitoria"