import logging

import openai
import asyncio

from aiogram import Bot
from aiogram.types import Message


async def get_response(lang_from, lang_to, code):
    logging.info("Resp")
    response = await openai.Completion.acreate(
    model="text-davinci-003",
    prompt=f"#{lang_from} to {lang_to}:\n{code}",
    temperature=0,
    max_tokens=64,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    return response["choices"][0]["text"]