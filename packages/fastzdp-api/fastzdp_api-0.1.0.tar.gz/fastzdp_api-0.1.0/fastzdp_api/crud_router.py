from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import SQLModel
import fastzdp_sqlmodel as fasm


def get_crud_router(
        engine: Engine,
        modelSchema: BaseModel,
        model: SQLModel,
):
    """或者增删改查的路由对象"""
    if model is None:
        return

    name = model.__name__
    path = name.lower()

    router = APIRouter(tags=[f"{name} 管理"])

    @router.post(f"/{path}", summary=f"新增 {name}")
    async def add_classes(req_data: modelSchema):
        fasm.add(engine, model(**req_data.model_dump()))
        return None

    @router.put(f"/{path}" + "/{id}", summary=f"更新 {name}")
    async def update_classes(id: int, req_data: modelSchema):
        classes = fasm.get(engine, model, id)
        if not classes:
            return JSONResponse(status_code=404, content={"error": "数据不存在"})

        fasm.update(engine, classes, req_data.model_dump())
        return None

    @router.delete(f"/{path}" + "/{id}", summary=f"删除 {name}")
    async def delete_classes(id: int):
        fasm.delete_id(engine, model, id)
        return None

    @router.get(f"/{path}", summary=f"查询 {name}")
    async def get_classes(page: int = 1, size: int = 8):
        return fasm.get_page(engine, model, page, size)

    return router
