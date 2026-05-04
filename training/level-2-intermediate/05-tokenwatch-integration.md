# Lesson: TokenWatch integration

**Level:** Intermediate — Level 2  
**Time:** 30 minutes  
**Prerequisites:** [04-session-management.md](04-session-management.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Integrate `tokenwatch.py` into an existing Python application in under 10 minutes.
2. Use provider helper methods (`record_from_anthropic_response`, `record_from_openai_response`) correctly.
3. Set meaningful budgets and alert thresholds.
4. Read the dashboard output and act on the top-5 expensive task labels.

---

## Why TokenWatch for local development

`tokenwatch.py` is zero-dependency (standard library only). It records usage to a local JSON file and computes cost from a built-in pricing table. It is not a replacement for production billing dashboards, but it is the fastest way to:

- See which task types are consuming the most tokens during development.
- Test budget enforcement before any production traffic.
- Compare model costs on real-world request shapes (not synthetic benchmarks).

---

## Minimal integration pattern

```python
from tokenwatch import TokenWatch

# Initialize once at app startup
monitor = TokenWatch(storage_path=".tokenwatch")
monitor.set_budget(monthly_usd=50.0, alert_at_percent=80.0)

# After any API call — manual recording
monitor.record_usage(
    model="claude-haiku-4-5-20251001",
    input_tokens=1200,
    output_tokens=400,
    task_label="summarize"
)

# Print dashboard to terminal
print(monitor.format_dashboard())
```

The `storage_path` is a local directory. TokenWatch creates it if it does not exist. All data stays on disk — nothing leaves the machine.

---

## Using provider helper methods

If you use the Anthropic or OpenAI Python SDK, pass the full response object to the helper method instead of extracting token counts manually:

### Anthropic

```python
import anthropic
from tokenwatch import TokenWatch

client = anthropic.Anthropic()
monitor = TokenWatch(storage_path=".tokenwatch")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    messages=[{"role": "user", "content": "Summarize this: ..."}]
)

# TokenWatch reads token counts and model from the response object
monitor.record_from_anthropic_response(response, task_label="summarize")
```

### OpenAI

```python
from openai import OpenAI
from tokenwatch import TokenWatch

client = OpenAI()
monitor = TokenWatch(storage_path=".tokenwatch")

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role": "user", "content": "Classify this message: ..."}],
    max_tokens=20
)

monitor.record_from_openai_response(response, task_label="classify")
```

### Generic providers (any JSON API)

```python
def record_generic(monitor, model_id: str, usage: dict, task_label: str = None):
    inp = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
    out = usage.get("completion_tokens") or usage.get("output_tokens") or 0
    monitor.record_usage(model_id, int(inp), int(out), task_label=task_label)
```

Call this after any provider's response, extracting the usage field from the response JSON.

---

## Setting meaningful budgets

The budget alert prevents surprise cost spikes during development or CI. Set it to a value that would trigger concern if exceeded in a sprint:

```python
# For a small dev team doing integration testing
monitor.set_budget(monthly_usd=25.0, alert_at_percent=75.0)

# For a team running load tests
monitor.set_budget(monthly_usd=200.0, alert_at_percent=50.0)
```

When the alert fires, `format_dashboard()` includes a warning line. You can also check programmatically:

```python
status = monitor.get_budget_status()
if status["alert_triggered"]:
    logger.warning("Token budget alert: %.1f%% used", status["percent_used"])
```

---

## Reading the dashboard

`monitor.format_dashboard()` prints a table like:

```
===== TokenWatch Dashboard =====
Period: 2026-05-01 to 2026-05-04
Budget: $25.00/month | Used: $3.47 (13.9%) | Alert at: 75.0%

Model                           | In (k)  | Out (k) | Cost
--------------------------------|---------|---------|--------
claude-haiku-4-5-20251001       |  145.2  |   48.6  |  $0.82
claude-sonnet-4-5-20251015      |   32.1  |   18.4  |  $2.65
Total                           |  177.3  |   67.0  |  $3.47

Top task labels by cost:
  codegen         $1.42 (40.9%)
  summarize       $0.88 (25.4%)
  qa              $0.71 (20.5%)
  classify        $0.33 ( 9.5%)
  other           $0.13 ( 3.7%)
```

**What to do with this:**

1. Find the top 2–3 task labels by cost. Ask: is this expected given their importance?
2. Check whether `codegen` (usually a mid/large task) is routed to the right model.
3. If `classify` is appearing in a MID model, fix the routing — it should be SMALL.
4. If `other` is above 10%, add more specific task labels to understand what it contains.

---

## Exercise

1. Open or create a Python script that makes one API call.
2. Import TokenWatch and add `record_from_<provider>_response` immediately after the API call.
3. Run the script 5 times with different prompts (to simulate varied requests).
4. Call `monitor.format_dashboard()` and print it.
5. Export the results: `python ../../scripts/estimate-cost.py` — paste the output into your team wiki (no PII in usage stats).

---

## You know this lesson when…

- You have `tokenwatch.py` integrated in at least one script or route in your project.
- You can read the dashboard output and identify which task label to investigate.
- You have set a budget alert appropriate to your development spend expectations.

---

## Continue

- [../level-3-expert/README.md](../level-3-expert/README.md) — advanced architecture patterns
- Root SKILL.md for full API reference: [../../SKILL.md](../../SKILL.md)
