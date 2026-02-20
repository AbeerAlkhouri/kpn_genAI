from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers.agent import router as agent_router
import logging
from app.services.ingestion_service import ingestion_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
#application startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    ingestion_service.initialize_vector_store()
    yield


app = FastAPI( title="KPN GenAI Agent",
    version="1.0.0",lifespan=lifespan)

#Routers initialization
app.include_router(agent_router)



