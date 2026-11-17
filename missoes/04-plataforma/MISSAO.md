![Missão 4](../../assets/missao-4.svg)

# Missão 4 · Plataforma · O pós-incidente sem culpado

A API da loja entrou em `CrashLoopBackOff` depois da última mudança. Sua missão: colocar de pé, do jeito certo, e escrever o pós-incidente.

## Objetivo
1. Os 2 pods da `api` no namespace `loja` ficam `Running` e prontos.
2. A correção fica **no código** (nos YAML de `k8s/`), não só no cluster.
3. Escreva `POS-INCIDENTE.md` com: o que aconteceu, como você descobriu, o que corrigiu e o que evita repetir. Sem culpar pessoas.

## Comandos
```bash
cd missoes/04-plataforma
./subir-cluster.sh
kubectl get pods -n loja
kubectl logs -n loja deploy/api
kubectl describe pod -n loja -l app=api
```
Dica: o banco do laboratório pode ser só um texto, como `postgres://lab:lab@banco:5432/loja`. Um ConfigMap é o jeito elegante.

## Conferir
```bash
python3 scripts/checar.py 4
```
![Missão cumprida](../../assets/cumprida.svg)

Recompensa: ★ Plataforma destravada.
