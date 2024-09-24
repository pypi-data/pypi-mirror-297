from fastapi import FastAPI


class Api(FastAPI):
    """API接口核心类"""

    def run(self, host: str = "0.0.0.0", port: int = 8888):
        """运行程序"""
        import uvicorn
        uvicorn.run(self, host=host, port=port)
