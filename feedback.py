"""Rule-based personalized feedback."""


def generate_feedback(r):
    tips = []

    # Speech rate
    if r["wpm"] == 0:
        tips.append("No speech was detected. Try recording again.")
    elif r["wpm"] < 120:
        tips.append(f"Your pace is {r['wpm']} WPM, which is slow. Aim for 120-160 WPM.")
    elif r["wpm"] > 160:
        tips.append(f"Your pace is {r['wpm']} WPM, which is fast. Slow down to 120-160 WPM.")
    else:
        tips.append(f"Your pace of {r['wpm']} WPM is good.")

    # Fillers
    if r["filler_total"] == 0:
        tips.append("No filler words found. Great job.")
    else:
        top = max(r["fillers"], key=r["fillers"].get)
        tips.append(f"You used {r['filler_total']} filler words. "
                    f"The most common was '{top}'. Try pausing silently instead.")

    # Pronunciation
    if r["pronunciation_score"] >= 85:
        tips.append("Your pronunciation was clear.")
    else:
        tips.append("Some words were unclear. Practice these words: "
                    + (", ".join(sorted(set(r["unclear_words"]))) or "speak more clearly") + ".")

    # Grammar
    if r["grammar"]:
        tips.append(f"{len(r['grammar'])} grammar issue(s) found. Review them below.")
    else:
        tips.append("No grammar issues found.")

    return tips
