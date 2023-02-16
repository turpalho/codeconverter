from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


async def get_main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="🔄  Code convert", callback_data="converter"),
        InlineKeyboardButton(text="ℹ  Instruction", callback_data="helper"),
        InlineKeyboardButton(text="™  About", callback_data="info")
    ])
    kb.adjust(1)
    return kb.as_markup()


async def get_cancel_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="🔙  Back", callback_data="main_menu"),
    ])
    kb.adjust(1)
    return kb.as_markup()


async def get_go_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ])
    kb.adjust(1)
    return kb.as_markup()


async def get_first_languages_keyboard(turn: str, langs: List) -> InlineKeyboardMarkup:
    langs_btns = []
    for lang in langs:
        langs_btns.append(InlineKeyboardButton(text=f"{lang}", callback_data=f"{turn}_{lang}"))
    langs_btns.append(InlineKeyboardButton(text="🔙  Назад", callback_data="main_menu"))
    kb = InlineKeyboardBuilder()
    kb.add(*langs_btns)
    kb.adjust(1)
    return kb.as_markup()


async def get_invite_link_keyboard(link) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Перейти", url=link))
    return kb.as_markup()