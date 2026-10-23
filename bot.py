import asyncio
import os
import re
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8973896748:AAHUMFRWyQ8MOFEPimaU7DwNScGKQ9SoQa4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def resolve_sfl(target_url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": target_url
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(target_url, allow_redirects=True, timeout=10) as response:
                final_url = str(response.url)
                html = await response.text()
                match_meta = re.search(r'content=["\'][0-9];url=([^"\']+)["\']', html, re.IGNORECASE)
                if match_meta:
                    return match_meta.group(1)
                match_js = re.search(r'window\.location\.href\s*=\s*["\']([^"\']+)["\']', html)
                if match_js:
                    return match_js.group(1)
                return final_url
        except Exception as e:
            return f"Gagal nge-resolve link: {str(e)}"

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Kirim link SFL-nya, bro. Nanti gua bersihin iklannya.")

@dp.message(F.text.startswith("http"))
async def handle_link(message: Message):
    wait_msg = await message.answer("Nge-bypass iklan...")
    target = message.text.strip()
    result = await resolve_sfl(target)
    await wait_msg.edit_text(f"🔗 **Link Asli:**\n{result}", disable_web_page_preview=True)

async def main():
    print("[+] Bot SFL Resolver jalan...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
