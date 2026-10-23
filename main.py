import csv
import re
from datetime import datetime

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

CANAIS_PADRAO = {
    "mercado": "Mercado",
    "loja física": "Loja física",
    "web": "Web",
}
def padronizar_canal(texto):
    """Devolve o canal oficial, ou None se não for reconhecido."""
    chave = texto.strip().lower()
    return CANAIS_PADRAO.get(chave)
def padronizar_canais(registros):
    """Padroniza o canal e conta correções e canais não reconhecidos."""
    corrigidos = 0
    nao_reconhecidos = 0
    for registro in registros:
        original = registro["canal_venda"]
        padrao = padronizar_canal(original)
        if padrao is None:
            nao_reconhecidos += 1  # não inventamos valor: mantém o original
        else:
            if padrao != original:
                corrigidos += 1
            registro["canal_venda"] = padrao
    return corrigidos, nao_reconhecidos

def validar_quantidade(texto):
    """Devolve o motivo do problema, ou None se a quantidade for válida."""
    texto = texto.strip()
    if texto == "":
        return "quantidade vazia"
    try:
        valor = int(texto)
    except ValueError:
        # não quebra o programa: apenas registra o problema e segue
        return "quantidade não é inteiro"
    if valor <= 0:
        return "quantidade não é maior que zero"
    return None


def validar_preco(texto):
    """Devolve o motivo do problema, ou None se o preço for válido."""
    texto = texto.strip()
    if texto == "":
        return "preço ausente"
    try:
        valor = float(texto)
    except ValueError:
        return "preço não é número"
    if valor < 0:
        return "preço negativo"
    return None


def validar_registros(registros):
    """Marca problemas em cada pedido, sem alterar valores, e conta."""
    problemas_quantidade = 0
    problemas_preco = 0
    pedidos_afetados = 0
    for registro in registros:
        motivos = []
        motivo_q = validar_quantidade(registro["quantidade"])
        motivo_p = validar_preco(registro["preco_unitario"])
        if motivo_q is not None:
            motivos.append(motivo_q)
            problemas_quantidade += 1
        if motivo_p is not None:
            motivos.append(motivo_p)
            problemas_preco += 1
        registro["problemas"] = motivos  # só marca; não inventa valores
        if motivos:
            pedidos_afetados += 1  # conta o pedido uma vez, mesmo com 2 problemas
    return problemas_quantidade, problemas_preco, pedidos_afetados

def processar_datas(registros):
    vazias = 0
    invalidas = 0
    for registro in registros:
        texto = registro["data_venda"].strip()
        registro["ano_mes"] = None
        if texto == "":
            vazias += 1
            continue
        try:
            data = datetime.strptime(texto, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas += 1
            continue
        registro["ano"] = data.year
        registro["mes"] = data.month
        registro["dia"] = data.day
        registro["hora"] = data.hour
        registro["data_br"] = data.strftime("%d/%m/%Y")
        registro["ano_mes"] = data.strftime("%Y-%m")
    return vazias, invalidas

registros = ler_csv("halloween_vendas.csv")
print("total de registros:", len(registros))
print("canais ANTES:", valores_distintos(registros, "canal_venda"))
print("categorias ANTES:", valores_distintos(registros, "categoria"))

vazias, alteradas = padronizar_categorias(registros)
print("categorias vazias preenchidas:", vazias)
print("categorias não vazias alteradas:", alteradas)

print("categorias DEPOIS:", valores_distintos(registros, "categoria"))
corrigidos, nao_reconhecidos = padronizar_canais(registros)
print("canais corrigidos:", corrigidos)
print("canais não reconhecidos:", nao_reconhecidos)
print("canais DEPOIS:", valores_distintos(registros, "canal_venda"))
prob_q, prob_p, afetados = validar_registros(registros)
print("problemas em quantidade:", prob_q)
print("problemas em preço:", prob_p)
print("pedidos afetados:", afetados)
datas_vazias, datas_invalidas = processar_datas(registros)
print("datas vazias:", datas_vazias)
print("datas inválidas:", datas_invalidas)
print("exemplo de data BR:", registros[0].get("data_br"))
            