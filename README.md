# The 12th Man — AI World Cup Companion (Streamlit)

*Every team has eleven players. Now you have a twelfth.*

Built for Philips MatchMind 2026. Seven features: live AI chat (Gemini + Google Search grounding), tournament insights, predictions with reasoning, head-to-head lab, a 10,000-run Monte Carlo simulator, an adaptive AI penalty keeper, and trivia. Hardcoded no-gambling guardrail throughout.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Playbook (offline) mode works with no key. To go live, either paste a Google AI Studio key in the sidebar, or create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-key-here"
```

Get a free key at https://aistudio.google.com (no card needed).

## Deploy free on Streamlit Community Cloud

1. Push this folder to a **public GitHub repo** (keep `secrets.toml` out — it's for local only; never commit it).
2. Go to https://share.streamlit.io → **New app** → pick the repo, branch `main`, file `app.py`.
3. In the app's **Settings → Secrets**, paste: `GEMINI_API_KEY = "your-key-here"`
4. Deploy. You get a public URL where the AI chat is **live for every visitor** — the key stays server-side and is never exposed.

That public URL is your People's Choice link.

## Files

- `app.py` — Streamlit UI (7 tabs)
- `engine.py` — pure logic: Monte Carlo engine, adaptive keeper, Gemini client, playbook fallback (unit-testable, no Streamlit imports)
- `.streamlit/config.toml` — pitch-green/gold theme
