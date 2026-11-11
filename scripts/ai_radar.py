"""Write today's top Hugging Face paper and trending models into README.md
between the AIRADAR markers. Fails soft: on any error the old block stays."""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

README = "README.md"
START, END = "<!-- AIRADAR:START -->", "<!-- AIRADAR:END -->"
UA = {"User-Agent": "bernhardbrugger-profile-readme"}
# keep the profile professional: skip jailbroken / NSFW model variants
BLOCK = re.compile(r"uncensor|abliterat|heretic|nsfw|erotic|jailbreak|lewd|porn|hentai|unfiltered", re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def esc(text):
    return text.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;").strip()


def compact(n):
    n = int(n or 0)
    for unit, div in (("M", 1_000_000), ("k", 1_000)):
        if n >= div:
            return f"{n / div:.1f}{unit}".replace(".0", "")
    return str(n)


def top_paper():
    items = get("https://huggingface.co/api/daily_papers?limit=50")
    best = max(items, key=lambda x: (x.get("paper") or {}).get("upvotes", 0))
    p = best["paper"]
    title = esc(best.get("title") or p.get("title", ""))
    return title, f"https://huggingface.co/papers/{p['id']}", p.get("upvotes", 0)


def trending_models(n=3):
    models = get("https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=25")
    out = []
    for m in models:
        mid = m.get("id") or m.get("modelId")
        if not mid or BLOCK.search(mid) or len(out) >= n:
            continue
        out.append((mid, f"https://huggingface.co/{mid}", m.get("pipeline_tag") or "model",
                    m.get("likes", 0), m.get("downloads", 0)))
    return out


def render(paper, models):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title, url, votes = paper
    rows = "\n".join(
        f"| [{esc(mid)}]({murl}) | {esc(tag)} | ❤️ {compact(likes)} | ⬇️ {compact(dl)} |"
        for mid, murl, tag, likes, dl in models
    )
    return f"""{START}
📄 **Paper of the day:** [{title}]({url}) · ▲ {votes}

🔥 **Trending on Hugging Face**

| Model | Task | Likes | Downloads |
|---|---|---|---|
{rows}

<sub>Pulled daily from the Hugging Face API by a GitHub Action · last run {today}</sub>
{END}"""


def main():
    try:
        block = render(top_paper(), trending_models())
    except Exception as e:
        print(f"AI radar skipped: {e}", file=sys.stderr)
        return
    text = open(README, encoding="utf-8").read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    if new != text:
        open(README, "w", encoding="utf-8").write(new)
    print(block)


if __name__ == "__main__":
    main()
