# 📡 API Specification

## Endpoint: `/v1/reason`
**Method:** `POST`  
**Auth:** `X-API-Key`

### Request Body
```json
{
  "prompt": "string",
  "stream": "boolean"
}
```

### Response Body
```json
{
  "status": "success",
  "cognitive_state": {
    "goal": "string",
    "confidence": "float",
    "reflection": "string"
  }
}
```
