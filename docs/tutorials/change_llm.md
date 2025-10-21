# Improve LLM Performance by Selecting a Better LLM

The demo is set to use free models, which have lower performance.
You can now change the LLM model using environment variables instead of editing code.

## Method 1: Environment Variable (Recommended)

Set the `OPENROUTER_LLM_MODEL` environment variable in your `.env` file:

```bash
# .env
OPENROUTER_LLM_MODEL=meta-llama/llama-3.3-70b-instruct
```

## Method 2: Edit Code (Legacy)

Edit `services/chat_service.py` in this project
and change the LLM model from "meta-llama/llama-3.3-70b-instruct:free"
to another model such as "meta-llama/llama-3.3-70b-instruct" without the free
for better performance and still be about 20x cheaper than premier OpenAI models.

## Available Models

[Browse OpenRouter cheap models](https://openrouter.ai/models?max_price=0.1).

Popular alternatives:
- `meta-llama/llama-3.3-70b-instruct` (paid version, better performance)
- `anthropic/claude-3.5-sonnet:free` (Claude 3.5 Sonnet)
- `openai/gpt-4o-mini:free` (GPT-4o Mini)
- `google/gemini-pro:free` (Gemini Pro)

(as of August 15, 2025)
