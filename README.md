# ClinicSocial - Health Content Generator

Live app: https://clinicsocial.streamlit.app/

Generate patient education content based on real health search trends in India.

## Setup

1. **Install dependencies**
```bash
pip install streamlit serpapi openai python-dotenv pandas
```

2. **Create .env file**
```bash
SERPAPI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

3. **Run locally**
```bash
streamlit run app.py
```

## API Keys

- **SerpAPI**: Get free key at serpapi.com (100 searches/month)
- **OpenAI**: Get API key from openai.com

## Usage

1. Enter health topic (e.g., "diabetes", "mental health")
2. Select content format and audience
3. Generate content ideas
4. Download as CSV

## Deploy

**Streamlit Cloud**
1. Fork this repo
2. Connect at share.streamlit.io
3. Add API keys in secrets:
   - `SERPAPI_API_KEY`
   - `OPENAI_API_KEY`

## Files

```
app.py              # Main application
requirements.txt    # Dependencies
.env               # API keys (local only)
```

## Requirements.txt

```
streamlit
serpapi
openai
python-dotenv
pandas
```