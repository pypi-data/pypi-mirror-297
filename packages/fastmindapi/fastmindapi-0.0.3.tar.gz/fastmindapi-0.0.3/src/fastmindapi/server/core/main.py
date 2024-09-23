from . import app
from ...model import ModelModule
from ..router.basic import get_basic_router
from ..router.model import get_model_router

from ... import logger

class Server:
    def __init__(self):
        self.logger = logger

        # 设置FastAPI服务
        self.app = app
        # 将 Server 实例存储到 app.state
        self.app.state.server = self
        self.port = 8000
        self.deploy_mode = "uvicorn"
        self.local_mode = False

        # 加载模块
        self.module = dict()
        self.module["model"] = ModelModule()

        # 加载路由
        self.app.include_router(get_basic_router())
        self.app.include_router(get_model_router())


    # def load_model(self, model_name: str, model):
    #     self.module["model"].load_model(model_name, model)

    def run(self):
        match self.deploy_mode:
            case "uvicorn":
                import uvicorn
                self.logger.info("Running the client in PORT: "+str(self.port))
                uvicorn.run(self.app, 
                            host='0.0.0.0' if not self.local_mode else "127.0.0.1", 
                            port=self.port,
                            log_config=None)
                self.logger.info("Client stops running.")
                
    