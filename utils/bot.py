from datetime import datetime

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from utils.find15 import percorrer
from utils.request_api import return_sequence


class IA:
    def __init__(self) -> None:
        pass

    def predict_next_number(self, data):
            # Criar uma série temporal a partir da lista de números
            data = pd.Series(data)
            
            # Treinar o modelo ARIMA
            model = ARIMA(data, order=(1, 1, 0))
            model_fit = model.fit()
            
            # Fazer a previsão do próximo número
            try:
                next_number = model_fit.predict(len(data), len(data))
                next_number = float(str(next_number).split(" ")[4][0:4])
                if next_number == 0 :
                    return "white"
                elif next_number < 8:
                    return "red"
                else:
                    return "black"
            except:
                pass
        
    def next_number(self, giros):
        next_number = self.predict_next_number(giros)

        # Imprimir o resultado
        return next_number

ia = IA()


class ReturnPrevResult:
    from bot.models import Historico, Sequencia
    def __init__(self) -> None:
        self.porcentagem = 0
        self.blaze = 19
        self.resultado = []


    def return_prev_sequence(self, last_sequence):
        if not last_sequence:
            return
        result, p5, p4, p3, p2, p1 = last_sequence

        sinais = self.Sequencia.objects.filter(
            p1=p1, p2=p2, p3=p3, p4=p4,
            p5=p5
        ).first()
        if sinais:
            self.resultado.append(sinais.result)
            print('sequence', sinais.result)
        return

        
    
    def return_prev_minute(self):
        
        now = datetime.now()
        minute= now.strftime("%M")
        historico = self.Historico.objects.filter(minute=minute)

        if historico:
            media = {'red': 0, 'black': 0, 'white': 0}

            for giro in historico:
                media[giro.color] += 1
            
            maior_valor = max(media, key=lambda x: media[x])
            self.resultado.append(maior_valor)
            print('minute', maior_valor)
        return
        
    def return_prev_number(self, last20_results):
        next_number = ia.next_number(last20_results)
        self.resultado.append(next_number)
        print('nextnumber', next_number)
        return

    def verifica_branco_com_calculo(self, last_results):
        if percorrer(last_results[15:]):
            self.resultado.append('white')
            print("Chance de branco")
        return


    def get_result(self):
        last_sequence, last_20_results = return_sequence()
        if last_20_results == None:
            return None
        prev_sequence = self.return_prev_sequence(last_sequence)
        prev_number = self.return_prev_number(last_20_results)
        prev_minute = self.return_prev_minute()
        # prev_branco_calc = self.verifica_branco_com_calculo(last_20_results[::-1])
        
        item = max(set(self.resultado), key = self.resultado.count)
        print(self.resultado)
        quantidade = [i for i in range(1, self.resultado.count(item) + 1)]
        self.porcentagem = 27 * len(quantidade)
        # quantidade = self.resultado.count(item)
        

        return [item, quantidade, self.porcentagem]
