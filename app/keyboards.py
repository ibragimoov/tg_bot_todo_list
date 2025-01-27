from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_users, get_tasks_by_user

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Просмотреть задачи'), KeyboardButton(text='Создать задачу')]
],
    resize_keyboard=True
)

def task_detail(task_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Завершить', callback_data='done_' + str(task_id)))
    keyboard.add(InlineKeyboardButton(text='Изменить', callback_data='edit_' + str(task_id)))
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data='delete_' + str(task_id)))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back'))

    return keyboard.adjust(2).as_markup()


async def get_tasks(tg_id: int):
    keyboard = InlineKeyboardBuilder()
    tasks = await get_tasks_by_user(tg_id=tg_id)

    for task in tasks:
        keyboard.add(InlineKeyboardButton(text=task.content, callback_data='task_' + str(task.id)))

    return keyboard.adjust(1).as_markup()


async def handle_users():
    all_users = await get_users()
    keyboard = InlineKeyboardBuilder()

    for user in all_users:
        keyboard.add(InlineKeyboardButton(text=str(user.tg_id), callback_data='user_' + str(user.id)))

    return keyboard.adjust(2).as_markup()