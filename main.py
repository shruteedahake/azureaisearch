from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from router import router
from fastapi_mcp import FastApiMCP
 
def apply_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
 
def create_sub_app(title: str, description: str, version: str = "0.1.0") -> FastAPI:
    app = FastAPI(title=title, description=description, version=version)
    apply_cors(app)
    return app
 
app = FastAPI()
apply_cors(app)
 
query_search = create_sub_app(
    title="Query Search",
    description="to be changed..."
)
query_search.include_router(router)
 
FastApiMCP(query_search, include_operations=["query_search"]).mount_http()
 
app.mount("risk_assesment_agent", query_search)
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6004)
