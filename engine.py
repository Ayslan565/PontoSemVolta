import json

import pandas as pd

df =pd.read_excel("jogo.xlsx")
df.to_json("data/event.json", orient="records", force_ascii=False, indent=4)
print("Arquivo JSON criado com sucesso!")

class Engine:
    def __init__(self):
        self.status = {
            'TES': 50, 'DIP': 50, 'FOR': 50, 
            'CON': 50, 'JUD': 50, 'AP_ESQ': 50, 'AP_DIR': 50
    }
        self.eventos = self.carregar_eventos()
        self.evento_atual = 0 

    def carregar_eventos(self):
        with open("data/event.json", "r", encoding="utf-8") as f:
            return json.load(f)
        if escolha =="sim":
            self.status['TES'] += evento['sim']['TES']
            self.status['DIP'] += evento['sim']['DIP']
            self.status['FOR'] += evento['sim']['FOR']
            self.status['CON'] += evento['sim']['CON']
            self.status['JUD'] += evento['sim']['JUD']
            self.status['AP_ESQ'] += evento['sim']['AP_ESQ']
            self.status['AP_DIR'] += evento['sim']['AP_DIR']
        elif escolha =="nao":
            self.status['TES'] += evento['nao']['TES']
            self.status['DIP'] += evento['nao']['DIP']
            self.status['FOR'] += evento['nao']['FOR']
            self.status['CON'] += evento['nao']['CON']
            self.status['JUD'] += evento['nao']['JUD']
            self.status['AP_ESQ'] += evento['nao']['AP_ESQ']
            self.status['AP_DIR'] += evento['nao']['AP_DIR']
            
        for k in self.status:
            self.status[k] = max(0, min(100, self.status[k]))
        
        self.evento_atual += 1 
