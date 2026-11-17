![Missão 1](../../assets/missao-1.svg)

# Missão 1 · Base · O primeiro incidente sozinho

O site da loja caiu às 3 da manhã. Ninguém mais está online. Você tem o terminal.

## Objetivo
Colocar o site no ar em `http://localhost:8080` achando a causa **pelo log**, sem chutar.

## Comandos que ajudam
```bash
cd missoes/01-base
docker compose up -d
docker compose ps
docker compose logs web
```

## Regras
- Não troque a imagem nem a porta.
- Corrija só o que o log apontar.

## Conferir
```bash
python3 scripts/checar.py 1
```
![Missão cumprida](../../assets/cumprida.svg)

Recompensa: ★ Base destravada.
