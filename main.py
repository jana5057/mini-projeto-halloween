import csv
with open("halloween_vendas.csv", mode="r", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    registros = list(leitor)
print("total de registros:", len(registros))
for registro in registros[:3]:
    print(registro)
