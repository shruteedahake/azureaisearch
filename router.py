from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from handler import ai_search
 
router = APIRouter()
 
class querySearchRequest(BaseModel):
    AgentName: str = Field(default="RiskAssesmentAgent", description=("The unique agent name of the agent that is being called"))
    UserId: str = Field(default="markRuffalo", description=("The unique user id of a specific user (default: 'markRuffalo')."))
    query: str = Field(..., description=("Query written by user."))
 
@router.post("/query_search_mcp", operation_id="query_search_mcp")
async def search_using_azure_ai(p_body: querySearchRequest):
    try:
        result = await ai_search(p_body.query)
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": 1,
                "result": result
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": 1,
                "error": str(e)
            },
            status_code=500
        )
 
