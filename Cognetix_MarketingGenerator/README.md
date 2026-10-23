# Cognetix AI Marketing Content Generator

## Objective
Generate editable marketing content for Instagram, LinkedIn,
and Email using configurable tone, length, language, and variations.

## Live Links
- App: Add your deployed Streamlit URL.
- GitHub: https://github.com/LizaNawaz/Cognetix_MarketingGenerator

## Architecture
Streamlit UI -> Prompt Builder -> Platform Templates and Few-Shot
Examples -> LLM API -> Pydantic Validation -> Editing UI -> TXT/PDF Export.

## Setup
1. Install Python 3.10 or newer.
2. Create a virtual environment:
   `python -m venv .venv`
3. Activate it:
   `.\.venv\Scripts\Activate.ps1`
4. Install packages:
   `python -m pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Add your API key and model settings to `.env`.
7. Run:
   `python -m streamlit run app.py`

## How It Works
Users enter product information and choose the platform, tone,
length, language, and number of variations.

The prompt builder applies platform rules and optional few-shot
examples. The model returns JSON, which Pydantic validates.
Users can edit drafts, view character counts, and export TXT/PDF.

## Evaluation Results
Test 12 inputs with few-shot examples enabled and disabled.
Record format validity, relevance, platform fit, and unsupported
claims in `eval/results.csv`.

Only report results after completing the tests.

## Limitations
- Output quality depends on the model and input details.
- Generated claims must be checked before publication.
- Built-in PDF fonts have limited Unicode support.
- API usage may incur charges or rate limits.
- Twelve test cases provide a small manual evaluation.

## Author
Liza Nawaz