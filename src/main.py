from fastapi import FastAPI
import uvicorn
from menus.router import router as router_menus


app = FastAPI()

app.include_router(router_menus, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
