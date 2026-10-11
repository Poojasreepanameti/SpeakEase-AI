"""Display results and progress charts."""
import pandas as pd
import streamlit as st


def show_results(r):
    st.subheader("Transcript")
    st.write(r["transcript"] or "(no speech detected)")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Words per minute", r["wpm"])
    c2.metric("Filler words", r["filler_total"])
    c3.metric("Pronunciation", f"{r['pronunciation_score']}%")
    c4.metric("Grammar issues", len(r["grammar"]))

    if r["fillers"]:
        st.subheader("Filler words used")
        st.bar_chart(pd.Series(r["fillers"]))

    if r["unclear_words"]:
        st.subheader("Unclear words")
        st.write(", ".join(sorted(set(r["unclear_words"]))))

    if r["grammar"]:
        st.subheader("Grammar issues")
        st.table(pd.DataFrame(r["grammar"]))

    st.subheader("Feedback")
    for tip in r["feedback"]:
        st.write("- " + tip)


def show_progress(rows):
    if not rows:
        st.info("No sessions yet. Record your first speech.")
        return
    df = pd.DataFrame(rows).set_index("created")
    st.subheader("Speech rate (WPM)")
    st.line_chart(df["wpm"])
    st.subheader("Filler words per session")
    st.line_chart(df["fillers"])
    st.subheader("Pronunciation score")
    st.line_chart(df["pronunciation"])
    st.subheader("Grammar issues per session")
    st.line_chart(df["grammar_issues"])
    st.subheader("History")
    st.dataframe(df[["words", "wpm", "fillers", "pronunciation", "grammar_issues"]])
