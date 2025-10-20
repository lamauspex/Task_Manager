
""" Назначение: Отображение графиков на стартовой странице """

from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from src.app.core.constants import TaskStatus
from src.app.models import Task
from src.app.core.database import get_async_session
from src.app.analytics.charts import (
    pie_chart_task_statuses,
    bar_chart_completed_tasks_per_user,
    bar_chart_active_tasks_per_user
)


templates = Jinja2Templates(directory="src/app/templates")


async def home_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    # Вызываем функции построения графиков
    pie_chart_data = await pie_chart_task_statuses(session)
    bar_chart_data = await bar_chart_completed_tasks_per_user(session)
    bar_chart_activ = await bar_chart_active_tasks_per_user(session)

    total_tasks = await session.scalar(select(func.count()).select_from(Task))

    # Количество задач в работе
    assigned_tasks = await session.scalar(
        select(func.count()).where(
            Task.status == TaskStatus.CREATED.value,
            Task.assigned_to_id.isnot(None)
        )
    )

    # Количество активных пользователей (у которых есть назначенные задачи)
    active_users_count = await session.scalar(
        select(func.count(func.distinct(Task.assigned_to_id))).where(
            Task.status == TaskStatus.CREATED.value,
            Task.assigned_to_id.isnot(None)
        )
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pie_chart": pie_chart_data,
            "bar_chart": bar_chart_data,
            "bar_activ": bar_chart_activ,
            "total_tasks": total_tasks,
            "assigned_tasks": assigned_tasks,
            "active_users_count": active_users_count
        }
    )
