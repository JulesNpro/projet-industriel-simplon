from fastapi import APIRouter

router = APIRouter()

@router.get("/datasasia")
def get_all_datas():
    return [{"id": 1, "message": "Test data"}]
