"""Speech analysis: fillers, speech rate, pronunciation, grammar."""
import re

import language_tool_python
import streamlit as st

FILLERS = ["um", "uh", "er", "ah", "hmm", "like", "you know", "i mean",
           "basically", "actually", "literally"]
UNCLEAR_THRESHOLD = 0.6   # Whisper word confidence below this = unclear word


def detect_fillers(text):
    counts = {}
    for f in FILLERS:
        n = len(re.findall(r"\b" + re.escape(f) + r"\b", text.lower()))
        if n:
            counts[f] = n
    return counts


def speech_rate(words):
    """Words per minute, from first word start to last word end."""
    if len(words) < 2:
        return 0.0
    minutes = (words[-1]["end"] - words[0]["start"]) / 60
    return round(len(words) / minutes, 1) if minutes > 0 else 0.0


def assess_pronunciation(words):
    """Score = average Whisper word confidence (0-100). Low-confidence words are flagged."""
    if not words:
        return 0.0, []
    score = round(sum(w["prob"] for w in words) / len(words) * 100, 1)
    unclear = [w["word"] for w in words if w["prob"] < UNCLEAR_THRESHOLD]
    return score, unclear


@st.cache_resource
def _grammar_tool():
    return language_tool_python.LanguageTool("en-US")


def check_grammar(text):
    issues = []
    for m in _grammar_tool().check(text):
        issues.append({"message": m.message, "context": m.context,
                       "suggestions": ", ".join(m.replacements[:3])})
    return issues
