from playwright.async_api import async_playwright

from src.app.core.config import settings


async def parse_with_playwright(file_path: str) -> str:
    """Получает HTML-страницу с сайта suip.biz после загрузки файла и возвращает её содержимое."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(settings.parser_url)

        await page.set_input_files('input[name="fileforsending"]', file_path)

        await page.evaluate("document.forms[0].submit();")

        await page.wait_for_selector("text=Найденные метаданные.", timeout=60000)

        html = await page.content()

        await browser.close()
        return html
