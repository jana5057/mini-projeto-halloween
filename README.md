# Mini-Projeto: Festa em Cena (Halloween)

## Descrição do Projeto
A Festa em Cena é uma rede fictícia que vende fantasias e acessórios de Halloween por três canais: Mercado, Loja física e Web. A empresa precisa organizar seus registros e entender como os pedidos variam por canal e período.

O programa lê o arquivo `halloween_vendas.csv` (1500 pedidos, de agosto a novembro de 2024 e 2025), limpa e valida os dados e gera um relatório. Os dados são fictícios e têm problemas de propósito.

**O que é uma linha:** um pedido de um único produto, que pode ter várias unidades.

**Quatro colunas:**
- `canal_venda`: onde o pedido foi feito (Mercado, Loja física ou Web)
- `quantidade`: unidades do produto no pedido
- `data_venda`: data e hora do pedido
- `data_entrega`: data da entrega (vazia = sem entrega)

## Regras adotadas
**Textos**
- Categoria: `strip()`, `lower()` e `re.sub()` para remover pontuação, mantendo letras e espaços. Categoria vazia vira "sem categoria".
- Canal: padronizado para Mercado, Loja física e Web. Se não fosse reconhecido, o texto original ficaria e seria contado (aqui: 0).

**Valores**
- `quantidade` deve ser inteiro maior que zero.
- `preco_unitario` deve estar preenchido e não ser negativo.
- Registros com problema são marcados, sem inventar valores. Um pedido com dois problemas conta uma vez só no total de pedidos afetados.

**Datas**
- `data_venda` é convertida com `datetime.strptime` (formato `2025-10-12 14:35:00`). O texto original é preservado e a apresentação brasileira é criada com `strftime` (ex.: 12/10/2025).
- Data vazia ou inválida é contada e o processamento continua. Não se usa a data de hoje.

Custos e descontos estão no CSV, mas não foram usados.

## Guia de Execução
1. Coloque `main.py` e `halloween_vendas.csv` na mesma pasta.
2. Instale o Pandas: `pip install pandas`.
3. Execute: `python main.py`.

Arquivos necessários: `main.py`, `halloween_vendas.csv` e este `README.md`.

## Resultados
- Linhas lidas: 1500
- Categorias vazias preenchidas: 18 | Categorias não vazias alteradas: 1482
- Canais corrigidos: 45 | Não reconhecidos: 0
- Problemas em quantidade: 7 | em preço: 12 | Pedidos afetados: 19
- Datas vazias: 0 | Datas inválidas: 4
- Total de cancelados: 109

**Entrega sem data:** 109 pedidos sem data de entrega estão Cancelados e 34 têm outro status (exemplos: pedidos 1170, 990 e 740, todos Concluídos). A hipótese de que todo pedido sem entrega é cancelado é **falsa nesta base**. Status e datas não foram alterados.

### Descoberta 1: pedidos por período
- **Números:** outubro teve 393 pedidos em 2024 e 410 em 2025. Os outros meses ficaram entre 62 e 182.
- **Interpretação:** os dois meses de outubro somam 803 dos 1496 pedidos com data válida (cerca de 54%), então a procura se concentra no mês do Halloween.
- **Limitação:** a base é fictícia e cobre só agosto a novembro. Os números são pedidos registrados, não receita nem vendas concluídas. Quatro pedidos ficaram de fora por data inválida.

### Descoberta 2: pedidos por canal
- **Números:** Web 666, Loja física 551 e Mercado 283.
- **Interpretação:** a Web tem mais pedidos (cerca de 44% do total) e o Mercado tem menos (cerca de 19%).
- **Limitação:** pedido não é unidade nem valor. O canal com mais pedidos não é, necessariamente, o que mais vende.

## Reflexão: Machine Learning e qualidade de dados
Um modelo de Machine Learning aprende com os dados que recebe. Se os dados estão bagunçados, ele aprende errado. Por isso, antes de usar os dados, é preciso verificar informações ausentes, textos inconsistentes e datas inválidas.

Neste projeto, isso apareceu na prática. A mesma categoria estava escrita de vários jeitos (como "Fantasia", "FANTASIA!!!" e "Fantasia " com espaços), e 18 estavam vazias. Também havia 45 canais de venda escritos de forma diferente, 19 pedidos com quantidade ou preço inválidos e 4 datas inválidas. Sem a limpeza, um modelo trataria "Fantasia" e "fantasia" como coisas diferentes.

Outro cuidado foi não inventar valores. Quando faltava preço ou data, os registros foram apenas marcados. Se eu preenchesse com um valor qualquer, estaria criando uma informação falsa, e isso pioraria os resultados.

Limpar os dados é necessário, mas não basta. Mesmo com dados limpos, o modelo pode sofrer overfitting (decorar os dados de treino e errar com dados novos) ou underfitting (ser simples demais e não aprender o padrão). Para evitar isso, também importam os dados representarem bem o problema, a escolha do modelo e a forma de avaliá-lo. Esta base, por exemplo, é fictícia e cobre só quatro meses, então não representa o mercado real.