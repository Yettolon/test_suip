from typing import List, Sequence
from fastapi import UploadFile, File
from fastapi import APIRouter

from src.app.parsers.suip_parser import parse_with_playwright
from src.app.services.suip_service import (
    extract_main_metadata,
    list_suip_data,
    save_suip_data,
    parse_metadata_from_html,
)
from src.app.schemas.suip import SuipDataRead
from src.app.db.models import SuipData

router = APIRouter(prefix="/suip-data")


@router.post("/parse", response_model=SuipDataRead)
async def parse_endpoint(file: UploadFile = File(...)) -> SuipDataRead:
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    html = await parse_with_playwright(file_path)

    parsed = await parse_metadata_from_html(html)
    result = await extract_main_metadata(parsed)

    suip_data: SuipData = await save_suip_data(result, html)
    return suip_data


@router.get("", response_model=List[SuipDataRead])
async def get_saved_data() -> Sequence[SuipData]:
    data_list: Sequence[SuipData] = await list_suip_data()
    return data_list
