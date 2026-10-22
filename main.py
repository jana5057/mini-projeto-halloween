import csv
import re
with open("halloween_vendas.csv", mode="r", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    registros = list(leitor)
for registro in registros:
    registro["categoria"]= re.sub(r"[^\w\s]", "", registro["categoria"]).strip().lower()
    if not registro["categoria"]: 
            registro["categoria"] = "sem categoria"
print("total de registros:", len(registros))
for registro in registros[:3]:
    print(registro)
