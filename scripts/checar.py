#!/usr/bin/env python3
"""Modo Carreira · verificação das missões.
Uso: python3 scripts/checar.py <1-5>
Olha o resultado (site no ar, plan, cluster), não o texto. Sai com código 1 se a missão não foi cumprida."""
import csv, json, subprocess, sys, time, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
M = RAIZ / "missoes"
NOMES = {1: "BASE", 2: "NUVEM", 3: "ESTEIRA", 4: "PLATAFORMA", 5: "IA APLICADA"}
falhas = []


def ok(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        falhas.append(msg)
    return cond


def run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(r.stdout[-1500:], r.stderr[-1500:])
    return r


def plano_json(pasta):
    """terraform init + plan + show -json. Devolve a lista resource_changes."""
    if run("terraform init -input=false -no-color", cwd=pasta).returncode != 0:
        ok(False, "terraform init falhou")
        return []
    if not ok(run("terraform validate -no-color", cwd=pasta).returncode == 0, "terraform validate ok"):
        return []
    if not ok(run("terraform plan -input=false -no-color -refresh=false -out=.checar.tfplan", cwd=pasta).returncode == 0, "terraform plan ok"):
        return []
    r = run("terraform show -json .checar.tfplan", cwd=pasta)
    try:
        return json.loads(r.stdout).get("resource_changes", [])
    except json.JSONDecodeError:
        ok(False, "não consegui ler o plan em JSON")
        return []


def por_tipo(rc, tipo):
    return [x["change"]["after"] or {} for x in rc if x["type"] == tipo]


def checar_bucket_seguro(rc, exigir_cripto_tags=False):
    vers = por_tipo(rc, "aws_s3_bucket_versioning")
    ok(any((v.get("versioning_configuration") or [{}])[0].get("status") == "Enabled" for v in vers), "versionamento ligado")
    pab = por_tipo(rc, "aws_s3_bucket_public_access_block")
    chaves = ["block_public_acls", "block_public_policy", "ignore_public_acls", "restrict_public_buckets"]
    ok(any(all(p.get(k) is True for k in chaves) for p in pab), "4 bloqueios de acesso público")
    if exigir_cripto_tags:
        sse = por_tipo(rc, "aws_s3_bucket_server_side_encryption_configuration")
        algs = [((s.get("rule") or [{}])[0].get("apply_server_side_encryption_by_default") or [{}])[0].get("sse_algorithm") for s in sse]
        ok(any(a in ("AES256", "aws:kms", "aws:kms:dsse") for a in algs), "criptografia no servidor")
        buckets = por_tipo(rc, "aws_s3_bucket")
        ok(any({"dono", "custo"} <= set((b.get("tags") or {}).keys()) for b in buckets), "tags dono e custo")


def missao1():
    pasta = M / "01-base"
    run("docker compose up -d", cwd=pasta, check=False)
    corpo, codigo = "", 0
    for _ in range(15):
        try:
            with urllib.request.urlopen("http://localhost:8080", timeout=3) as r:
                codigo, corpo = r.status, r.read().decode()
                break
        except Exception:
            time.sleep(2)
    ok(codigo == 200, "site responde 200 na porta 8080")
    ok("Missão 1 cumprida" in corpo, "página da loja no ar")
    ok(run("docker compose exec -T web nginx -t", cwd=pasta, check=False).returncode == 0, "nginx -t válido")


def missao2():
    import yaml
    pasta = M / "02-nuvem"
    def soma(arq):
        t = {}
        for r in csv.DictReader(open(pasta / arq, encoding="utf-8")):
            t[r["recurso"]] = t.get(r["recurso"], 0) + float(r["custo_brl"])
        return t
    out, nov = soma("fatura_outubro.csv"), soma("fatura_novembro.csv")
    aumento = sum(nov.values()) - sum(out.values())
    cresc = sorted(((nov[k] - out[k], k) for k in nov if k in out), reverse=True)
    top3 = [k for _, k in cresc[:3]]
    novo = [k for k in nov if k not in out]
    resp = yaml.safe_load(open(pasta / "respostas.yaml", encoding="utf-8")) or {}
    ok(abs(float(resp.get("aumento_total_brl") or 0) - aumento) <= 1, "aumento total correto")
    ok([str(x).strip() for x in (resp.get("recursos_que_mais_cresceram") or [])] == top3, "top 3 recursos, na ordem")
    ok(str(resp.get("recurso_novo") or "").strip() in novo, "recurso novo identificado")
    alerta = float(resp.get("alerta_orcamento_percentual") or 0)
    ok(50 <= alerta <= 90, "alerta antes de estourar")


def missao3():
    checar_bucket_seguro(plano_json(M / "03-esteira"))


def missao4():
    pasta = M / "04-plataforma"
    r = run("kubectl rollout status deployment/api -n loja --timeout=180s", check=False)
    ok(r.returncode == 0, "rollout da api concluído")
    r = run("kubectl get deployment api -n loja -o json", check=False)
    prontos = json.loads(r.stdout).get("status", {}).get("readyReplicas", 0) if r.returncode == 0 else 0
    ok(prontos == 2, "2 pods prontos")
    import yaml
    def nomes_env(doc):
        if not isinstance(doc, dict) or doc.get("kind") != "Deployment":
            return []
        cs = (((doc.get("spec") or {}).get("template") or {}).get("spec") or {}).get("containers") or []
        return [e.get("name") for c in cs for e in (c.get("env") or [])] + \
               [r for c in cs for f in (c.get("envFrom") or []) for r in ("envFrom",)]
    envs = []
    for p in (pasta / "k8s").glob("*.y*ml"):
        for doc in yaml.safe_load_all(p.read_text(encoding="utf-8")):
            envs += nomes_env(doc)
    ok("DATABASE_URL" in envs or "envFrom" in envs, "correção no YAML do Deployment")
    pi = pasta / "POS-INCIDENTE.md"
    linhas = [l for l in pi.read_text(encoding="utf-8").splitlines() if l.strip()] if pi.exists() else []
    ok(len(linhas) >= 4, "POS-INCIDENTE.md escrito")


def missao5():
    pasta = M / "05-ia-aplicada"
    rc = plano_json(pasta)
    checar_bucket_seguro(rc, exigir_cripto_tags=True)
    ok((pasta / "PROMPT.md").exists() and (pasta / "PROMPT.md").read_text(encoding="utf-8").strip() != "", "PROMPT.md presente")
    exp = pasta / "EXPLICACAO.md"
    texto = exp.read_text(encoding="utf-8") if exp.exists() else ""
    tipos = sorted({x["type"] for x in rc})
    ok(bool(tipos) and all(t in texto for t in tipos), "EXPLICACAO.md cobre o plan")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if n not in NOMES:
        sys.exit("uso: python3 scripts/checar.py <1-5>")
    print(f"\n MODO CARREIRA · MISSÃO {n} · {NOMES[n]}\n")
    globals()[f"missao{n}"]()
    if falhas:
        print(f"\n ✗ Missão {n}: {len(falhas)} pendência(s). Veja o MISSAO.md.\n")
        sys.exit(1)
    print(f"\n ★ MISSÃO {n} CUMPRIDA ★\n")


if __name__ == "__main__":
    main()
