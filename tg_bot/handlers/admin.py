import logging

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot.config import Config
from database.repository import Repo
from tg_bot.filters.admin import AdminFilter

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(AdminFilter())