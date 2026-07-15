# The 12th Man — Solution Overview

**MatchMind Hackathon · Submitted 14 July 2026 · Solo entry: Krishiv**

*"Every team has eleven players. Now you have a twelfth."*

## What it is

The 12th Man is an AI-powered football companion for the FIFA World Cup 2026 — a Streamlit web application that informs, engages, and predicts. It combines a live conversational AI grounded in tournament knowledge, transparent match predictions with reasoning, an interactive what-if prediction lab, a real Monte Carlo simulation engine, an adaptive game AI, and playable trivia — all wrapped in a strict, visible no-gambling guardrail.

It's hosted free on Streamlit Community Cloud, so the AI chat is live for every visitor — the API key stays server-side and is never exposed. When the live model is unavailable, a built-in playbook answers from local tournament knowledge, so the app never looks broken.

## The eight features

**1. Ask The 12th Man — conversational AI.** A live chat agent powered by the Google Gemini API with Google Search grounding, so answers stay current through the knockout rounds. It is grounded in tournament context, predicts any matchup with reasoning on request, and refuses betting or odds questions by design. A graceful offline fallback answers from built-in knowledge when no API is available, so the hosted app never looks broken.

**2. Insights.** Four semifinalist profile cards (France, Spain, Argentina, England — the first World Cup semis featuring the top four FIFA-ranked teams), the fixture schedule, and an animated Golden Boot race (Mbappé 8, Messi 8, Kane 6).

**3. Predictions with reasoning.** Three tap-to-reveal cards covering both semi-finals and the final. Each card shows a scoreline and the full analytical reasoning behind it — not odds, not tips, a read on the game. These match the officially submitted picks exactly, so judges can verify consistency.

**4. The What-If Prediction Lab — the flagship feature.** Where most prediction tools hand you a single fixed number, this one lets you *interrogate* the model. Pick any two teams, then change the conditions of the game — a talisman ruled out (Mbappé, Messi, Kane, Yamal), a red card, heavy rain, a partisan crowd — and the win probabilities recompute across 20,000 simulations in real time, each bar showing exactly how far it moved from the neutral baseline. The model then explains *why* the number shifted, in plain language and in The 12th Man's voice, with a live Gemini read on demand. It turns a static Monte Carlo output into an interactive, explainable reasoning tool — the direct answer to "anyone can run a simulation." Pull Mbappé out of France vs Spain and watch the favourite visibly flip; that five-second moment is the demo.

**5. Head-to-Head Lab.** Pick any two semifinalists and the model compares them stat by stat with animated bars, then calls the game: winner, win percentage across 20,000 simulations, most likely scoreline, and a written reasoning line built from each side's biggest statistical edge.

**6. The Simulator.** A genuine Monte Carlo engine that plays the semi-finals and final 10,000 times in the browser using a Poisson goal model with strength-adjusted expected goals and penalty shootouts on knockout draws. Animated trophy-odds bars show each team's title probability, while a dual commentary panel reacts live: the Analyst narrates the numbers, and a Nervous Fan reacts from the perspective of whichever team you choose to back. This is what makes The 12th Man an AI *system*, not a chatbot.

**7. Beat the Keeper.** A penalty shootout against an *adaptive* AI goalkeeper that studies the user's shooting pattern in real time — recency-weighted frequency analysis plus repeat-shot bias — and shows its "file" on you: shots studied, where it expects you to go, and how confident its read is. It keeps its memory between rounds, so it visibly gets harder. A second, transparent AI living inside the app.

**8. Trivia.** A playable 10-question World Cup quiz with scoring — pure engagement, all real football history.

## Locked predictions (submitted 14 July)

| Match | Prediction |
|---|---|
| SF1 — France vs Spain (14 Jul, Dallas) | **France 2–1 Spain** |
| SF2 — Argentina vs England (15 Jul, Atlanta) | **Argentina 2–1 England** |
| Final (19 Jul, MetLife) | **France 2–1 Argentina** — the 2022 rematch, script flipped |

## Responsible by design

The hackathon excludes gambling and betting concepts. The 12th Man doesn't just avoid them — it enforces the boundary. The guardrail is hardcoded into the AI agent's instructions, displayed in the hero ("Zero betting · zero odds"), restated in the chat interface and footer, and demonstrable live: ask it for betting odds and it declines, then offers analysis instead.

## Technology

Python/Streamlit app in two files: `app.py` (UI) and `engine.py` (pure, testable logic — Monte Carlo engine, what-if scenario engine, adaptive keeper, Gemini client, offline playbook). Google Gemini API (free tier) with Google Search grounding for live answers, called server-side with the key held in Streamlit secrets; Poisson-model Monte Carlo (10,000+ iterations); graceful offline playbook so nothing ever looks broken. Hosted free on Streamlit Community Cloud. No paid software, no copyrighted content redistribution, fully functional and demonstrable.

## Why it stands out

Anyone can wire up a chatbot, and plenty of solutions can run a Monte Carlo simulation. The 12th Man's differentiator is composition — and one feature that goes a step further. It pairs grounded knowledge, live web search, and transparent reasoning on every prediction with a **what-if lab that lets anyone stress-test the model and watch it explain why it changes its mind** — a static simulation turned into an interactive, explainable tool. Add a real statistical simulation engine, an adaptive game AI that learns the user, and an enforced responsibility guardrail, delivered as one portable artifact with a distinct personality, and the through-line is clear: the AI doesn't replace football judgment — it shows its work, and it lets you push on it.