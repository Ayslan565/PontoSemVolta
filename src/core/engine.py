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
        
        # Sistema de Calendário de 1 Ano (365 Dias)
        self.mes_atual = 1
        self.perguntas_respondidas_mes = 0
        self.meta_perguntas_mes = random.randint(10, 15)
        
        # Histórias de encerramento de cada mês
        self.historias_mes = {
            1: "MÊS 1: O choque inicial passou. As ruas ainda queimam com os protestos, mas o governo de transição não caiu. Os generais recolheram os tanques, mas observam suas decisões de perto.",
            2: "MÊS 2: O inverno rigoroso de Vesper se aproxima. O Tesouro sangra mais rápido do que o esperado devido à inflação. As sombras do seu antecessor ainda assombram os corredores do Gabinete 04.",
            3: "MÊS 3: Um quarto do mandato se foi. Facções que antes te ignoravam por acharem que você era apenas uma marionete inofensiva agora tentam comprar seu apoio ou ameaçar sua vida.",
            4: "MÊS 4: Protestos isolados no polo industrial exigem sua renúncia. O Congresso tenta aprovar leis secretas de anistia enquanto você está distraído apagando incêndios menores.",
            5: "MÊS 5: Os cofres públicos estão no limite. Você precisou cortar verbas essenciais de manutenção urbana. O povo sente a fome e o frio, e a miséria sempre gera fúria.",
            6: "MÊS 6: Metade do caminho. Um atentado a bomba foi frustrado nos arredores do Palácio. O serviço de inteligência omitiu o relatório. Ninguém sabe se foi a Esquerda ou a Direita.",
            7: "MÊS 7: A mídia internacional começou a cobrir a crise interna. Embaixadores de nações vizinhas fazem exigências absurdas de recursos em troca de apoio diplomático.",
            8: "MÊS 8: Generais da velha guarda fizeram uma reunião a portas fechadas. O barulho de coturnos ecoa mais forte. O Ministério da Defesa afirma que um golpe é iminente se você falhar.",
            9: "MÊS 9: O Judiciário tenta cassar seus poderes de emergência alegando inconstitucionalidade. A burocracia está te sufocando. Você está governando quase que inteiramente por decretos.",
            10: "MÊS 10: O outono traz ventos frios, cortes de energia e paranoia. Os telefones estão grampeados. Seus próprios conselheiros param de olhar nos seus olhos nas reuniões.",
            11: "MÊS 11: Faltam poucas semanas para as eleições gerais. As ruas estão estranhamente silenciosas. É o silêncio que antecede a explosão de uma guerra civil ou a paz definitiva?",
            12: "MÊS 12: O último mês. A poeira está baixando e os candidatos estão nas ruas. Sobreviva a estas últimas decisões e Vesper terá um amanhã. Não cometa erros agora."
        }

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
            
        estado_final = self.verificar_finais()
        if estado_final != "jogando":
            return estado_final
            
        # Lógica de progressão de meses
        self.perguntas_respondidas_mes += 1
        
        if self.perguntas_respondidas_mes >= self.meta_perguntas_mes:
            self.mes_atual += 1
            self.perguntas_respondidas_mes = 0 
            
            if self.mes_atual > 12:
                return "vitoria" 
                
            self.meta_perguntas_mes = random.randint(10, 15) 
            return "fim_mes" 

        return "jogando"

    def obter_texto_mes(self):
        mes_concluido = self.mes_atual - 1 
        return self.historias_mes.get(mes_concluido, "O silêncio ecoa pelos corredores do poder...")

    def verificar_finais(self):
        if self.status['POP'] <= 0: return "f01_levante_massas"
        if self.status['TES'] <= 0: return "f02_leilao_patria"
        if self.status['CON'] <= 0: return "f03_guilhotina_papel"
        if self.status['JUD'] <= 0: return "f04_veredito_carcere"
        if self.status['AP_ESQ'] >= 1000: return "f05_revolucao_vermelha"
        if self.status['AP_DIR'] >= 1000: return "f06_punho_ferro"
        if self.status['DIP'] <= 0: return "f07_guerra_civil"
        if self.status['CON'] >= 1000: return "f08_estadista_centro"
        if self.status['POP'] >= 1000: return "f09_populista_carismatico"
        if self.status['TES'] >= 1000: return "f10_gerente_tecnocrata"
        if self.status['DIP'] >= 1000: return "f11_marionete_internacional"
        if self.status['FOR'] <= 0: return "f12_golpe_militar"
        if self.status['FOR'] >= 1000: return "f13_forca_1000"
        if self.status['JUD'] >= 1000: return "f14_jud_1000"
        if self.status['AP_ESQ'] <= 0: return "f15_esquerda_0"
        if self.status['AP_DIR'] <= 0: return "f16_direita_0"
        
        if len(self.eventos) > 0:
            return "jogando"
        else:
            return "vitoria"