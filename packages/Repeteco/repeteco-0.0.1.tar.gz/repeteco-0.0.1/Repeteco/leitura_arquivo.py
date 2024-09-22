from docx import Document
import re

def leitura(caminho_arquivo: str) -> list:
    '''Transforma o texto em uma lista e filtra usando a função remove_simbolos'''
    texto = ''
    document = Document(caminho_arquivo)
    for paragrafo in document.paragraphs:
        texto += paragrafo.text
    texto_filtrado = remove_simbolos(texto)
    return texto_filtrado

def remove_simbolos(texto:str) -> str:
    # Remove todos os caracteres que não são letras ou números
    texto_limpo = re.sub(r'[^\w\s]', '', texto)
    texto_vetor = texto_limpo.split()
    return texto_vetor
    
