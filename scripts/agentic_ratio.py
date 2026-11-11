"""Count how many of my recent public commits were co-authored with AI agents
and write the result into README.md between the AGENTIC markers."""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

USER = os.environ.get("GH_USER", "bernhardbrugger")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
DAYS = 30
README = "README.md"
START, END = "<!-- AGENTIC:START -->", "<!-- AGENTIC:END -->"

AGENTS = r"claude|anthropic|cursor|copilot|codex|openai|gemini|devin|aider|replit|windsurf|jules"
AGENT_TRAILER = re.compile(rf"^co-authored-by:.*({AGENTS})", re.I | re.M)
AGENT_FOOTER = re.compile(r"generated with \[?claude code", re.I)
AGENT_AUTHOR = re.compile(AGENTS, re.I)
BOT_AUTHOR = re.compile(r"\[bot\]|-bot\b|dependabot|renovate", re.I)


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def paged(path):
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = api(f"{path}{sep}per_page=100&page={page}")
        if not batch:
            return
        yield from batch
        if len(batch) < 100:
            return
        page += 1


def classify(author_name, author_email, message):
    """Return 'bot', 'agent' or 'human'."""
    who = f"{author_name} {author_email}"
    if BOT_AUTHOR.search(who):
        return "bot"
    if AGENT_TRAILER.search(message) or AGENT_FOOTER.search(message) or AGENT_AUTHOR.search(who):
        return "agent"
    return "human"


def collect():
    since = (datetime.now(timezone.utc) - timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = agent = 0
    repos_touched = set()
    for repo in paged(f"/users/{USER}/repos?type=owner&sort=pushed"):
        if repo["fork"] or repo["private"] or repo["name"] == USER:
            continue
        try:
            commits = list(paged(f"/repos/{USER}/{repo['name']}/commits?since={since}"))
        except Exception as e:  # empty repo or similar
            print(f"skip {repo['name']}: {e}", file=sys.stderr)
            continue
        for c in commits:
            if len(c.get("parents", [])) > 1:
                continue  # merge commit
            a = c["commit"]["author"] or {}
            kind = classify(a.get("name", ""), a.get("email", ""), c["commit"]["message"])
            if kind == "bot":
                continue
            total += 1
            agent += kind == "agent"
            repos_touched.add(repo["name"])
    return total, agent, len(repos_touched)


def render(total, agent, repos):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if total == 0:
        line = f"⚙️ <b>Last {DAYS} days:</b> quiet month, the agents are recharging."
    else:
        pct = round(100 * agent / total)
        repo_word = "repo" if repos == 1 else "repos"
        line = (f"⚙️ <b>Last {DAYS} days:</b> {total} commits across {repos} {repo_word} · "
                f"<b>{pct} % agent-assisted, 100 % human-reviewed</b>")
    return (f"{START}\n<p align=\"center\">\n{line}<br>\n"
            f"<sub>Auto-updated daily by a GitHub Action · last run {today}</sub>\n</p>\n{END}")


def main():
    total, agent, repos = collect()
    print(f"total={total} agent={agent} repos={repos}")
    text = open(README, encoding="utf-8").read()
    block = render(total, agent, repos)
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
    if new != text:
        open(README, "w", encoding="utf-8").write(new)


if __name__ == "__main__":
    main()
