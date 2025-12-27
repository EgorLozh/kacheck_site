from fastapi import APIRouter

from .auth import router as auth_router
from .exercises import router as exercises_router
from .muscle_groups import router as muscle_groups_router
from .training_templates import router as training_templates_router
from .trainings import router as trainings_router
from .analytics import router as analytics_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(exercises_router)
api_router.include_router(muscle_groups_router)
api_router.include_router(training_templates_router)
api_router.include_router(trainings_router)
api_router.include_router(analytics_router)

