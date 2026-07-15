# The 12th Man — Solution Overview

**MatchMind Hackathon · Submitted 14 July 2026 · Solo entry: Krishiv**

*"Every team has eleven players. Now you have a twelfth."*

## What it is

The 12th Man is an AI-powered football companion for the FIFA World Cup 2026 — a Streamlit web application that informs, engages, and predicts. It combines a live conversational AI grounded in tournament knowledge, transparent match predictions with reasoning, a real Monte Carlo simulation engine, an adaptive game AI, and playable trivia — all wrapped in a strict, visible no-gambling guardrail.

It's hosted free on Streamlit Community Cloud, so the AI chat is live for every visitor — the API key stays server-side and is never exposed. A self-contained single-file HTML edition ships alongside it as an offline demo fallback.

## The seven features

**1. Ask The 12th Man — conversational AI.** A live chat agent powered by the Google Gemini API with Google Search grounding, so answers stay current through the knockout rounds. It is grounded in tournament context, predicts any matchup with reasoning on request, and refuses betting or odds questions by design. A graceful offline fallback answers from built-in knowledge when no API is available, so the hosted app never looks broken.

**2. Insights.** Four semifinalist profile cards (France, Spain, Argentina, England — the first World Cup semis featuring the top four FIFA-ranked teams), the fixture schedule, and an animated Golden Boot race (Mbappé 8, Messi 8, Kane 6).

**3. Predictions with reasoning.** Three tap-to-reveal cards covering both semi-finals and the final. Each card shows a scoreline and the full analytical reasoning behind it — not odds, not tips, a read on the game. These match the officially submitted picks exactly, so judges can verify consistency.

**4. Head-to-Head Lab.** Pick any two semifinalists and the model compares them stat by stat with animated bars, then calls the game: winner, win percentage across 20,000 simulations, most likely scoreline, and a written reasoning line built from each side's biggest statistical edge.

**5. The Simulator.** A genuine Monte Carlo engine that plays the semi-finals and final 10,000 times in the browser using a Poisson goal model with strength-adjusted expected goals and penalty shootouts on knockout draws. Animated trophy-odds bars show each team's title probability, while a dual commentary panel reacts live: the Analyst narrates the numbers, and a Nervous Fan reacts from the perspective of whichever team you choose to back. This is what makes The 12th Man an AI *system*, not a chatbot.

**6. Beat the Keeper.** A penalty shootout against an *adaptive* AI goalkeeper that studies the user's shooting pattern in real time — recency-weighted frequency analysis plus repeat-shot bias — and shows its "file" on you: shots studied, where it expects you to go, and how confident its read is. It keeps its memory between rounds, so it visibly gets harder. A second, transparent AI living inside the app.

**7. Trivia.** A playable 10-question World Cup quiz with scoring — pure engagement, all real football history.

## Locked predictions (submitted 14 July)

| Match | Prediction |
|---|---|
| SF1 — France vs Spain (14 Jul, Dallas) | **France 2–1 Spain** |
| SF2 — Argentina vs England (15 Jul, Atlanta) | **Argentina 2–1 England** |
| Final (19 Jul, MetLife) | **France 2–1 Argentina** — the 2022 rematch, script flipped |

## Responsible by design

The hackathon excludes gambling and betting concepts. The 12th Man doesn't just avoid them — it enforces the boundary. The guardrail is hardcoded into the AI agent's instructions, displayed in the hero ("Zero betting · zero odds"), restated in the chat interface and footer, and demonstrable live: ask it for betting odds and it declines, then offers analysis instead.

## Technology

Python/Streamlit app in two files: `app.py` (UI) and `engine.py` (pure, unit-tested logic — Monte Carlo engine, adaptive keeper, Gemini client, offline playbook). Google Gemini API (free tier) with Google Search grounding for live answers, called server-side with the key held in Streamlit secrets; Poisson-model Monte Carlo (10,000 iterations); graceful offline fallback so nothing ever looks broken. Hosted free on Streamlit Community Cloud. A ~60 KB single-file HTML edition serves as a zero-dependency offline backup. No paid software, no copyrighted content redistribution, fully functional and demonstrable.

## Why it stands out

Anyone can wire up a chatbot. The 12th Man's differentiator is composition: grounded knowledge + live web search + transparent reasoning on every prediction + a real statistical simulation engine + an adaptive game AI that learns the user + an enforced responsibility guardrail, delivered as one portable artifact with a distinct personality. The AI doesn't replace football judgment — it shows its work.