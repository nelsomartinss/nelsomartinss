"""Gera o gráfico de atividade (últimos 31 dias) como SVG, no estilo do github-readme-activity-graph."""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

USER = os.environ["GITHUB_USER"]
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/activity-graph.svg"
DAYS = 31

BG, TEXT, LINE, POINT, GRID = "#1F242C", "#E6EDF3", "#3B82F6", "#58A6FF", "#30363D"
W, H = 1200, 420
PAD_L, PAD_R, PAD_T, PAD_B = 70, 40, 70, 60


def fetch_days():
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=DAYS - 1)
    query = """query($login:String!,$from:DateTime!,$to:DateTime!){
      user(login:$login){contributionsCollection(from:$from,to:$to){
        contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    body = json.dumps({"query": query, "variables": {
        "login": USER,
        "from": start.strftime("%Y-%m-%dT00:00:00Z"),
        "to": end.strftime("%Y-%m-%dT23:59:59Z"),
    }}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
    })
    data = json.load(urllib.request.urlopen(req, timeout=30))
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    return days[-DAYS:]


def render(days):
    counts = [d["contributionCount"] for d in days]
    top = max(max(counts), 4)
    step = -(-top // 4)
    top = step * 4
    pw, ph = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    xs = [PAD_L + i * pw / (len(days) - 1) for i in range(len(days))]
    ys = [PAD_T + ph - c / top * ph for c in counts]

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Ubuntu, sans-serif">',
           f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>',
           f'<text x="{W / 2}" y="40" text-anchor="middle" fill="{TEXT}" font-size="22" font-weight="600">Gráfico de Contribuições de {USER}</text>',
           f'<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LINE}" stop-opacity=".5"/><stop offset="1" stop-color="{LINE}" stop-opacity="0"/></linearGradient></defs>']
    for i in range(5):
        y = PAD_T + ph - i * ph / 4
        out.append(f'<line x1="{PAD_L}" x2="{W - PAD_R}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="4 4"/>')
        out.append(f'<text x="{PAD_L - 12}" y="{y + 4:.1f}" text-anchor="end" fill="{TEXT}" font-size="12">{i * step}</text>')
    for i, d in enumerate(days):
        out.append(f'<text x="{xs[i]:.1f}" y="{H - PAD_B + 22}" text-anchor="middle" fill="{TEXT}" font-size="12">{int(d["date"][8:])}</text>')
    out.append(f'<text x="{W / 2}" y="{H - 12}" text-anchor="middle" fill="{TEXT}" font-size="13">Dias</text>')
    out.append(f'<text x="20" y="{PAD_T + ph / 2}" text-anchor="middle" fill="{TEXT}" font-size="13" transform="rotate(-90 20 {PAD_T + ph / 2})">Contribuições</text>')

    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    base = PAD_T + ph
    out.append(f'<polygon points="{xs[0]:.1f},{base} {pts} {xs[-1]:.1f},{base}" fill="url(#a)"/>')
    out.append(f'<polyline points="{pts}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>')
    for x, y, d in zip(xs, ys, days):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{POINT}"><title>{d["date"]}: {d["contributionCount"]}</title></circle>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(fetch_days()))
    print(f"Gerado {OUT}")
