import logging

import asyncio
import openai

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.repository import Repo
from tg_bot.config import Config
from tg_bot.filters.user import AddAdminFilter
from tg_bot.misc.states import CodeWriteState
from tg_bot.keyboards.user import (get_main_keyboard, get_cancel_keyboard,
                                   get_first_languages_keyboard, get_go_menu_keyboard)

from tg_bot.services.broadcaster import get_response

logger = logging.getLogger(__name__)

user_router = Router()
user_router.message.filter(F.chat.type == "private")
user_router.callback_query.filter(F.message.chat.type == "private")


langs = ["JavaScript", "Python", "C#", "C++"]
stop_loop = False


@user_router.message(CommandStart())
@user_router.callback_query(F.data == "main_menu")
async def user_start(obj: Message | CallbackQuery, repo: Repo, config: Config) -> None:
    text = f"Меню:"
    if isinstance(obj, CallbackQuery):
        await obj.message.edit_text(text=text, reply_markup=await get_main_keyboard())
    else:
        await obj.answer(text=text, reply_markup=await get_main_keyboard())
        # check_user = await repo.get_user_username(obj.chat.id)
        # if not check_user:
        #     await repo.add_user(user_id=obj.chat.id, username=obj.chat.username, first_name=None)


@user_router.callback_query(F.data == "converter")
async def set_first_lang(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    
    text = "Выберите язык, на котором написан код:"
    await call.message.edit_text(text=text, reply_markup=await get_first_languages_keyboard(turn="second", langs=langs))


@user_router.callback_query(Text(startswith='second_'))
async def set_second_lang(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()

    first_lang = call.data.split("_")[1]
    await state.set_data({"first_lang": first_lang})
    text = "Выберите язык, на который необходимо конвертировать код:"
    await call.message.edit_text(text=text, reply_markup=await get_first_languages_keyboard(turn="code", langs=langs))


@user_router.callback_query(Text(startswith='code_'))
async def set_second_lang(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    
    await state.set_state(CodeWriteState.waiting_enter_code)
    second_lang = call.data.split("_")[1]
    await state.update_data({"second_lang": second_lang})
    text = "Введите код, который необходимо конвертировать:"
    await call.message.edit_text(text=text)


@user_router.message(CodeWriteState.waiting_enter_code)
async def enter_code(message: Message, repo: Repo, state: FSMContext, config: Config, bot: Bot) -> None:
    
    state_data = await state.get_data()
    first_lang = state_data['first_lang']
    second_lang = state_data['second_lang']
    current_msg =await message.answer(text="Ожидание")

    animate_task = asyncio.create_task(animate_f(bot=bot, chat_id=message.chat.id, message_id=current_msg.message_id))
    response = await rerpons_task(lang_from=first_lang, lang_to=second_lang, code=message.text)
    await animate_task

    await current_msg.edit_text(text=response, reply_markup=await get_go_menu_keyboard())   


async def animate_f(bot: Bot, chat_id: int, message_id:int):
    steps = ["⢿","⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
    global stop_loop

    while not stop_loop:
        for i in steps:
            await bot.edit_message_text(text=f"Ожидание {i}", message_id=message_id, chat_id=chat_id)


async def rerpons_task(lang_from, lang_to, code):
    response = await get_response(lang_from, lang_to, code)

    global stop_loop
    stop_loop = True
    return response