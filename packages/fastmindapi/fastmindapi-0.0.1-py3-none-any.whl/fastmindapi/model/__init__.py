from .transformers.CasualLM import AutoModel as TransformersCausalLM
from .llama_cpp.LLM import LLM as LlamacppLLM
from .. import logger

class ModelModule:
    def __init__(self):
        self.available_models = {}
        self.loaded_models = {}

    def load_model(self, model_name: str, model):
        self.loaded_models[model_name] = model

    def load_model_from_path(self, model_name: str):
        '''
        Load the specific model.
        '''
        model_type = self.available_models[model_name]["model_type"]
        model_path = self.available_models[model_name]["model_path"]

        logger.info("model_path:"+model_path)
        
        # 匹配模型类型
        match model_type:
            case "TransformersCausalLM":
                self.loaded_models[model_name] = TransformersCausalLM.from_path(model_path)
            case "LlamacppLLM":
                self.loaded_models[model_name] = LlamacppLLM.from_path(model_path)

