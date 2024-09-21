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


curl http://127.0.0.1:8000/model/add_info \
  -H "Content-Type: application/json" \
  -d '{
  "model_name": "gemma2",
  "model_type": "TransformersCausalLM",
  "model_path": "/Users/wumengsong/Resource/gemma-2-2b"
}'

curl http://127.0.0.1:8000/model/load/gemma2

curl http://127.0.0.1:8000/model/call \
  -H "Content-Type: application/json" \
  -d '{
  "model_name": "gemma2",
  "input_text": "Do you know something about Dota2?",
  "max_new_tokens": 2
}'

curl http://127.0.0.1:8000/model/generate/gemma2 \
  -H "Content-Type: application/json" \
  -d '{
  "input_text": "Do you know something about Dota2?",
  "max_new_tokens": 2,
  "return_logits": true
}'
```

