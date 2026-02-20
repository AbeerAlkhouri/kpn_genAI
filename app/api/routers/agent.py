from fastapi import APIRouter, HTTPException
from app.api.schemas.agent_schema import QueryResponse, QueryRequest
from app.services.agent_service import agent_service

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/query",  summary="Query the Intelligent Agent",
    description="Processes user input and conversational history through the AI agent to generate context-aware responses.",response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    try:
        output = await agent_service.run_agent(
            user_input=request.input,
            chat_history=request.chat_history
        )
        return QueryResponse(output=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

