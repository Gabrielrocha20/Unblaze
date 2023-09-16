import requests


def enviar_msg_telegram(chave, chat_id, cor, porcentagem):
    cor = cor.replace('red', '🔴') \
                .replace('black', '⚫') \
                .replace('white', '⚪')
    msg = f"""
        Chance de ser {cor}
        {porcentagem}% de ser {cor}
        Com proteção no ⚪

        Sequencia: 
        Entrar depois do 
        Com Gale 1

        Tendencias:
        Tendendia de Red:🔴🔴⚫⚫
        Tendendia de Red:🔴⚫🔴⚫
        Tendendia de Black:⚫⚫🔴🔴
        Tendendia de Black:⚫🔴⚫🔴

        Lembrando Caso nao esteja a favor
        Não Jogue

        Sempre Olhe o valor da aposta pois a casa
        sempre rouba
        """
    url = f'https://api.telegram.org/bot{chave}/sendMessage?chat_id={chat_id}&text={msg}'
    req = requests.get(url)
    print(req.content)
    return

def enviar_resultado_telegram(chave, chat_id, res):
    res = res.replace('gale', '🐔🐔🐔G1🐔🐔🐔') \
        .replace('win', '🟢🟢🟢WIN🟢🟢🟢') \
        .replace('loss', '🔴🔴🔴Loss🔴🔴🔴')\
        .replace('white', '⚪⚪⚪Branco⚪⚪⚪ \n Tente no duplo tambem')
    msg = f"""{res}"""
    url = f'https://api.telegram.org/bot{chave}/sendMessage?chat_id={chat_id}&text={msg}'
    req = requests.get(url)
    print(req.content)
    return
