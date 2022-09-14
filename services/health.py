from fastapi import APIRouter


# Endpoint to handle the health check
router = APIRouter(
    prefix='/api/v1'
)

# Health checker endpoint
@router.get("/health")
async def health_checker():

    return {'detail':{
                'status':'ok',
                'status_code':0,
                'version': '1.0.1'},}

# Sentry debug
@router.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0