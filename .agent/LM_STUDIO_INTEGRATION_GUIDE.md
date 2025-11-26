# LM Studio Integration Guide for Agent Zero

## Problem Solved
**Error**: `litellm.AuthenticationError: Incorrect API key provided`

**Root Cause**: Agent Zero was using `lm_studio` provider which litellm doesn't recognize properly. LM Studio provides an OpenAI-compatible API that doesn't require authentication.

## Solution Applied

### 1. Configuration Changes (`data/tmp/settings.json`)

```json
{
  "chat_model_provider": "openai",
  "chat_model_name": "llama-3.2-3b-instruct",
  "chat_model_api_base": "http://192.168.0.32:7002/v1",
  
  "util_model_provider": "openai",
  "util_model_name": "llama-3.2-3b-instruct",
  "util_model_api_base": "http://192.168.0.32:7002/v1",
  
  "browser_model_provider": "openai",
  "browser_model_name": "llama-3.2-3b-instruct",
  "browser_model_api_base": "http://192.168.0.32:7002/v1",
  
  "api_keys": {
    "openai": "not-needed"
  },
  
  "litellm_global_kwargs": {
    "drop_params": true
  }
}
```

### 2. Key Changes

| Setting | Before | After | Reason |
|---------|--------|-------|--------|
| `*_model_provider` | `lm_studio` | `openai` | Use OpenAI-compatible mode |
| `*_model_name` | `llama3.2?3b` | `llama-3.2-3b-instruct` | Fixed model name typo |
| `*_model_api_base` | Empty | `http://192.168.0.32:7002/v1` | Point to LM Studio server |
| `api_keys.openai` | Not set | `"not-needed"` | Dummy key to satisfy litellm |
| `litellm_global_kwargs` | `{}` | `{"drop_params": true}` | Ignore auth params |

## How It Works

### LM Studio Server
- **Address**: `http://192.168.0.32:7002`
- **API Endpoint**: `/v1` (OpenAI-compatible)
- **Model**: `llama-3.2-3b-instruct`
- **Authentication**: None required

### Litellm Integration
Litellm is used by Agent Zero to provide a unified interface to different LLM providers. For LM Studio:

1. **Provider**: Uses `openai` provider (not `lm_studio`)
2. **API Base**: Points to your LM Studio server at `http://192.168.0.32:7002/v1`
3. **API Key**: Set to dummy value `"not-needed"` to prevent litellm from complaining
4. **Drop Params**: Enabled to ignore authentication parameters

## Verification Steps

### 1. Test LM Studio Server
```bash
# Should return model information
curl http://192.168.0.32:7002/v1/models

# Test completion endpoint
curl http://192.168.0.32:7002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.2-3b-instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 2. Check Agent Zero Logs
```bash
docker-compose logs -f agent-zero-unity
```

Look for successful model initialization without authentication errors.

### 3. Test in Web UI
1. Go to http://localhost:50001
2. Send a test message
3. Verify response comes from LM Studio model

## Alternative Configuration

### If Using LM Studio on Different IP
Update all `*_model_api_base` fields:
```json
{
  "chat_model_api_base": "http://YOUR_IP:PORT/v1",
  "util_model_api_base": "http://YOUR_IP:PORT/v1",
  "browser_model_api_base": "http://YOUR_IP:PORT/v1"
}
```

### If Using Different Model
Update all `*_model_name` fields to match your loaded model:
```json
{
  "chat_model_name": "your-model-name",
  "util_model_name": "your-model-name",
  "browser_model_name": "your-model-name"
}
```

## Common Issues

### Issue: Still Getting Auth Errors
**Solution**: Ensure `api_keys.openai` is set to any non-empty string:
```json
"api_keys": {
  "openai": "sk-anything-works"
}
```

### Issue: Connection Refused
**Cause**: LM Studio server not accessible from Docker container

**Solution**: 
1. Use host IP (not localhost) in container
2. Add to docker-compose if needed:
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Then use: `http://host.docker.internal:7002/v1`

### Issue: Wrong Model Name
**Cause**: Model name doesn't match what's loaded in LM Studio

**Solution**: 
1. Check LM Studio's API identifier
2. Try generic name: `gpt-3.5-turbo` (many local models accept this)
3. Use exact model name from LM Studio

## Performance Tips

### 1. Model Selection
For Agent Zero, consider:
- **Chat Model**: Larger model (7B-13B) for better reasoning
- **Util Model**: Smaller model (3B) for quick tasks
- **Browser Model**: Medium model (3B-7B)

### 2. Context Length
Adjust based on your model's capabilities:
```json
{
  "chat_model_ctx_length": 8192,
  "util_model_ctx_length": 8192
}
```

### 3. Temperature
For consistent behavior:
```json
{
  "chat_model_kwargs": {
    "temperature": "0"
  }
}
```

## Environment Variables Alternative

Instead of editing `settings.json`, you can use environment variables:

```bash
# In .env file or docker-compose.yml
CHAT_MODEL_PROVIDER=openai
CHAT_MODEL_NAME=llama-3.2-3b-instruct
CHAT_MODEL_API_BASE=http://192.168.0.32:7002/v1
OPENAI_API_KEY=not-needed
```

## Testing Script

```python
# test_lmstudio.py
from litellm import completion

response = completion(
    model="openai/llama-3.2-3b-instruct",
    api_base="http://192.168.0.32:7002/v1",
    api_key="not-needed",
    messages=[{"role": "user", "content": "Hello, test"}],
    drop_params=True
)

print(response.choices[0].message.content)
```

Run with:
```bash
docker exec agent-zero-unity python test_lmstudio.py
```

---

**Status**: ✅ **Configuration Complete**

**Next Step**: Restart Agent Zero container to apply changes:
```bash
docker-compose restart agent-zero-unity
```

Then test at: http://localhost:50001

