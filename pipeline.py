"""NLP pipeline: audio -> transcript -> structured insights -> feedback."""
import analysis
import feedback
import transcribe


def run_pipeline(audio_path):
    text, words = transcribe.transcribe(audio_path)             # 1. speech to text
    fillers = analysis.detect_fillers(text)                     # 2. filler words
    wpm = analysis.speech_rate(words)                           # 3. speech rate
    score, unclear = analysis.assess_pronunciation(words)       # 4. pronunciation
    grammar = analysis.check_grammar(text)                      # 5. grammar

    result = {
        "transcript": text,
        "word_count": len(words),
        "wpm": wpm,
        "fillers": fillers,
        "filler_total": sum(fillers.values()),
        "pronunciation_score": score,
        "unclear_words": unclear,
        "grammar": grammar,
    }
    result["feedback"] = feedback.generate_feedback(result)     # 6. feedback
    return result
