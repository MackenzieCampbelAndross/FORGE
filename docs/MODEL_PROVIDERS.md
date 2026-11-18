# FORGE Model Provider Architecture & Resilience

FORGE v1.0 separates architectural reasoning and agent coordination from specific model APIs via an extensible provider layer (`forge.core.model_provider.ModelProvider`).

---

## 1. Supported Model Providers

| Provider | Class | Primary Protocol | Target Environments |
| :--- | :--- | :--- | :--- |
| **Google Gemini** | `GeminiProvider` | Modern Google GenAI SDK | Cloud, Google Cloud Vertex / Studio |
| **Local Ollama** | `OllamaProvider` | HTTP REST (`:11434`) | Air-gapped, local workstation, GPU clusters |
| **OpenAI / Compatible** | `OpenAIProvider` | HTTPS (`api.openai.com/v1`) | OpenAI, Azure OpenAI, Groq, Together, vLLM |
| **Anthropic Claude** | `AnthropicProvider` | HTTPS (`api.anthropic.com/v1`) | Claude 3.5 Sonnet, Claude 3 Opus |
| **Deterministic Mock** | `MockModelProvider` | In-memory | Automated CI/CD, regression testing, FEB benchmark |

---

## 2. Configuration & Initialization

### Environment Variables

```bash
# Provider Selection
FORGE_MODEL_PROVIDER=gemini       # Options: gemini, ollama, openai, anthropic, mock

# Credentials
GEMINI_API_KEY="your-gemini-key"
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"

# Local Ollama Host
OLLAMA_BASE_URL="http://localhost:11434"
```

### Programmatic Factory Usage

```python
from forge.core.model_provider import get_model_provider

# 1. Automatic from settings:
provider = get_model_provider()

# 2. Local Ollama:
ollama_provider = get_model_provider("ollama", model_name="llama3.1:70b")

# 3. OpenAI GPT-4o:
openai_provider = get_model_provider("openai", api_key="sk-...", model_name="gpt-4o")

# 4. Anthropic Claude:
claude_provider = get_model_provider("anthropic", api_key="sk-ant-...", model_name="claude-3-5-sonnet-20241022")
```

---

## 3. Resilience and Fault Tolerance

### Automatic Provider Failover (`FallbackModelProvider`)

In mission-critical engineering pipelines, transient upstream outages or rate limits must not halt blueprint synthesis. FORGE provides a transparent multi-provider fallback wrapper:

```python
from forge.core.model_provider import FallbackModelProvider, GeminiProvider
from forge.core.providers.ollama import OllamaProvider

primary = GeminiProvider()
secondary = OllamaProvider(model_name="llama3.1:8b")

# Automatically catches ProviderTimeoutError / ModelProviderError and fails over
resilient_provider = FallbackModelProvider(primary=primary, secondary=secondary)
```

### Rate Limiting (`TokenBucketRateLimiter`)

Enforces client-side rate limits using a token bucket algorithm to prevent 429 penalties:

```python
from forge.core.rate_limiter import TokenBucketRateLimiter

# Allow 10 requests per second with burst capacity of 30
limiter = TokenBucketRateLimiter(rate_per_second=10.0, capacity=30.0)

# Blocking acquire with timeout
limiter.acquire(tokens=1, timeout=5.0)
```

### Exponential Backoff with Jitter (`ExponentialBackoff`)

Mitigates thundering-herd issues on distributed API gateways with four jitter modes:
- `FULL`: Uniformly distributed random delay between 0 and exponential ceiling
- `EQUAL`: Half fixed delay + half uniform random delay
- `DECORRELATED`: Delay based on previous retry duration
- `NONE`: Deterministic exponential progression

```python
from forge.core.backoff import ExponentialBackoff, JitterMode

backoff = ExponentialBackoff(
    base_delay=1.0,
    max_delay=30.0,
    factor=2.0,
    jitter_mode=JitterMode.FULL
)

response = backoff.retry(api_call_function, max_retries=4)
```
