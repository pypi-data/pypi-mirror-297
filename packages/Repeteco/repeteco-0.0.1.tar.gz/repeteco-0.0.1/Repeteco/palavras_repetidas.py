from collections import Counter

def contagem(texto: list) -> tuple[int,dict]:
    '''Conta a quantidade de palavras e a frequência de cada'''
    contagem_total = len(texto)
    contagem_palavra = Counter(texto)
    return contagem_total, contagem_palavra

def densidade_palavras(total_palavras: int, contagem_palavra:dict) :
    '''Retorna as palavras com densidade média e alta de repetição'''
    densidade_alta = {}
    densidade_media = {}
    for palavra,repeticao in contagem_palavra.items():
        porcentagem_repeticao = repeticao / total_palavras * 100
        if porcentagem_repeticao >= 10:
            densidade_alta[palavra] = porcentagem_repeticao
        elif porcentagem_repeticao >= 5:
            densidade_media[palavra] = porcentagem_repeticao
    densidade_alta = dict(sorted(densidade_alta.items(), key=lambda item: item[1], reverse=True))
    densidade_media = dict(sorted(densidade_media.items(), key=lambda item: item[1], reverse=True))
    return densidade_alta,densidade_media



