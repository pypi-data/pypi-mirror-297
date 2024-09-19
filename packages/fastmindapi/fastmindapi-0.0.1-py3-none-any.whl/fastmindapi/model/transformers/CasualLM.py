
class AutoModel:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        pass

    @classmethod
    def from_path(self, model_path: str):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        return AutoModel(AutoTokenizer.from_pretrained(model_path),
                         AutoModelForCausalLM.from_pretrained(model_path, device_map="auto"))

    def generate(self, input_text: str):
        output_text = self.model.generate(input_text)
        return output_text
    
    def generate_next_token(self):
        pass

    def chat(self):
        pass