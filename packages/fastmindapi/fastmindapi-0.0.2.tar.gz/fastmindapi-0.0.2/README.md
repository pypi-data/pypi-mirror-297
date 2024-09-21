# FastMindAPI
An easy-to-use, high-performance(?) backend for serving LLMs and other AI models, built on FastAPI.

## 🚀 Quick Start

### Install

```shell
pip install fastmindapi
```

### Use

#### Run the server 

```Python
import fastmindapi as FM

server = FM.Server()
server.run()
```

#### Access via client / HTTP requests

```python
import fastmindapi as FM

client = FM.Client(IP="x.x.x.x", PORT=xxx) # 127.0.0.1:8000 for default
```

```
curl http://IP:PORT/docs#/
```

> 🪧 **We primarily maintain the backend server; the client is provided for reference only.** The main usage is through sending HTTP requests. (We might release FM-GUI in the future.)

## ✨ Features

### Model: Support models with various backends

- ✅  [Transformers](https://github.com/huggingface/transformers)
  - `TransformersCausalLM` ( `AutoModelForCausalLM`)
  - `PeftCausalLM` ( `PeftModelForCausalLM` )
  
- ✅  [llama.cpp](https://github.com/abetlen/llama-cpp-python)
  - `LlamacppLM` (`Llama`)

- [MLC LLM](https://llm.mlc.ai)
- [vllm](https://github.com/vllm-project/vllm)
- ...

### Modules: More than just chatting with models

- Function Calling (extra tools in Python)
- Retrieval
- Agent
- ...

### Flexibility: Easy to Use & Highly Customizable

- Load the model when coding / runtime
- Add any APIs you want

