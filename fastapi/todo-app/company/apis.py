from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_company_name():
    return {'name': 'This is a company nam'}