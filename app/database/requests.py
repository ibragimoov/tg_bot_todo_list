from app.database.models import async_session
from app.database.models import User, Task
from sqlalchemy import select


async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))


async def get_tasks_by_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            print('Пользователь не найден')
            return

        return await session.scalars(select(Task).where(Task.user_id == user.id))


async def get_task_by_id(task_id: int):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == task_id))

        if not task:
            print('Задача не найдена')
            return

        return task


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_task(content: str, tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            print('Пользователь не найден')
            return

        task = Task(content=content, user_id=user.id)

        session.add(task)
        await session.commit()


async def update_task_done(task_id: int):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == task_id))

        if not task:
            print('Задача не найдена')
            return

        task.completed = True

        await session.commit()


async def update_task_content(task_id: int, content: str):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == task_id))

        if not task:
            print('Задача не найдена')
            return

        task.content = content
        task.completed = False

        await session.commit()


async def delete_task(task_id: int):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == task_id))

        await session.delete(task)
        await session.commit()