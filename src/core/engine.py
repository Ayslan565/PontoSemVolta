import json
import pandas as pd
import os
import random 
try:
    df = pd.read_excel("data\jogo.xlsx")
    df.to_json("data/event.json", orient="records", force_ascii=False, indent=4)
    print("Arquivo JSON atualizado com sucesso!")
except Exception as e:
    print("Aviso: Não foi possível ler o Excel. Tentando usar o JSON existente.")


class Engine:
    def __init__(self):
        self.status = {
            'POP': 250, 'TES': 250, 'DIP': 250, 'FOR': 250, 
            'CON': 250, 'JUD': 250, 'AP_ESQ': 250, 'AP_DIR': 250
        }
        self.eventos = self.carregar_eventos()

    def carregar_eventos(self):
        with open("data/event.json", "r", encoding="utf-8") as f:
            eventos_carregados = json.load(f)
            random.shuffle(eventos_carregados) 
            return eventos_carregados

    def obter_pergunta_atual(self):
        if len(self.eventos) > 0:
            return self.eventos[0].get('texto_crise', 'Erro ao ler pergunta')
        return "Fim do mandato!"

    def processar_escolha(self, escolha):
        if len(self.eventos) == 0:
            return "vitoria"

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
        if self.status['TES'] >= 1000: return "trabalho 1"
        if self.status['TES'] <= 0: return "trabalho 2"        
        if self.status['FOR'] >=1000: return "trabalho 3"
        if self.status['FOR'] <= 0: return "trabalho 4"
        
        if self.status['CON'] >= 1000: return "trabalho 5"
        if self.status['CON'] <= 0: return "trabalho 6"
        
        if self.status['JUD'] >= 1000: return "trabalho 7"
        if self.status['JUD'] <= 0: return "trabalho 8"
        
        if self.status['DIP'] >= 1000: return "trabalho 9"
        if self.status['DIP'] <= 0: return "trabalho 10"
        
        if self.status['AP_ESQ'] >= 1000: return "trabalho 11"
        if self.status['AP_ESQ'] <= 0: return "trabalho 12"
        
        if self.status['AP_DIR'] >= 1000: return "final_direita_100"
        if self.status['AP_DIR'] <= 0: return "final_direita_0"
        
        if self.status['POP'] >= 1000: return "final_popularidade_100"
        if self.status['POP'] <= 0: return "final_popularidade_0"

        if len(self.eventos) > 0:
            return "jogando"
        else:
            return "vitoria"
