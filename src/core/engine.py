import json
import pandas as pd
import os
import random 
try:
    df = pd.read_excel("data/jogo.xlsx")
    df.to_json("data/event.json", orient="records", force_ascii=False, indent=4)
    print("Arquivo JSON atualizado com sucesso!")
except Exception as e:
    print(f"Aviso: Não foi possível ler o Excel. Tentando usar o JSON existente.\n{e}")


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
        
        #f01_levante_massas
        if self.status['POP'] <= 0: return "f01_levante_massas"
        
        #f02_leilao_patria
        if self.status['TES'] <= 0: return "f02_leilao_patria"
        
        #f03_guilhotina_papel
        if self.status['CON'] <= 0: return "f03_guilhotina_papel"
        
        #f04_veredito_carcere
        if self.status['JUD'] <= 0: return "f04_veredito_carcere"
        
        #f05_revolucao_vermelha
        if self.status['AP_ESQ'] >= 1000: return "f05_revolucao_vermelha"
        
        #f06_punho_ferro
        if self.status['AP_DIR'] >= 1000: return "f06_punho_ferro"
        
        #f07_guerra_civil
        if self.status['DIP'] <= 0: return "final_diplomacia_0"
        
        #f08_estadista_centro
        if self.status['CON'] >= 1000: return "f14_cong_1000"

        #f09_populista_carismatico
        if self.status['POP'] >= 1000: return "f09_populista_carismatico"
        
        #f10_gerente_tecnocrata
        if self.status['TES'] >= 1000: return "f10_gerente_tecnocrata"
        
        #f11_marionete_internacional
        if self.status['DIP'] >= 1000: return "f11_marionete_internacional"
        
        #f12_golpe_militar
        if self.status['FOR'] <= 0: return "f12_golpe_militar"
        
        #finais inacabados
        if self.status['FOR'] >=1000: return "f13_forca_1000"
        if self.status['JUD'] >= 1000: return "f15_jud_1000"
        if self.status['AP_ESQ'] <= 0: return "f16_esquerda_0"
        if self.status['AP_DIR'] <= 0: return "f17_direita_0"
        
        if len(self.eventos) > 0:
            return "jogando"
        else:
            return "vitoria"
