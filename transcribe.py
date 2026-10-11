"""Speech-to-text using Whisper."""
import streamlit as st
import whisper

# The prompt nudges Whisper to keep filler words like "um" and "uh" in the text.
FILLER_PROMPT = "Umm, let me think, like, hmm... okay, so, you know, I mean, uh..."


@st.cache_resource
def load_model():
    return whisper.load_model("base")


def transcribe(audio_path):
    """Returns (text, words). Each word: {word, start, end, prob}."""
    result = load_model().transcribe(audio_path, word_timestamps=True,
                                     initial_prompt=FILLER_PROMPT, fp16=False)
    words = []
    for segment in result["segments"]:
        for w in segment.get("words", []):
            words.append({"word": w["word"].strip(), "start": w["start"],
                          "end": w["end"], "prob": w["probability"]})
    return result["text"].strip(), words
