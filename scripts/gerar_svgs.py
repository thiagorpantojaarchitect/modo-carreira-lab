#!/usr/bin/env python3
"""Gera as artes animadas (SVG) da documentação do Modo Carreira.
Estilo: tela de carregamento de jogo de mundo aberto, pôr do sol neon. Desenho próprio, sem marca de terceiros.
Uso: python3 scripts/gerar_svgs.py   (precisa de fonttools)"""
import base64, io
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "assets" / "fonts"
SAIDA = RAIZ / "assets"

MISSOES = [
    (1, "BASE", "Ache o erro do nginx pelo log", "O primeiro incidente sozinho", "linux · redes · logs"),
    (2, "NUVEM", "Descubra por que a conta estourou", "A conta que estoura", "custo · FinOps · orçamento"),
    (3, "ESTEIRA", "Bucket seguro só por Terraform", "O deploy que quebra", "git · CI/CD · terraform"),
    (4, "PLATAFORMA", "Tire o pod do CrashLoopBackOff", "O pós-incidente sem culpado", "kubernetes · SRE · SLO"),
    (5, "IA APLICADA", "Gere com IA e prove que está certo", "O agente que ninguém explica", "agentes · MCP · governança"),
]


def fonte_b64(arquivo, texto):
    """Subconjunto só com os caracteres usados, embutido como WOFF em base64 (o SVG fica leve e autossuficiente)."""
    f = TTFont(FONTES / arquivo)
    s = subset.Subsetter(subset.Options())
    s.populate(text=texto + " ·→★✓…0123456789")
    s.subset(f)
    f.flavor = "woff"
    buf = io.BytesIO()
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cabecalho(w, h, textos_anton, textos_mono):
    a = fonte_b64("Anton.ttf", textos_anton)
    m = fonte_b64("JetBrainsMono.ttf", textos_mono)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<style>
@font-face{{font-family:A;src:url(data:font/woff;base64,{a}) format("woff")}}
@font-face{{font-family:M;src:url(data:font/woff;base64,{m}) format("woff")}}
.a{{font-family:A,Impact,"Arial Narrow Bold",sans-serif}} .m{{font-family:M,ui-monospace,Menlo,monospace;font-weight:700}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140A33"/><stop offset=".45" stop-color="#5B1E6E"/><stop offset=".72" stop-color="#E8436F"/><stop offset="1" stop-color="#FF9A4D"/></linearGradient>
<linearGradient id="sol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE27A"/><stop offset="1" stop-color="#FF3D8B"/></linearGradient>
<linearGradient id="txt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF3D8B"/><stop offset=".55" stop-color="#FF8A3D"/><stop offset="1" stop-color="#FFC247"/></linearGradient>
<linearGradient id="verde" x1="0" x2="1"><stop offset="0" stop-color="#3DF5A6"/><stop offset="1" stop-color="#2EE6E6"/></linearGradient>
<clipPath id="corte"><rect width="{w}" height="{h}" rx="22"/></clipPath>
<symbol id="estrela" viewBox="0 0 100 100"><path d="M50 3l13.5 31.5 34 3-26 22.5 8 33.5L50 76 20.5 93.5l8-33.5-26-22.5 34-3z"/></symbol>
<symbol id="palmeira" viewBox="0 0 100 200"><path d="M52 200c-4-55-2-100 4-130" stroke="#120624" stroke-width="7" fill="none"/><path d="M56 72c-20-18-44-20-56-12 18-2 34 4 50 18zM56 72c18-22 40-28 54-22-18 0-34 8-48 24zM56 72c-6-26 0-48 12-58-6 18-8 36-6 56zM56 72c-28-4-44 10-50 24 12-12 28-18 46-18zM56 72c26 0 40 14 44 28-10-12-26-20-42-22z" fill="#120624"/></symbol>
</defs>
<g clip-path="url(#corte)">'''


def hud_estrelas(x, y, n_acesas, total=5, tam=34, anim=True):
    out = []
    for i in range(total):
        acesa = i < n_acesas
        cor = "#FFC247" if acesa else "rgba(255,255,255,.18)"
        a = f'<animate attributeName="opacity" values="0.25;1;1;0.25" keyTimes="0;.15;.85;1" dur="5s" begin="{i*0.35}s" repeatCount="indefinite"/>' if (anim and acesa) else ""
        out.append(f'<use href="#estrela" x="{x + i*(tam+8)}" y="{y}" width="{tam}" height="{tam}" fill="{cor}">{a}</use>')
    return "".join(out)


def cidade(w, h, base):
    """Horizonte: prédios + data center com luzes piscando + palmeiras + rio com reflexo."""
    p = [f'<rect y="{base}" width="{w}" height="{h-base}" fill="#0A0620"/>']
    import random
    rnd = random.Random(7)
    x = 0
    while x < w:
        bw = rnd.randint(40, 90); bh = rnd.randint(40, 150)
        p.append(f'<rect x="{x}" y="{base-bh}" width="{bw}" height="{bh}" fill="#1A0B33"/>')
        for _ in range(rnd.randint(2, 6)):
            lx = x + rnd.randint(6, bw - 10); ly = base - rnd.randint(10, bh - 6)
            d = rnd.uniform(1.5, 4)
            p.append(f'<rect x="{lx}" y="{ly}" width="5" height="5" fill="#2EE6E6"><animate attributeName="opacity" values="1;.2;1" dur="{d:.1f}s" repeatCount="indefinite"/></rect>')
        x += bw + rnd.randint(2, 10)
    for px, s in ((60, 1.0), (w - 180, 1.25), (w - 90, .85)):
        p.append(f'<use href="#palmeira" x="{px}" y="{base-200*s+8}" width="{100*s}" height="{200*s}"/>')
    p.append(f'<g opacity=".55">' + "".join(f'<rect x="{i}" y="{base+10+(i*7)%40}" width="{rnd.randint(30,120)}" height="3" fill="#FF8A3D"><animate attributeName="x" values="{i};{i+30};{i}" dur="{rnd.uniform(4,8):.1f}s" repeatCount="indefinite"/></rect>' for i in range(0, w, 140)) + '</g>')
    return "".join(p)


def banner():
    w, h = 1280, 520
    t1, t2 = "MODO CARREIRA", "O LABORATÓRIO"
    sub = "5 missões reais · do suporte à IA aplicada · estrelas automáticas"
    s = [cabecalho(w, h, t1 + t2 + "MISSÕES", sub + "MISSÃO 0/5 CARREGANDO PRESSIONE START")]
    s.append(f'<rect width="{w}" height="{h}" fill="url(#ceu)"/>')
    s.append(f'<circle cx="{w*0.72}" cy="300" r="150" fill="url(#sol)"><animate attributeName="r" values="146;156;146" dur="6s" repeatCount="indefinite"/></circle>')
    s.append("".join(f'<rect x="{w*0.72-160}" y="{300+i*16}" width="320" height="{6+i}" fill="#5B1E6E"/>' for i in range(1, 7)))
    s.append(cidade(w, h, 400))
    # grade synthwave em movimento
    s.append('<g stroke="#FF3D8B" stroke-width="2" opacity=".55">')
    for i in range(-12, 13):
        s.append(f'<line x1="{w/2+i*12}" y1="400" x2="{w/2+i*140}" y2="{h}"/>')
    s.append('</g><g stroke="#FF3D8B" stroke-width="2" opacity=".55">')
    for k in range(5):
        s.append(f'<line x1="0" x2="{w}" y1="410" y2="410"><animate attributeName="y1" values="410;{h}" dur="3s" begin="{k*0.6}s" repeatCount="indefinite"/><animate attributeName="y2" values="410;{h}" dur="3s" begin="{k*0.6}s" repeatCount="indefinite"/></line>')
    s.append('</g>')
    # HUD
    s.append(f'<rect x="40" y="36" width="350" height="48" rx="8" fill="rgba(2,13,33,.75)" stroke="#3DF5A6" stroke-width="2"/><circle cx="64" cy="60" r="7" fill="#3DF5A6"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="82" y="68" class="m" font-size="20" fill="#3DF5A6" letter-spacing="2">MISSÃO 0/5 CARREGANDO</text>')
    s.append(hud_estrelas(w - 250, 42, 5))
    # minimapa com varredura
    s.append(f'<g transform="translate({w-120},420)"><circle r="70" fill="#081A33" stroke="#F4F7FB" stroke-width="5"/><path d="M-70 10 Q0 -20 70 20" stroke="#1E6FA8" stroke-width="14" fill="none"/><g><path d="M0 0 L0 -68 A68 68 0 0 1 48 -48 Z" fill="rgba(61,245,166,.35)"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/></g><path d="M0 -14 L10 10 L0 4 L-10 10 Z" fill="#FFC247"/><circle cx="-30" cy="-22" r="6" fill="#FF5470"><animate attributeName="r" values="4;8;4" dur="1.5s" repeatCount="indefinite"/></circle></g>')
    # título
    s.append(f'<text x="60" y="230" class="a" font-size="128" fill="#F4F7FB" letter-spacing="2" style="paint-order:stroke" stroke="#140A33" stroke-width="10">{t1}</text>')
    s.append(f'<text x="64" y="300" class="a" font-size="64" fill="url(#txt)" letter-spacing="3">{esc(t2)}</text>')
    s.append(f'<rect x="60" y="322" width="760" height="44" rx="6" fill="rgba(2,13,33,.72)"/><text x="78" y="351" class="m" font-size="19" fill="#F4F7FB">{esc(sub)}</text>')
    s.append(f'<text x="60" y="{h-30}" class="m" font-size="22" fill="#FFC247" letter-spacing="4">PRESSIONE START<animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></text>')
    s.append('</g></svg>')
    return "".join(s)


def mapa():
    w, h = 1280, 330
    nomes = [m[1] for m in MISSOES]
    s = [cabecalho(w, h, "".join(nomes) + "O MAPA", "região · " + "".join(m[4] for m in MISSOES))]
    s.append(f'<rect width="{w}" height="{h}" fill="#020D21"/>')
    s.append("".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="rgba(255,255,255,.04)"/>' for x in range(0, w, 40)))
    s.append(f'<text x="40" y="58" class="a" font-size="40" fill="#F4F7FB" letter-spacing="2">O MAPA</text>')
    xs = [130, 380, 640, 900, 1150]; ys = [250, 200, 165, 130, 95]
    d = f"M{xs[0]} {ys[0]} " + " ".join(f"C{(xs[i-1]+xs[i])/2} {ys[i-1]} {(xs[i-1]+xs[i])/2} {ys[i]} {xs[i]} {ys[i]}" for i in range(1, 5))
    s.append(f'<path d="{d}" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="10" stroke-linecap="round"/>')
    s.append(f'<path d="{d}" fill="none" stroke="url(#verde)" stroke-width="6" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200"><animate attributeName="stroke-dashoffset" values="1200;0;0;1200" keyTimes="0;.55;.9;1" dur="8s" repeatCount="indefinite"/></path>')
    for i, (x, y) in enumerate(zip(xs, ys)):
        cor = "#FF3D8B" if i == 4 else "#FFC247"
        t = 0.6 + i * 0.85
        s.append(f'<g transform="translate({x},{y})"><circle r="34" fill="#020D21" stroke="{cor}" stroke-width="6"><animate attributeName="stroke-width" values="6;6;11;6;6" keyTimes="0;{t/8:.3f};{(t+0.25)/8:.3f};{(t+0.6)/8:.3f};1" dur="8s" repeatCount="indefinite"/></circle><text y="13" text-anchor="middle" class="a" font-size="36" fill="{cor}">{i+1}</text></g>')
        s.append(f'<text x="{x}" y="{y+68}" text-anchor="middle" class="a" font-size="26" fill="#F4F7FB" letter-spacing="1">{esc(MISSOES[i][1])}</text><text x="{x}" y="{y+92}" text-anchor="middle" class="m" font-size="14" fill="#8EA0B8">{esc(MISSOES[i][4])}</text>')
    s.append('</g></svg>')
    return "".join(s)


def card(n, regiao, missao, chefao, skills):
    w, h = 1280, 300
    s = [cabecalho(w, h, f"{n}{regiao}MISSÃO", f"MISSÃO {n}/5 CARREGANDO CHEFÃO: {chefao} {missao} {skills} REGIÃO DICA")]
    s.append(f'<rect width="{w}" height="{h}" fill="url(#ceu)"/><rect width="{w}" height="{h}" fill="rgba(2,13,33,.55)"/>')
    s.append(cidade(w, h, 250))
    s.append(f'<text x="40" y="250" class="a" font-size="300" fill="rgba(255,255,255,.08)">{n}</text>')
    s.append(f'<rect x="40" y="30" width="250" height="40" rx="8" fill="rgba(2,13,33,.8)" stroke="#3DF5A6" stroke-width="2"/><text x="60" y="57" class="m" font-size="17" fill="#3DF5A6" letter-spacing="2">MISSÃO {n}/5</text>')
    s.append(hud_estrelas(w - 230, 34, n, tam=30))
    s.append(f'<text x="210" y="140" class="a" font-size="86" fill="#F4F7FB" letter-spacing="2" style="paint-order:stroke" stroke="#140A33" stroke-width="8">{esc(regiao)}</text>')
    s.append('<rect x="196" y="154" width="620" height="104" rx="12" fill="rgba(2,13,33,.78)"/>')
    s.append(f'<text x="214" y="182" class="m" font-size="24" fill="#FFC247">{esc(missao)}</text>')
    s.append(f'<text x="214" y="214" class="m" font-size="18" fill="#FF8FA8">CHEFÃO: {esc(chefao)}</text>')
    # barra de carregamento
    s.append(f'<rect x="214" y="234" width="560" height="10" rx="5" fill="rgba(255,255,255,.15)"/><rect x="214" y="234" width="0" height="10" rx="5" fill="url(#verde)"><animate attributeName="width" values="0;560;560" keyTimes="0;.8;1" dur="4s" repeatCount="indefinite"/></rect>')
    s.append(f'<text x="{w-40}" y="{h-26}" text-anchor="end" class="m" font-size="16" fill="#F4F7FB" opacity=".8">{esc(skills)}</text>')
    s.append('</g></svg>')
    return "".join(s)


def cumprida():
    w, h = 1280, 240
    s = [cabecalho(w, h, "MISSÃO CUMPRIDA", "+1 ESTRELA · região destravada")]
    s.append(f'<rect width="{w}" height="{h}" fill="#020D21"/>')
    s.append(f'<rect x="0" y="70" width="{w}" height="110" fill="rgba(255,194,71,.10)"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="4s" repeatCount="indefinite"/></rect>')
    s.append(f'<text x="{w/2}" y="158" text-anchor="middle" class="a" font-size="104" fill="url(#txt)" letter-spacing="4">MISSÃO CUMPRIDA<animate attributeName="letter-spacing" values="30;4;4;30" keyTimes="0;.15;.85;1" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.85;1" dur="4s" repeatCount="indefinite"/></text>')
    s.append(f'<text x="{w/2}" y="212" text-anchor="middle" class="m" font-size="22" fill="#3DF5A6">+1 ESTRELA · região destravada</text>')
    s.append(hud_estrelas(w/2 - 105, 20, 5, tam=34))
    s.append('</g></svg>')
    return "".join(s)


def main():
    (SAIDA / "banner.svg").write_text(banner(), encoding="utf-8")
    (SAIDA / "mapa.svg").write_text(mapa(), encoding="utf-8")
    (SAIDA / "cumprida.svg").write_text(cumprida(), encoding="utf-8")
    for m in MISSOES:
        (SAIDA / f"missao-{m[0]}.svg").write_text(card(*m), encoding="utf-8")
    for p in sorted(SAIDA.glob("*.svg")):
        print(p.name, round(p.stat().st_size / 1024), "KB")


if __name__ == "__main__":
    main()
