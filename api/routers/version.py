from fastapi import APIRouter

router = APIRouter(
    prefix="/v1",
    tags=["Version"]
)

@router.get("/version", summary="Get API version", tags=["version"])
def version():
    return {"version": "1.0.4"}

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}