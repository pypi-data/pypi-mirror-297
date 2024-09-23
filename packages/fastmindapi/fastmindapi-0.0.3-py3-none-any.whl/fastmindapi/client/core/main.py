from .http_request import HTTPRequest


class Client:
    def __init__(self, IP: str="127.0.0.1", PORT: int=8000):
        self.address = IP + ":" + str(PORT)
        self.request = HTTPRequest(self.address)

    def add_model_info_list(self, model_info_list: list):
        for model_info in model_info_list:
            response = self.request.post("/model/add_info", data=model_info)

    def load_model(self, model_name: str):
        response = self.request.get(f"/model/load/{model_name}")

    def unload_model(self, model_name: str):
        response = self.request.get(f"/model/unload/{model_name}")

    def generate(self, model_name: str, data: dict={}):
        response = self.request.post(f"/model/generate/{model_name}", data=data)
        return response
