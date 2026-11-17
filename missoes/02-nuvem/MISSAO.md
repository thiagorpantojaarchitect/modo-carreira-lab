# Missão 2 · Nuvem · A conta que estoura

A fatura de novembro chegou bem maior que a de outubro. O financeiro quer saber o motivo até o fim do dia.

## Objetivo
Comparar `fatura_outubro.csv` e `fatura_novembro.csv` e preencher `respostas.yaml`.

## Dicas
- Some por recurso e compare os dois meses. Pode usar planilha, Python, SQL ou uma IA, desde que você confira a conta.
- Recurso que aparece só em novembro também é pista.
- Um bom alerta de orçamento avisa antes de estourar, não depois.

```bash
cd missoes/02-nuvem
python3 -c "import csv;print(sum(float(r['custo_brl']) for r in csv.DictReader(open('fatura_novembro.csv'))))"
```

## Conferir
```bash
python3 scripts/checar.py 2
```
Recompensa: ★ Nuvem destravada. Dados fictícios.
