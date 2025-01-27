from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class EditTaskState(StatesGroup):
    new_content = State()


@router.callback_query(F.data.startswith('edit_'))
async def handle_edit_task(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditTaskState.new_content)

    # 'edit_123'
    task_id = int(callback.data.split('_')[1])
    await state.update_data(task_id=task_id)

    await callback.message.answer('Введите новое название задачи')


@router.message(EditTaskState.new_content)
async def handle_new_content(message: Message, state: FSMContext):
    new_content = message.text

    await state.update_data(new_content=new_content)

    task_info = await state.get_data()

    await rq.update_task_content(int(task_info['task_id']), task_info['new_content'])

    task = await rq.get_task_by_id(int(task_info['task_id']))

    if task.completed:
        status = 'Завершена'
    else:
        status = 'Не готова'

    await message.answer(f'Задача: {task.content}\nСтатус: {status}', reply_markup=kb.task_detail(task.id))



class CreateTaskState(StatesGroup):
    content = State()


@router.message(F.text == 'Создать задачу')
async def handle_get_tasks(message: Message, state: FSMContext):
    await state.set_state(CreateTaskState.content)
    await message.answer('Введите текст задачи')


@router.message(CreateTaskState.content)
async def handle_task_content(message: Message, state: FSMContext):
    content = message.text

    await rq.set_task(content=content, tg_id=message.from_user.id)

    await message.answer('Задача успешно создана')

    await state.clear()


@router.callback_query(F.data.startswith('task_'))
async def handle_task_details(callback: CallbackQuery):
    # 'task_123'
    task_id = int(callback.data.split('_')[1])

    task = await rq.get_task_by_id(task_id)

    if task.completed:
        status = 'Завершена'
    else:
        status = 'Не готова'

    await callback.message.edit_text(f'Задача: {task.content}\nСтатус: {status}', reply_markup=kb.task_detail(task.id))


@router.callback_query(F.data == 'back')
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text('Все задачи:', reply_markup=await kb.get_tasks(callback.message.chat.id))


@router.callback_query(F.data.startswith('done_'))
async def handle_task_details_done(callback: CallbackQuery):
    # 'done_123'
    task_id = int(callback.data.split('_')[1])

    await rq.update_task_done(task_id)

    task = await rq.get_task_by_id(task_id)

    if task.completed:
        status = 'Завершена'
    else:
        status = 'Не готова'

    await callback.message.edit_text(f'Задача: {task.content}\nСтатус: {status}', reply_markup=kb.task_detail(task.id))


@router.callback_query(F.data.startswith('delete_'))
async def handle_delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[1])

    await rq.delete_task(task_id)

    await callback.message.edit_text('Все задачи:', reply_markup=await kb.get_tasks(callback.message.chat.id))


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в бота для управления задачами', reply_markup=kb.main)


@router.message(F.text == 'Просмотреть задачи')
async def handle_get_tasks(message: Message):
    await message.answer('Все задачи:', reply_markup=await kb.get_tasks(message.from_user.id))


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())

#
#

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])

    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Все товары из категории', reply_markup=await kb.items(category_id))


@router.message(F.text == 'Пользователи')
async def hndle_users(message: Message):
    await message.answer('Все пользователи: ', reply_markup=await kb.handle_users())
