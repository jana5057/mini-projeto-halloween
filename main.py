import csv
import re

def ler_csv(caminho):
    """Lê o csv como texto e devolve uma lista de dicionários"""
    with open(caminho, mode="r", encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))

def limpar_categoria(texto):
    """Limpa uma categoria: minúscula, sem espaços nas pontas e sem pontuação"""
    texto = texto.strip().lower()
    texto = re.sub(r"[^\w\s]", '', texto) # remove pontuações
    texto = re.sub(r"\s+", " ", texto).strip() #junta espaços repetidos
    if texto == "":
        return "sem categoria" #sem valores inventados
    return texto

def padronizar_categorias(registros):
    """Limpa as categorias e conta as duas situações separadamente"""
    vazias_preenchidas = 0
    nao_vazias_alteradas = 0
    for registro in registros:
        original = registro["categoria"]
        limpa = limpar_categoria(original)
        if original.strip() == "":
            vazias_preenchidas += 1
        elif limpa != original:
            nao_vazias_alteradas += 1
        registro["categoria"] = limpa
    return vazias_preenchidas, nao_vazias_alteradas

def valores_distintos(registros, campo):
    """Conta quantas vezes cada valor aparece em uma coluna"""
    contagem = {}
    for registro in registros: 
        valor = registro[campo]
        contagem[valor] = contagem.get(valor,0) + 1
    return contagem 

registros = ler_csv("halloween_vendas.csv")
print("total de registros:", len(registros))
print("canais ANTES:", valores_distintos(registros, "canal_venda"))
print("categorias ANTES:", valores_distintos(registros, "categoria"))

vazias, alteradas = padronizar_categorias(registros)
print("categorias vazias preenchidas:", vazias)
print("categorias não vazias alteradas:", alteradas)

print("categorias DEPOIS:", valores_distintos(registros, "categoria"))
            