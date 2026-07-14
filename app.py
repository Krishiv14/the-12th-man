"""The 12th Man — AI World Cup Companion (Streamlit edition)."""
import streamlit as st

import engine as E

st.set_page_config(page_title="The 12th Man — AI World Cup Companion", page_icon="⚽", layout="wide")

GOLD = "#F5C542"
RED = "#E4572E"
DIM = "#9DB0A2"

st.markdown(f"""
<style>
  .block-container {{max-width: 1080px}}
  h1, h2, h3 {{letter-spacing: .01em}}
  .tm-hero {{text-align:center; padding: 8px 0 4px}}
  .tm-hero h1 {{font-size: 3.2rem; line-height: 1.05; margin-bottom: 0}}
  .tm-hero .gold {{color:{GOLD}}}
  .tm-tag {{font-size: 1.15rem; margin-top: 6px}}
  .tm-tag em {{color:{GOLD}; font-style: normal}}
  .tm-pill {{display:inline-block; border:1px solid rgba(228,87,46,.5); background:rgba(228,87,46,.08);
            border-radius:100px; padding:6px 16px; margin-top:12px; font-weight:600}}
  .tm-card {{background: rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.10);
            border-radius:14px; padding:16px 18px; height:100%}}
  .tm-card h4 {{margin:0 0 2px}}
  .tm-card .rank {{color:{GOLD}; font-weight:700; font-size:.8rem; margin-bottom:8px}}
  .tm-card p {{color:{DIM}; font-size:.9rem; margin:0}}
  .tm-score {{font-size:2.6rem; font-weight:800; text-align:center; margin:6px 0 0}}
  .tm-score .w {{color:{GOLD}}}
  .tm-verdict {{text-align:center; font-weight:700; margin-bottom:6px}}
  .tm-bar {{background:rgba(255,255,255,.07); border-radius:100px; height:14px; overflow:hidden}}
  .tm-bar > div {{height:100%; border-radius:100px}}
  .tm-note {{color:{DIM}; font-size:.82rem}}
  .tm-guard b {{color:{RED}}}
</style>
""", unsafe_allow_html=True)


# ---------------- session state ----------------
def init_state():
    ss = st.session_state
    ss.setdefault("chat", [])
    ss.setdefault("shot_log", [])          # keeper's memory — survives replays
    ss.setdefault("pk_results", [])
    ss.setdefault("pk_goals", 0)
    ss.setdefault("pk_last", None)         # (shot, dive, scored)
    ss.setdefault("quiz_i", 0)
    ss.setdefault("quiz_score", 0)
    ss.setdefault("quiz_answered", False)
    ss.setdefault("quiz_choice", None)
    ss.setdefault("quiz_started", False)
    ss.setdefault("sim_results", None)
    ss.setdefault("user_key", "")


init_state()


def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return st.session_state.user_key.strip()


# ---------------- sidebar ----------------
with st.sidebar:
    st.markdown("## ⚽ The 12th Man")
    st.caption("Every team has eleven players. *Now you have a twelfth.*")
    key = get_api_key()
    if key:
        st.success("Live mode — Gemini connected")
    else:
        st.info("Playbook mode — add a key to go live")
        st.session_state.user_key = st.text_input(
            "Google AI Studio API key", type="password",
            help="Free at aistudio.google.com. Used server-side only.")
    st.divider()
    st.markdown('<div class="tm-guard">🛡️ <b>Zero betting · zero odds.</b> '
                'Insights and fun — never gambling.</div>', unsafe_allow_html=True)
    st.caption("Built for Philips MatchMind 2026")

# ---------------- hero ----------------
st.markdown("""
<div class="tm-hero">
  <h1>THE <span class="gold">12TH MAN</span></h1>
  <div class="tm-tag">Every team has eleven players. <em>Now you have a twelfth.</em></div>
  <div class="tm-pill">🛡️ Zero betting · zero odds</div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["💬 Ask", "📋 Insights", "🎯 Predictions", "⚔️ Head-to-Head",
                "🎲 Simulator", "🧤 Beat the Keeper", "🧠 Trivia"])


# ================= 1. ASK =================
with tabs[0]:
    st.subheader("Ask The 12th Man")
    st.markdown('<span class="tm-note">A real conversational agent — grounded in the tournament, '
                'checks the latest as you talk. It shares insight and analysis, '
                '<b>never betting tips or odds</b>.</span>', unsafe_allow_html=True)

    cols = st.columns(4)
    chips = ["Who wins the final?", "Predict Brazil vs Germany",
             "Who's the top scorer right now?", "Latest on the semis"]
    pending = None
    for c, chip in zip(cols, chips):
        if c.button(chip, use_container_width=True):
            pending = chip

    if not st.session_state.chat:
        st.session_state.chat.append({
            "role": "assistant",
            "content": "I'm The 12th Man — your companion for World Cup 2026. Ask me for a "
                       "prediction on any match, who to watch, or what's happening right now."})

    for m in st.session_state.chat:
        with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "⚽"):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask about any team, match, or prediction…") or pending
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        api_key = get_api_key()
        with st.chat_message("assistant", avatar="⚽"):
            with st.spinner("Checking the latest…" if api_key else "Thinking…"):
                if api_key:
                    text, err = E.call_gemini(st.session_state.chat, api_key)
                    if text is None:
                        text = f"⚠️ *Live lookup failed ({err}) — answering from the playbook.*\n\n" \
                               + E.offline_answer(prompt)
                else:
                    text = E.offline_answer(prompt)
            st.markdown(text)
        st.session_state.chat.append({"role": "assistant", "content": text})


# ================= 2. INSIGHTS =================
with tabs[1]:
    st.subheader("The Line-up")
    st.caption("Four heavyweights, three matches, one trophy. The road to MetLife runs through Dallas and Atlanta.")

    fcols = st.columns(3)
    for col, (tag, a, b, meta) in zip(fcols, E.FIXTURES):
        col.markdown(f"""<div class="tm-card" style="text-align:center">
          <div class="rank">{tag}</div><h4>{a} <span style="color:{DIM}">vs</span> {b}</h4>
          <p>{meta}</p></div>""", unsafe_allow_html=True)

    st.write("")
    tcols = st.columns(4)
    for col, (team, (rank, blurb)) in zip(tcols, E.TEAMS.items()):
        col.markdown(f"""<div class="tm-card" style="border-top:4px solid {E.TEAM_COLOR[team]}">
          <h4>{team}</h4><div class="rank">{rank}</div><p>{blurb}</p></div>""",
          unsafe_allow_html=True)

    st.write("")
    st.markdown("#### The Golden Boot race")
    st.caption("Top scorers heading into the semi-finals")
    for name, sub, goals in E.GOLDEN_BOOT:
        c1, c2, c3 = st.columns([3, 6, 1])
        c1.markdown(f"**{name}**<br><span class='tm-note'>{sub}</span>", unsafe_allow_html=True)
        c2.markdown(f"<div class='tm-bar' style='margin-top:12px'><div style='width:{goals/8*100:.0f}%;"
                    f"background:linear-gradient(90deg,#D9A520,{GOLD})'></div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div style='font-size:1.4rem;font-weight:800;color:{GOLD};text-align:right'>{goals}</div>",
                    unsafe_allow_html=True)


# ================= 3. PREDICTIONS =================
with tabs[2]:
    st.subheader("The Calls")
    st.caption("Not odds. Not a bet. A read on the game — with the reasoning behind every scoreline.")
    pcols = st.columns(3)
    for col, p in zip(pcols, E.PREDICTIONS):
        with col:
            st.markdown(f"""<div class="tm-card" style="text-align:center">
              <div class="rank">{p['stage']}</div>
              <h4>{p['a']} <span style="color:{DIM}">v</span> {p['b']}</h4>
              <div class="tm-score"><span class="w">{p['score'].split('–')[0]}</span>–{p['score'].split('–')[1]}</div>
              <div class="tm-verdict">{p['verdict']}</div></div>""", unsafe_allow_html=True)
            with st.expander("Why this call"):
                st.markdown(p["reason"])
    st.caption("These are the exact picks submitted on July 14 — the app and the official submission always agree.")


# ================= 4. HEAD-TO-HEAD =================
with tabs[3]:
    st.subheader("Head-to-Head Lab")
    st.caption("Pick any two of the four. The model weighs them stat by stat, then calls the game — reasoning included.")
    c1, c2, c3 = st.columns([2, 1, 2])
    team_a = c1.selectbox("First team", list(E.POWER), index=0)
    c2.markdown("<div style='text-align:center;font-size:1.6rem;font-weight:800;margin-top:26px'>VS</div>",
                unsafe_allow_html=True)
    team_b = c3.selectbox("Second team", list(E.POWER), index=2)

    if team_a == team_b:
        st.info("Even The 12th Man can't split a team from itself — pick two different sides.")
    else:
        for k in E.STATS[team_a]:
            va, vb = E.STATS[team_a][k], E.STATS[team_b][k]
            b1, b2, b3, b4, b5 = st.columns([1, 5, 2, 5, 1])
            b1.markdown(f"<b style='color:{GOLD if va>=vb else DIM}'>{va}</b>", unsafe_allow_html=True)
            b2.markdown(f"<div class='tm-bar' style='margin-top:8px;direction:rtl'><div style='width:{va}%;"
                        f"background:{E.TEAM_COLOR[team_a]};opacity:{1 if va>=vb else .45}'></div></div>",
                        unsafe_allow_html=True)
            b3.markdown(f"<div style='text-align:center' class='tm-note'><b>{k.upper()}</b></div>",
                        unsafe_allow_html=True)
            b4.markdown(f"<div class='tm-bar' style='margin-top:8px'><div style='width:{vb}%;"
                        f"background:{E.TEAM_COLOR[team_b]};opacity:{1 if vb>=va else .45}'></div></div>",
                        unsafe_allow_html=True)
            b5.markdown(f"<b style='color:{GOLD if vb>=va else DIM}'>{vb}</b>", unsafe_allow_html=True)

        r = E.h2h_sim(team_a, team_b)
        fav = team_a if r["win_pct"] >= 50 else team_b
        pct = r["win_pct"] if r["win_pct"] >= 50 else 100 - r["win_pct"]
        edge_a, edge_b = E.h2h_edges(team_a, team_b)
        pens = " — most often level after 90, settled on penalties" if r["draw"] else ""
        st.divider()
        st.markdown(f"### 🏅 **{fav}** win it")
        st.markdown(f"**{pct:.0f}%** of 20,000 simulations · most likely score: **{team_a} {r['score']} {team_b}**")
        st.markdown(f"**{team_a}** bring the edge in **{edge_a.lower()}** "
                    f"({E.STATS[team_a][edge_a]} v {E.STATS[team_b][edge_a]}); "
                    f"**{team_b}** answer with **{edge_b.lower()}** "
                    f"({E.STATS[team_b][edge_b]} v {E.STATS[team_a][edge_b]}). "
                    f"Over 20,000 simulated games the model backs **{fav}**{pens}.")
        st.caption("Model output, not odds — a read on the matchup, nothing to bet on.")


# ================= 5. SIMULATOR =================
with tabs[4]:
    st.subheader("The Simulator")
    st.caption("The reasoning behind the calls, quantified. We run the rest of the tournament "
               "ten thousand times — and let the numbers argue with the heart.")

    rcols = st.columns(4)
    for col, (t, p) in zip(rcols, E.POWER.items()):
        col.metric(t, p)
    st.caption("Power index — the model's team strength")

    backing = st.radio("You're backing", list(E.POWER), horizontal=True)
    if st.button("🎲 Run 10,000 simulations", type="primary", use_container_width=True):
        with st.spinner("Playing the semis and final 10,000 times…"):
            st.session_state.sim_results = E.run_monte_carlo(10_000)

    res = st.session_state.sim_results
    if res:
        teams = sorted(res["champ"], key=res["champ"].get, reverse=True)
        pct = {t: res["champ"][t] / res["n"] * 100 for t in teams}
        fin = {t: res["fin"][t] / res["n"] * 100 for t in teams}
        top_p = pct[teams[0]]
        st.write("")
        for t in teams:
            c1, c2, c3 = st.columns([2, 7, 1])
            c1.markdown(f"**{t}**<br><span class='tm-note'>final: {fin[t]:.0f}%</span>", unsafe_allow_html=True)
            c2.markdown(f"<div class='tm-bar' style='height:22px;margin-top:8px'><div style='width:{pct[t]/top_p*100:.0f}%;"
                        f"background:linear-gradient(90deg,{E.TEAM_COLOR[t]},{GOLD})'></div></div>",
                        unsafe_allow_html=True)
            c3.markdown(f"<div style='font-size:1.35rem;font-weight:800;color:{GOLD}'>{pct[t]:.0f}%</div>",
                        unsafe_allow_html=True)

        top, second = teams[0], teams[1]
        b_pct = pct[backing]
        a_col, f_col = st.columns(2)
        with a_col.container(border=True):
            st.markdown("**📊 The Analyst** · *reads the numbers*")
            st.markdown(f"Across **{res['n']:,}** simulations, **{top}** lift the trophy **{pct[top]:.0f}%** "
                        f"of the time — the widest margin in the field. **{second}** are the clearest threat at "
                        f"{pct[second]:.0f}%. But nothing here is a certainty: even the favourite loses far more "
                        f"often than they win.")
        with f_col.container(border=True):
            st.markdown(f"**🙈 The Nervous Fan** · *backing {backing}*")
            if backing == top:
                st.markdown(f"**{b_pct:.0f}%?!** Everyone says that like it's good news. All I hear is that we "
                            f"lose about {10 - b_pct/10:.0f} times out of ten. One bad night, one shootout, and "
                            f"it's gone. I'll be watching this one through my fingers.")
            else:
                st.markdown(f"**{b_pct:.0f}%** and buried behind {top}? Good. Write us off — that's exactly how "
                            f"we like it. Football isn't played in a spreadsheet. This is our year. I can feel it.")
        st.caption("A model for insight, not a bookmaker — probabilities to understand the race, never odds to bet on.")


# ================= 6. BEAT THE KEEPER =================
with tabs[5]:
    st.subheader("Beat the Keeper")
    st.caption("Five penalties against an AI keeper that studies your habits. "
               "The more you shoot, the better it reads you.")

    ss = st.session_state

    def take_shot(zone):
        dive = E.keeper_pick(ss.shot_log)
        ss.shot_log.append(zone)
        scored = zone != dive
        if scored:
            ss.pk_goals += 1
        ss.pk_results.append(scored)
        ss.pk_last = (zone, dive, scored)

    def reset_round():
        ss.pk_results, ss.pk_goals, ss.pk_last = [], 0, None  # keeper memory (shot_log) survives

    done = len(ss.pk_results) >= 5
    track = " ".join(("⚽" if r else "🧤") for r in ss.pk_results) + " ·" * (5 - len(ss.pk_results))
    st.markdown(f"### {track}")
    st.markdown(f"**Shot {min(len(ss.pk_results) + 1, 5)} / 5** · ⚽ {ss.pk_goals} scored")

    if ss.pk_last:
        zone, dive, scored = ss.pk_last
        if scored:
            st.success(f"GOAL! {E.ZONES[zone]} — keeper went {E.ZONES[dive]}.")
        else:
            st.error("SAVED — the keeper read you.")

    if not done:
        z1, z2, z3 = st.columns(3)
        z1.button("↖ Left", on_click=take_shot, args=(0,), use_container_width=True)
        z2.button("⬆ Centre", on_click=take_shot, args=(1,), use_container_width=True)
        z3.button("↗ Right", on_click=take_shot, args=(2,), use_container_width=True)
    else:
        won = ss.pk_goals >= 3
        if won:
            st.balloons()
        title = "Ice cold" if ss.pk_goals == 5 else ("Job done" if won else "Read like a book")
        st.markdown(f"## {ss.pk_goals}/5 — {title}")
        st.markdown("The keeper keeps its memory between rounds — it only gets harder. "
                    + ("Clinical." if won else "Change your pattern and run it back."))
        st.button("Shoot again", type="primary", on_click=reset_round)

    if len(ss.shot_log) >= 2:
        best, conf = E.keeper_read(ss.shot_log)
        st.caption(f"Keeper's file: **{len(ss.shot_log)} shots studied** · expects you to go "
                   f"**{E.ZONES[best]}** · read strength **{conf*100:.0f}%**")
    else:
        st.caption("The keeper has no file on you yet. It learns from every shot.")


# ================= 7. TRIVIA =================
with tabs[6]:
    st.subheader("The 12th Man Test")
    st.caption("Ten questions on the World Cup, past and present. The twelfth man always knows their stuff.")

    ss = st.session_state

    def start_quiz():
        ss.quiz_started, ss.quiz_i, ss.quiz_score = True, 0, 0
        ss.quiz_answered, ss.quiz_choice = False, None

    def answer(i):
        if not ss.quiz_answered:
            ss.quiz_answered, ss.quiz_choice = True, i
            if i == E.QUESTIONS[ss.quiz_i]["c"]:
                ss.quiz_score += 1

    def next_q():
        ss.quiz_i += 1
        ss.quiz_answered, ss.quiz_choice = False, None

    if not ss.quiz_started:
        st.markdown("### Ready, gaffer?")
        st.markdown("10 questions. One score. Let's see if you've earned the armband.")
        st.button("⚽ Kick off", type="primary", on_click=start_quiz)
    elif ss.quiz_i >= len(E.QUESTIONS):
        p = ss.quiz_score / len(E.QUESTIONS)
        title, msg = (("Captain's armband", "Flawless. You are the twelfth man this squad deserves.") if p == 1 else
                      ("Starting XI", "Serious knowledge. You'd walk into most punditry panels.") if p >= .7 else
                      ("On the bench", "Solid effort — a few more matchdays and you're starting.") if p >= .4 else
                      ("Trialist", "Everyone starts somewhere. Run it back and climb the ranks."))
        if p >= .7:
            st.balloons()
        st.markdown(f"## {ss.quiz_score}/{len(E.QUESTIONS)} — {title}")
        st.markdown(msg)
        st.button("Play again", type="primary", on_click=start_quiz)
    else:
        item = E.QUESTIONS[ss.quiz_i]
        st.progress(ss.quiz_i / len(E.QUESTIONS),
                    text=f"Q{ss.quiz_i + 1} / {len(E.QUESTIONS)} · ⚽ {ss.quiz_score} correct")
        st.markdown(f"#### {item['q']}")
        for i, opt in enumerate(item["a"]):
            label = f"{'ABCD'[i]} · {opt}"
            if ss.quiz_answered:
                if i == item["c"]:
                    label = f"✅ {label}"
                elif i == ss.quiz_choice:
                    label = f"❌ {label}"
            st.button(label, key=f"q{ss.quiz_i}o{i}", on_click=answer, args=(i,), use_container_width=True)
        if ss.quiz_answered:
            good = ss.quiz_choice == item["c"]
            (st.success if good else st.warning)(("Spot on. " if good else "Not quite. ") + item["f"])
            st.button("Next question" if ss.quiz_i < len(E.QUESTIONS) - 1 else "See your result",
                      type="primary", on_click=next_q)

st.divider()
st.markdown('<div class="tm-guard">🛡️ <b>Insights and fun — never betting.</b> The 12th Man shares no odds, '
            'takes no bets, and encourages no gambling of any kind. Predictions are a read on the game, '
            'nothing more. · Built for <b>Philips MatchMind 2026</b></div>', unsafe_allow_html=True)
