# Missão 5 · IA aplicada · Prove que a IA acertou

Use o assistente que quiser (Claude, GPT ou outro) para escrever um módulo Terraform. A IA escreve. O plan confere. **Você aprova e explica.**

## Objetivo
Criar em `modules/bucket/` um módulo com um bucket S3 que tenha:
1. versionamento ligado;
2. os 4 bloqueios de acesso público;
3. criptografia no servidor (AES256 ou KMS);
4. as tags `dono` e `custo`.

E entregar mais dois arquivos:
- `PROMPT.md`: o prompt que você usou, sem editar;
- `EXPLICACAO.md`: uma linha explicando cada `resource` do módulo, com o nome de cada tipo de recurso.

## Prompt de partida (original, funciona em qualquer assistente)
```
Atue como engenheiro de plataforma.
Crie um módulo Terraform para um bucket S3 (provider aws)
com versionamento, os 4 bloqueios de acesso público,
criptografia no servidor e as tags dono e custo.
1. Explique cada bloco em 1 linha.
2. Liste o que conferir no terraform plan.
3. Diga o que pode quebrar em produção.
Não invente versões nem argumentos. Na dúvida, escreva "conferir na doc".
```

`main.tf` desta pasta já chama o módulo e aponta para o LocalStack. Você só escreve o módulo.

## Conferir
```bash
cd missoes/05-ia-aplicada && terraform init && terraform validate
python3 scripts/checar.py 5
```
Recompensa: ★ IA aplicada destravada. Chefão vencido.
