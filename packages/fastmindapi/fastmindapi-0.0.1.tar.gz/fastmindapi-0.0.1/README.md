# FastMindAPI
An easy-to-use, high-performance(?) backend for serving LLMs and other AI models, built on FastAPI.

## Quick Start

### Install

```shell
pip install fastmindapi
```

### Use

```Python
import fastmindapi as FM

client = FM.Client()
client.run()
```

## Features

### Model: Support models with various backends

- ✅ [Transformers](https://github.com/huggingface/transformers)
  - `TransformersCausalLM` ( `AutoModelForCausalLM`)

- [llama.cpp](https://github.com/abetlen/llama-cpp-python)
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

