
class LLM:
    def __init__(self, model):
        self.model = model

    @classmethod
    def from_path(self, model_path: str):
        from llama_cpp import Llama
        return LLM(Llama(model_path, n_gpu_layers=-1))
    
    def generate(self, input_text: str):
        outputs = self.model(input_text)
        output_text = outputs["choices"][0]["text"]
        return output_text
    # {"id":"cmpl-bab2b133-cf08-43aa-8ea0-7c4b109b9cf4","object":"text_completion","created":1726721257,"model":"/Users/wumengsong/Resource/gguf/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf","choices":[{"text":" I'm a beginner and I'ts my first time playing this game. I","index":0,"logprobs":null,"finish_reason":"length"}],"usage":{"prompt_tokens":9,"completion_tokens":16,"total_tokens":25}}
    
    def generate_next_token(self):
        pass
    
    def chat(self):
        pass