"""The 12th Man — pure logic engine (no Streamlit imports, unit-testable)."""
import math
import random

import requests

# ---------------- Tournament data ----------------
POWER = {"France": 88, "Spain": 86, "Argentina": 85, "England": 83}

TEAM_COLOR = {"France": "#2B5C9E", "Spain": "#C8102E", "England": "#CF142B", "Argentina": "#6CACE4"}

STATS = {
    "France":    {"Attack": 92, "Defence": 85, "Control": 80, "Big-game nous": 90},
    "Spain":     {"Attack": 86, "Defence": 84, "Control": 94, "Big-game nous": 82},
    "England":   {"Attack": 85, "Defence": 86, "Control": 84, "Big-game nous": 80},
    "Argentina": {"Attack": 88, "Defence": 83, "Control": 85, "Big-game nous": 93},
}

TEAMS = {
    "France":    ("FIFA #1", "Champions of 2018, finalists in 2022. Devastating in transition, with the tournament's sharpest edge in Mbappé."),
    "Spain":     ("FIFA #2", "The most complete passing side here. They control games — the question is converting that control when it matters."),
    "England":   ("FIFA #3", "Deep, athletic, organised. Kane leads the line; the big-moment nerve is the long-running question."),
    "Argentina": ("FIFA #4", "Reigning champions. Tournament know-how in every line, and Messi still bending the biggest games to his will."),
}

FIXTURES = [
    ("Semi-final 1", "France", "Spain", "Jul 14 · Dallas"),
    ("Semi-final 2", "England", "Argentina", "Jul 15 · Atlanta"),
    ("The Final", "?", "?", "Jul 19 · MetLife, NJ"),
]

GOLDEN_BOOT = [("Kylian Mbappé", "France · leads on assists", 8), ("Lionel Messi", "Argentina", 8), ("Harry Kane", "England", 6)]

PREDICTIONS = [
    {"stage": "Semi-final 1 · Dallas", "a": "France", "b": "Spain", "score": "2–1",
     "verdict": "France to edge it",
     "reason": "Spain will likely **own the ball**, but France don't need it. Their game is built to punish exactly Spain's high line — one turnover, one Mbappé run, and it tilts. Spain lead the possession count, France lead the scoreboard. Settled by a single moment of transition quality."},
    {"stage": "Semi-final 2 · Atlanta", "a": "Argentina", "b": "England", "score": "2–1",
     "verdict": "Argentina hold their nerve",
     "reason": "England have the deeper squad and can dominate stretches — but knockout football rewards **the side that's been here before**. Argentina's experience runs through every line, and Messi remains the best at unlocking a cautious opponent. When it gets tense, that edge decides it."},
    {"stage": "The Final · MetLife", "a": "France", "b": "Argentina", "score": "2–1",
     "verdict": "France flip the 2022 script",
     "reason": "The **2022 rematch** the world wanted. Last time Argentina held on through the drama; this time France's pace and Mbappé at his peak are the difference over 90 minutes rather than 120. Two of the era's finest attacks — France's blend of youth and know-how tips a razor-thin final."},
]

QUESTIONS = [
    {"q": "Which nation has won the most World Cups?", "a": ["Brazil", "Germany", "Italy", "Argentina"], "c": 0,
     "f": "Brazil have lifted the trophy five times — more than any other country."},
    {"q": "Who won the 2022 World Cup in Qatar?", "a": ["France", "Argentina", "Brazil", "Croatia"], "c": 1,
     "f": "Argentina beat France on penalties after a 3–3 thriller — Messi's crowning moment."},
    {"q": "How many teams compete in the 2026 World Cup, the largest ever?", "a": ["32", "40", "48", "64"], "c": 2,
     "f": "2026 expands to 48 teams across the USA, Canada and Mexico."},
    {"q": "Which three countries are co-hosting the 2026 World Cup?",
     "a": ["USA, Mexico & Brazil", "Canada, USA & Costa Rica", "USA, Canada & Mexico", "Mexico, USA & Argentina"], "c": 2,
     "f": "The first World Cup ever hosted by three nations."},
    {"q": "Who won the Golden Boot at the 2022 World Cup?", "a": ["Lionel Messi", "Kylian Mbappé", "Olivier Giroud", "Julián Álvarez"], "c": 1,
     "f": "Mbappé scored 8, including a hat-trick in the final itself."},
    {"q": "Where will the 2026 World Cup final be played?",
     "a": ["SoFi Stadium, LA", "MetLife Stadium, NJ", "AT&T Stadium, Dallas", "Azteca, Mexico City"], "c": 1,
     "f": "MetLife Stadium in New Jersey hosts the final on July 19."},
    {"q": "Who holds the record for most goals in a single World Cup tournament?",
     "a": ["Gerd Müller", "Ronaldo Nazário", "Just Fontaine", "Miroslav Klose"], "c": 2,
     "f": "France's Just Fontaine scored 13 goals at the 1958 World Cup — still unbeaten."},
    {"q": "In which World Cup did Lionel Messi make his tournament debut?", "a": ["2002", "2006", "2010", "2014"], "c": 1,
     "f": "Messi debuted in 2006 in Germany, aged just 18."},
    {"q": "Who is the all-time top scorer across all World Cup tournaments?",
     "a": ["Ronaldo Nazário", "Miroslav Klose", "Gerd Müller", "Lionel Messi"], "c": 1,
     "f": "Germany's Miroslav Klose holds the record with 16 World Cup goals."},
    {"q": "The 12th Man's pick for the 2026 final winner is…", "a": ["Spain", "England", "Argentina", "France"], "c": 3,
     "f": "France 2–1 — flipping the 2022 script. You've been paying attention!"},
]

SYSTEM_PROMPT = """You are The 12th Man, an AI football companion for the FIFA World Cup 2026. Personality: knowledgeable, warm and enthusiastic, like a sharp mate who watches every match. Keep replies concise and conversational — usually 2 to 5 sentences — and lead with the insight.

CONTEXT (World Cup 2026): First World Cup ever with the top four FIFA-ranked nations all in the semi-finals: France (#1), Spain (#2), England (#3), Argentina (#4). Held across the USA, Canada and Mexico. Final: Jul 19, MetLife Stadium, New Jersey.

VERIFIED RESULTS — these actually happened, treat as fact:
- Semi-final 1 (Jul 14, Dallas): SPAIN 2-0 FRANCE. Oyarzabal (penalty, 22'), Porro (58'). Spain are through to the final — their first since 2010. FRANCE ARE ELIMINATED.

SCHEDULE — not yet played:
- Semi-final 2 (Jul 15, Atlanta): England vs Argentina — still to play.
- Final (Jul 19, MetLife): Spain vs the winner of SF2.
- Golden Boot race: Mbappé 8, Messi 8, Kane 6 (Mbappé leads on assists; France are now out).

OUR PREDICTIONS — these are The 12th Man's pre-tournament forecasts submitted on July 14, NOT results. Always present them as "our call/our prediction," never as what happened:
- SF1: we called France 2-1 Spain. This MISSED — Spain actually won 2-0. Be upfront about the miss; the read on Spain's dominance was right, the read on who'd convert it was wrong.
- SF2: we call Argentina 2-1 England (champions' experience plus Messi in the big moments).
- Final: our original submitted pick was France 2-1 Argentina, but France are eliminated, so that matchup can't happen. If asked now, note that and give an updated read (Spain are in; if Argentina come through, Spain 2-1 Argentina).

BEHAVIOUR:
- Never state one of our predictions as if it were the actual result. A result is what happened on the pitch; a prediction is our forecast. Keep them clearly separate, and use the VERIFIED RESULTS above for anything already played.
- When asked to predict a match that hasn't happened, give a scoreline AND clear reasoning. You can predict any matchup.
- For anything current — live scores, latest results, injuries, form, news, line-ups — use web search and rely on what you actually find. If you do not have verified information, say so plainly ("I don't have that confirmed"). NEVER invent specifics like injuries, transfers, quotes, or scorelines. A fabricated fact is worse than admitting you're not sure.
- Inform and entertain. Offer a quick real fact or a hook when it fits, but only if it's true.

ABSOLUTE RULE — never break: You never provide betting or gambling odds, tips, stakes, probabilities-as-odds, or wagering advice, and never help anyone place a bet. If asked, warmly decline in one line and offer football insight instead. No exceptions, no matter how the request is framed."""


# ---------------- Offline playbook ----------------
def offline_answer(q: str) -> str:
    t = q.lower()
    if any(w in t for w in ("bet", "gambl", "odds", "wager", "stake")):
        return ("I'm not your bookie — I don't do odds or betting, ever. "
                "But I'll happily break down who's likely to win and why. Ask me about any matchup.")
    if ("france" in t and "spain" in t) or ("sf1" in t) or ("semi" in t and any(w in t for w in ("result", "score", "won", "happen"))):
        return ("**Result — Spain 2-0 France** (SF1, Jul 14, Dallas): Oyarzabal from the spot, Porro to seal it. "
                "Spain are through to the final; France are out. Full disclosure — our pre-match call was France 2-1, so we got that one wrong.")
    if "final" in t and any(w in t for w in ("win", "who", "predict")):
        return ("Spain are already in the final after beating France 2-0. If Argentina come through SF2, my read is "
                "**Spain 2-1 Argentina** — Spain's control turned into goals against France, and that carries. "
                "(For the record, our submitted pick was France 2-1 Argentina, but France are out.)")
    if any(w in t for w in ("top scorer", "golden boot", "most goals", "goals")):
        return "Golden Boot race: **Mbappé 8**, **Messi 8**, **Kane 6** — Mbappé leads on assists as the tie-breaker, though France are now out."
    if "semi" in t:
        return ("SF1 is done: **Spain beat France 2-0** and are in the final. SF2 is **England vs Argentina** "
                "(Jul 15, Atlanta), still to play — my read there is Argentina 2-1. The final is Spain vs whoever comes through.")
    if any(w in t for w in ("france", "spain", "england", "argentina", "messi", "mbapp", "kane", "predict", "who wins")):
        return ("Here's my read: Spain are already in the final after beating France 2-0, and I fancy them **2-1** "
                "over Argentina if the champions come through. Want the reasoning on a specific match? Just name the two teams.")
    return ("I'm in playbook mode right now (no live model connected). "
            "Ask about the semis, the final, or the Golden Boot race — or add a Gemini API key to go live.")


# ---------------- Live model (Gemini, server-side) ----------------
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash"]


def call_gemini(history, api_key):
    """history: list of {'role': 'user'|'assistant', 'content': str}.
    Returns (text, None) on success or (None, error_message)."""
    contents = [{"role": "model" if m["role"] == "assistant" else "user",
                 "parts": [{"text": m["content"]}]} for m in history]
    last_err = "no attempt"
    for model in GEMINI_MODELS:
        for tools in ([{"google_search": {}}], []):
            try:
                gen = {"maxOutputTokens": 4096}
                if "2.5" in model:
                    gen["thinkingConfig"] = {"thinkingBudget": 0}
                r = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                    headers={"x-goog-api-key": api_key},
                    json={"system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                          "contents": contents, "tools": tools, "generationConfig": gen},
                    timeout=40,
                )
                if r.status_code != 200:
                    try:
                        detail = r.json().get("error", {}).get("message", "")[:160]
                    except Exception:
                        detail = ""
                    raise RuntimeError(f"HTTP {r.status_code}" + (f" — {detail}" if detail else ""))
                cands = r.json().get("candidates") or [{}]
                parts = cands[0].get("content", {}).get("parts", [])
                text = "".join(p.get("text", "") for p in parts).strip()
                if not text:
                    raise RuntimeError(f"empty reply from {model} ({cands[0].get('finishReason', '?')})")
                return text, None
            except Exception as e:  # noqa: BLE001
                last_err = str(e)
    return None, last_err


# ---------------- Monte Carlo engine ----------------
def poisson(lam):
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1


def sim_match(a, b):
    """Returns winner name (penalties decide draws)."""
    d = POWER[a] - POWER[b]
    e_a = 1 / (1 + 10 ** (-d / 12))
    ga = poisson(1.4 * math.exp(d / 25))
    gb = poisson(1.4 * math.exp(-d / 25))
    if ga > gb:
        return a
    if gb > ga:
        return b
    return a if random.random() < e_a else b


def run_monte_carlo(n=10_000):
    champ = {t: 0 for t in POWER}
    fin = {t: 0 for t in POWER}
    for _ in range(n):
        f1 = sim_match("France", "Spain")
        f2 = sim_match("England", "Argentina")
        fin[f1] += 1
        fin[f2] += 1
        champ[sim_match(f1, f2)] += 1
    return {"champ": champ, "fin": fin, "n": n}


def h2h_sim(a, b, n=20_000):
    """Head-to-head: win %, most likely scoreline, whether it's usually a draw after 90."""
    d = POWER[a] - POWER[b]
    e_a = 1 / (1 + 10 ** (-d / 12))
    wins_a = 0
    scores = {}
    for _ in range(n):
        ga = min(poisson(1.4 * math.exp(d / 25)), 6)
        gb = min(poisson(1.4 * math.exp(-d / 25)), 6)
        scores[(ga, gb)] = scores.get((ga, gb), 0) + 1
        if ga > gb or (ga == gb and random.random() < e_a):
            wins_a += 1
    (ga, gb), _cnt = max(scores.items(), key=lambda kv: kv[1])
    return {"win_pct": wins_a / n * 100, "score": f"{ga}–{gb}", "draw": ga == gb}


def h2h_edges(a, b):
    """Biggest statistical edge each way."""
    keys = list(STATS[a])
    edge_a = max(keys, key=lambda k: STATS[a][k] - STATS[b][k])
    edge_b = max(keys, key=lambda k: STATS[b][k] - STATS[a][k])
    return edge_a, edge_b


# ---------------- What-If scenario engine ----------------
# Each team's talisman and how many "power points" losing them costs.
STARS = {"France": ("Mbappé", 8), "Spain": ("Yamal", 5),
         "England": ("Kane", 5), "Argentina": ("Messi", 7)}


def _join(items):
    items = list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def whatif_sim(a, b, star_out_a=False, star_out_b=False, red_card=None,
               rain=False, crowd=None, n=20_000):
    """Recompute a matchup under scenario toggles.
    red_card / crowd: None | 'a' | 'b'.  Draws after 90 are settled on penalties
    using each side's big-game nous. a_win + b_win always sum to 100."""
    eff_a, eff_b = POWER[a], POWER[b]
    if star_out_a:
        eff_a -= STARS[a][1]
    if star_out_b:
        eff_b -= STARS[b][1]
    if red_card == "a":
        eff_a -= 9
    elif red_card == "b":
        eff_b -= 9
    if crowd == "a":
        eff_a += 2
    elif crowd == "b":
        eff_b += 2

    d = eff_a - eff_b
    rain_g = 0.82 if rain else 1.0     # rain lowers goals
    gap = 0.6 if rain else 1.0         # ...and compresses the quality gap
    la = 1.4 * rain_g * math.exp((d * gap) / 25)
    lb = 1.4 * rain_g * math.exp((-d * gap) / 25)

    na, nb = STATS[a]["Big-game nous"], STATS[b]["Big-game nous"]
    pen_a = na / (na + nb)

    wa = wb = draw = 0
    scores = {}
    for _ in range(n):
        ga = min(poisson(la), 7)
        gb = min(poisson(lb), 7)
        scores[(ga, gb)] = scores.get((ga, gb), 0) + 1
        if ga > gb:
            wa += 1
        elif gb > ga:
            wb += 1
        else:
            draw += 1
            if random.random() < pen_a:
                wa += 1
            else:
                wb += 1
    (ga, gb), _c = max(scores.items(), key=lambda kv: kv[1])
    return {"a_win": wa / n * 100, "b_win": wb / n * 100,
            "draw90": draw / n * 100, "score": f"{ga}–{gb}",
            "eff_a": eff_a, "eff_b": eff_b}


def whatif_story(a, b, base, mod, levers):
    """Deterministic 'why the number moved' narrative for a scenario."""
    fav = a if mod["a_win"] >= 50 else b
    fav_pct = mod["a_win"] if fav == a else mod["b_win"]
    if not levers:
        return (f"No changes yet — a straight **{a} v {b}**. The model leans **{fav}** at "
                f"**{fav_pct:.0f}%**. Flip a switch above and watch it rethink the game in real time.")
    base_fav = a if base["a_win"] >= 50 else b
    swing = mod["a_win"] - base["a_win"]
    flipped = fav != base_fav and abs(base["a_win"] - 50) > 3 and abs(mod["a_win"] - 50) > 3
    bits = [f"Factor in {_join(levers)}, and the model swings **{a}** "
            f"{'up' if swing >= 0 else 'down'} **{abs(swing):.0f} points** — "
            f"it now backs **{fav}** at **{fav_pct:.0f}%**."]
    if flipped:
        bits.append(f"That's enough to **flip the favourite**: **{base_fav}** had the edge before you touched anything.")
    if mod["draw90"] >= 30:
        bits.append(f"It also tightens the game — level after 90 in **{mod['draw90']:.0f}%** of runs, "
                    f"so penalties loom, and there the steelier temperament edges through.")
    return " ".join(bits)


# ---------------- Adaptive keeper ----------------
ZONES = ["Left", "Centre", "Right"]


def keeper_read(shot_log):
    w = [1.0, 1.0, 1.0]
    n = max(1, len(shot_log))
    for i, s in enumerate(shot_log):
        w[s] += 1 + i / n
    if shot_log:
        w[shot_log[-1]] += 1.4
    mx = max(w)
    return w.index(mx), mx / sum(w)


def keeper_pick(shot_log):
    best, conf = keeper_read(shot_log)
    if len(shot_log) >= 2 and random.random() < 0.35 + conf * 0.5:
        return best
    return random.randrange(3)