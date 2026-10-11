# Speech Analyzer

## Setup
1. Install Python 3.9+, **ffmpeg** (needed by Whisper) and **Java** (needed by the grammar checker).
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Files
| File | Purpose |
|---|---|
| app.py | Streamlit pages: login/register, record & analyze, progress |
| auth.py | Registration and login |
| db.py | SQLite for users and session history |
| transcribe.py | Whisper transcription |
| analysis.py | Filler words, speech rate, pronunciation, grammar |
| feedback.py | Personalized feedback rules |
| pipeline.py | Runs all steps and returns structured results |
| visualize.py | Result and progress charts |

## How each feature works
- **Filler words**: counts words from a fixed list (um, uh, like, you know, ...).
- **Speech rate**: number of words / speaking time in minutes (good range: 120-160 WPM).
- **Pronunciation**: average Whisper word confidence; words below 0.6 are flagged as unclear.
- **Grammar**: LanguageTool (en-US).
