import re
from typing import Sequence
from bs4 import BeautifulSoup
from sqlalchemy.future import select

from src.app.db.models import SuipData
from src.app.db.database import AsyncSessionLocal


async def parse_metadata_from_html(html: str) -> dict:
    """Извлекает метаданные из HTML-страницы, полученной с сайта suip.biz."""
    soup = BeautifulSoup(html, "html.parser")

    attempt_tag = soup.find(
        "b", string=re.compile(r"Найденные метаданные\. Попытка #1")
    )
    if not attempt_tag:
        raise ValueError("Не найдена секция 'Найденные метаданные. Попытка #1'")

    pre_tag = attempt_tag.find_next("pre")
    if not pre_tag:
        raise ValueError("Не найден блок <pre> с метаданными")

    raw_text = pre_tag.text.strip()
    result: dict[str, dict[str, str]] = {}
    current_section = None

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        section_match = re.match(r"^-{4}\s*(.+?)\s*-{4}$", line)
        if section_match:
            current_section = section_match.group(1).strip()
            result[current_section] = {}
            continue

        if current_section and ":" in line:
            key, value = line.split(":", 1)
            result[current_section][key.strip()] = value.strip()

    return result


async def extract_main_metadata(parsed: dict) -> dict:
    """Извлекает основные метаданные из распарсенного словаря."""
    system = parsed.get("System", {})
    file = parsed.get("File", {})

    return {
        "filename": system.get("Название файла"),
        "size": system.get("Размер файла"),
        "modified_at": system.get("Дата редактирования файла"),
        "accessed_at": system.get("Дата последнего доступа к файлу"),
        "file_type": file.get("Тип файла"),
        "mime_type": file.get("MIME тип"),
    }


async def save_suip_data(data: dict, raw_html: str) -> SuipData:
    """Сохраняет данные в базу данных и возвращает объект SuipData."""
    async with AsyncSessionLocal() as session:
        obj = SuipData(
            filename=data["filename"],
            size=data["size"],
            modified_at=data["modified_at"],
            accessed_at=data["accessed_at"],
            file_type=data["file_type"],
            mime_type=data["mime_type"],
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj


async def list_suip_data() -> Sequence[SuipData]:
    """Возвращает список всех сохраненных данных из базы данных."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(SuipData))
        return result.scalars().all()
