```
curl http://127.0.0.1:8000/available_models
curl http://127.0.0.1:8000/loaded_models

curl http://127.0.0.1:8000/model/add_info \
  -H "Content-Type: application/json" \
  -d '{
  "model_name": "llama3",
  "model_type": "LlamacppLLM",
  "model_path": "/Users/wumengsong/Resource/gguf/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
}'

curl http://127.0.0.1:8000/model/load/llama3

curl http://127.0.0.1:8000/model/generate \
  -H "Content-Type: application/json" \
  -d '{
  "model_name": "llama3",
  "prompt": "Do you know something about Dota2?"
}'

```

