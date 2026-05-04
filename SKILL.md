# TokenWatch

**Drop-in cost and usage intelligence for any application that calls LLM APIs** (OpenAI, Anthropic, Google, Mistral, custom endpoints, and more). Track spend locally, set budgets, compare models for the same token shape, and steer both **cost** and **context size** with data instead of guesses.

Free and open-source (MIT License) • Zero dependencies • Works locally • **No API keys required for TokenWatch itself** (your app still uses its own provider keys as usual)

---

## Adding TokenWatch to any LLM-powered app

TokenWatch is a **single Python module** (`tokenwatch.py`). You can vendor it into backends, agents, CLIs, or internal tools—anywhere you already make LLM calls.

| Integration surface | What to do |
|---------------------|------------|
| **Official Python SDKs** | After each successful call, use `record_from_openai_response` / `record_from_anthropic_response`, or read usage fields yourself and call `record_usage`. |
| **REST / any HTTP client** | Parse `usage` / `usage_metadata` (or equivalent) from the JSON response, then `monitor.record_usage(model, input_tokens, output_tokens, task_label=...)`. |
| **Streaming** | Record once the stream completes and the API returns final token counts (or sum chunks if your provider exposes that). |
| **Proxies & gateways** (Azure OpenAI, LiteLLM, etc.) | Map the **billing model id** string to an entry in `PROVIDER_PRICING`, or add a line with your gateway’s model name and per-1M rates. |

**One shared `TokenWatch()` instance** per process (or per tenant with a distinct `storage_path`) is enough to accumulate history, enforce budgets, and render dashboards.

---

## Cost optimization vs. context optimization

**Cost (what TokenWatch computes directly)**  
Use `compare_models` and `estimate_cost` *before* routing a request to pick a cheaper model for the same workload. Use `set_budget` / per-call caps to block runaway agents. Use `get_optimization_suggestions` and spend breakdowns to find expensive models and hot paths. Use `task_label` and `session_id` on `record_usage` to see *which features* burn the most money.

**Context (tokens in = money + latency + errors)**  
TokenWatch records **input** and **output** token counts per call. That makes oversized prompts and huge tool payloads visible in aggregates and suggestions (for example, high average input tokens per task). The library does **not** auto-shrink prompts; the application or agent should combine these metrics with good practices: trim chat history, summarize long documents before the final call, cache embeddings, avoid sending duplicate file contents, and choose smaller models for routing/classification steps.

Together: **measure with TokenWatch → decide smaller context and/or cheaper model → record again and confirm savings.**

---

## Why This Skill?

Shipping LLM features without telemetry on tokens and dollars is how teams get surprise bills and runaway context. This skill documents how to give **any** AI app local, transparent accounting and actionable comparisons—whether you use OpenAI, Anthropic, or another API—as long as you can obtain token counts from the provider response.

### Problems it solves:
- You don't know how much you're spending until the bill arrives
- No way to compare costs across providers and models before choosing one
- No alerts when you're approaching your budget
- No actionable suggestions for reducing spend
- Hard to see which routes, sessions, or prompts drive the largest **input** context and cost

---

## Features

### 1. Record Usage & Auto-Calculate Costs

```python
from tokenwatch import TokenWatch

monitor = TokenWatch()

monitor.record_usage(
    model="claude-haiku-4-5-20251001",
    input_tokens=1200,
    output_tokens=400,
    task_label="summarize article"
)
# ✅ Recorded: $0.00192
```

### 2. Auto-Record from API Responses

```python
from tokenwatch import record_from_anthropic_response, record_from_openai_response

# Anthropic
response = client.messages.create(model="claude-haiku-4-5-20251001", ...)
record_from_anthropic_response(monitor, response, task_label="my task")

# OpenAI
response = client.chat.completions.create(model="gpt-4o-mini", ...)
record_from_openai_response(monitor, response, task_label="my task")
```

### 3. Set Budgets with Alerts

```python
monitor.set_budget(
    daily_usd=1.00,
    weekly_usd=5.00,
    monthly_usd=15.00,
    per_call_usd=0.10,
    alert_at_percent=80.0   # Alert at 80% of budget
)
# ✅ Budget set: daily=$1.0, weekly=$5.0, monthly=$15.0
# 🚨 BUDGET ALERT fires automatically when threshold is crossed
```

### 4. Dashboard

```python
print(monitor.format_dashboard())
```

```
💰 SPENDING SUMMARY
  Today:   $0.0042  (4 calls, 13,600 tokens)
  Week:    $0.0231  (18 calls, 67,200 tokens)
  Month:   $0.1847  (92 calls, 438,000 tokens)

📋 BUDGET STATUS
  Daily:   [████░░░░░░░░░░░░░░░░] 42% $0.0042 / $1.00 ✅
  Monthly: [███████░░░░░░░░░░░░░] 37% $0.1847 / $0.50 ⚠️

💡 OPTIMIZATION TIPS
  🔴 Swap Opus → Sonnet for non-reasoning tasks (save ~$8.20/mo)
  🟡 High avg cost/call on gpt-4o — reduce prompt length
```

### 5. Compare Models Before Calling

```python
# For 2000 input + 500 output tokens:
for m in monitor.compare_models(2000, 500)[:6]:
    print(f"{m['model']:<42} ${m['cost_usd']:.6f}")
```

```
gemini-2.5-flash                           $0.000300
gpt-4o-mini                                $0.000600
mistral-small-2501                         $0.000350
claude-haiku-4-5-20251001                  $0.003600
mistral-large-2501                         $0.007000
gemini-2.5-pro                             $0.007500
```

### 6. Estimate Before You Call

```python
estimate = monitor.estimate_cost("claude-sonnet-4-5-20250929", input_tokens=5000, output_tokens=1000)
print(f"Estimated cost: ${estimate['estimated_cost_usd']:.6f}")
```

### 7. Optimization Suggestions

```python
suggestions = monitor.get_optimization_suggestions()
for s in suggestions:
    savings = s.get("estimated_monthly_savings_usd", 0)
    print(f"[{s['priority'].upper()}] {s['message']}")
    if savings:
        print(f"  → Save ~${savings:.2f}/month")
```

### 8. Export Reports

```python
monitor.export_report("monthly_report.json", period="month")
```

### 9. Generic pattern (any provider, any stack)

If there is no helper for your SDK, read whatever fields your API returns for prompt and completion tokens, then record:

```python
# After any successful LLM HTTP call — adapt field names to your provider JSON
def after_llm_call(monitor, model_id, usage, task_label=None):
    inp = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
    out = usage.get("completion_tokens") or usage.get("output_tokens") or 0
    monitor.record_usage(model_id, int(inp), int(out), task_label=task_label)
```

Use **`task_label`** for your product surface (e.g. `"support_reply"`, `"codegen"`, `"rerank"`) and **`session_id`** for a user or conversation id so dashboards and exports show where context and cost concentrate.

**Custom or private models:** add one row to `PROVIDER_PRICING` in `tokenwatch.py`:

```python
"my-azure-deployment-name": {"input": 0.50, "output": 1.50, "provider": "azure"},
```

Unknown model ids still create a usage row for counting tokens, but **cost is $0.00** until you add pricing—so production apps should register every model id they bill against.

---

## Supported Models (Feb 2026)

**41 models across 10 providers** — updated Feb 16, 2026.

| Provider | Model | Input/1M | Output/1M |
|----------|-------|----------|-----------|
| Anthropic | claude-opus-4-6 | $5.00 | $25.00 |
| Anthropic | claude-opus-4-5 | $5.00 | $25.00 |
| Anthropic | claude-sonnet-4-5-20250929 | $3.00 | $15.00 |
| Anthropic | claude-haiku-4-5-20251001 | $1.00 | $5.00 |
| OpenAI | gpt-5.2-pro | $21.00 | $168.00 |
| OpenAI | gpt-5.2 | $1.75 | $14.00 |
| OpenAI | gpt-5 | $1.25 | $10.00 |
| OpenAI | gpt-4.1 | $2.00 | $8.00 |
| OpenAI | gpt-4.1-mini | $0.40 | $1.60 |
| OpenAI | gpt-4.1-nano | $0.10 | $0.40 |
| OpenAI | o3 | $10.00 | $40.00 |
| OpenAI | o4-mini | $1.10 | $4.40 |
| Google | gemini-3-pro | $2.00 | $12.00 |
| Google | gemini-3-flash | $0.50 | $3.00 |
| Google | gemini-2.5-pro | $1.25 | $10.00 |
| Google | gemini-2.5-flash | $0.30 | $2.50 |
| Google | gemini-2.5-flash-lite | $0.10 | $0.40 |
| Google | gemini-2.0-flash | $0.10 | $0.40 |
| Mistral | mistral-large-2411 | $2.00 | $6.00 |
| Mistral | mistral-medium-3 | $0.40 | $2.00 |
| Mistral | mistral-small | $0.10 | $0.30 |
| Mistral | mistral-nemo | $0.02 | $0.10 |
| Mistral | devstral-2 | $0.40 | $2.00 |
| xAI | grok-4 | $3.00 | $15.00 |
| xAI | grok-3 | $3.00 | $15.00 |
| xAI | grok-4.1-fast | $0.20 | $0.50 |
| Kimi | kimi-k2.5 | $0.60 | $3.00 |
| Kimi | kimi-k2 | $0.60 | $2.50 |
| Kimi | kimi-k2-turbo | $1.15 | $8.00 |
| Qwen | qwen3.5-plus | $0.11 | $0.44 |
| Qwen | qwen3-max | $0.40 | $1.60 |
| Qwen | qwen3-vl-32b | $0.91 | $3.64 |
| DeepSeek | deepseek-v3.2 | $0.14 | $0.28 |
| DeepSeek | deepseek-r1 | $0.55 | $2.19 |
| DeepSeek | deepseek-v3 | $0.27 | $1.10 |
| Meta | llama-4-maverick | $0.27 | $0.85 |
| Meta | llama-4-scout | $0.18 | $0.59 |
| Meta | llama-3.3-70b | $0.23 | $0.40 |
| MiniMax | minimax-m2.5 | $0.30 | $1.20 |
| MiniMax | minimax-m1 | $0.43 | $1.93 |
| MiniMax | minimax-text-01 | $0.20 | $1.10 |

> To add a custom model: add it to `PROVIDER_PRICING` dict at the top of `tokenwatch.py`.

---

## API Reference

### `TokenWatch(storage_path)`
Initialize monitor. Data stored in `.tokenwatch/` by default.

### `record_usage(model, input_tokens, output_tokens, task_label, session_id)`
Record a single API call. Returns `TokenUsageRecord` with calculated cost.

### `set_budget(daily_usd, weekly_usd, monthly_usd, per_call_usd, alert_at_percent)`
Configure spending limits. Alerts fire automatically when thresholds are crossed.

### `get_spend(period)`
Get aggregated spend. Period: `"today"`, `"week"`, `"month"`, `"all"`, or `"YYYY-MM-DD"`.

### `get_spend_by_model(period)`
Spending breakdown by model, sorted by cost descending.

### `get_spend_by_provider(period)`
Spending breakdown by provider.

### `compare_models(input_tokens, output_tokens)`
Compare costs across all known models. Returns list sorted cheapest first.

### `estimate_cost(model, input_tokens, output_tokens)`
Estimate cost before making a call.

### `get_optimization_suggestions()`
Analyze usage and return ranked suggestions with estimated monthly savings.

### `format_dashboard()`
Human-readable spending dashboard with budget bars and tips.

### `export_report(output_file, period)`
Export full report to JSON.

### `record_from_anthropic_response(monitor, response, task_label)`
Helper to auto-record from Anthropic SDK response object.

### `record_from_openai_response(monitor, response, task_label)`
Helper to auto-record from OpenAI SDK response object.

---

## Privacy & Security

- ✅ **Zero telemetry** — No data sent anywhere
- ✅ **Local-only storage** — Everything in `.tokenwatch/` on your machine
- ✅ **No API keys required** — The monitor itself needs no credentials
- ✅ **No authentication** — No accounts or logins needed
- ✅ **Full transparency** — MIT licensed, source code included

---

## Changelog

### [1.2.3] - 2026-02-16

- 📋 SKILL.md: framed for **any LLM-backed app** (SDK, REST, streaming, gateways); added **cost vs. context** guidance; generic `record_usage` pattern and custom model pricing notes
- 📋 Updated SKILL.md model table to match code: 41 models across 10 providers

### [1.2.0] - 2026-02-16

- ✨ Added DeepSeek, Meta Llama, MiniMax providers
- ✨ Expanded to 41 models across 10 providers
- ✨ Updated all Anthropic/OpenAI/Google/Mistral pricing to Feb 2026 rates

### [1.1.0] - 2026-02-16

- ✨ Added xAI Grok, Kimi (Moonshot), Qwen (Alibaba)
- ✨ Expanded to 32 models across 7 providers

### [1.0.0] - 2026-02-16

- ✨ Initial release — TokenWatch
- ✨ Pricing table for 11 models across 5 providers
- ✨ Budget alerts: daily, weekly, monthly, per-call thresholds
- ✨ Model cost comparison, cost estimation, optimization suggestions
- ✨ Auto-hooks for Anthropic and OpenAI response objects
- ✨ Dashboard, JSON export, local-only storage, MIT licensed

---

**Last Updated**: February 16, 2026
**Current Version**: 1.2.3
**Status**: Active & Community-Maintained

© 2026 Ibrahim Saleem · [TokenLess](https://github.com/ibrahimsaleem/TokenLess)
