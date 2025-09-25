
""" Назначение: Графики, статистика """


import pandas as pd
import plotly.graph_objects as go
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.constants import TaskStatus
from src.app.core.database import get_async_session
from src.app.models import Task, User


async def pie_chart_task_statuses(
    session: AsyncSession = Depends(get_async_session)
):
    """ Количествo задач по статусам """
    statuses = {
        TaskStatus.CREATED.value: select(func.count()).where(
            Task.status == TaskStatus.CREATED.value),
        TaskStatus.IN_PROGRESS.value: select(func.count()).where(
            Task.status == TaskStatus.IN_PROGRESS.value),
        TaskStatus.COMPLETED.value: select(func.count()).where(
            Task.status == TaskStatus.COMPLETED.value)
    }

    counts = {}
    for status, query in statuses.items():
        counts[status] = await session.scalar(query)

    # Метки и значения для секторов
    labels = list(counts.keys())  # ["CREATED", "IN_PROGRESS", "COMPLETED"]
    values = list(counts.values())  # Соответствующее количество задач

    # 3D эффекты для круговой диаграммы
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=.3,  # Дырочка в центре
            textinfo='percent+value',  # Показывать проценты значения
            # Цвета для каждой секции
            marker=dict(colors=['rgb(255, 127, 14)',
                        'rgb(44, 160, 44)', 'rgb(31, 119, 180)']),
            rotation=90,  # Начальное положение сектора
            pull=[0.1, 0, 0],  # Эффект вытягивания первой секции
            opacity=0.8  # Прозрачность, добавляет ощущение глубины
        )
    ])

    # Настройка дизайна и стиля
    fig.update_traces(hoverinfo='label+percent',
                      textinfo='value+percent', textfont_size=14)
    fig.update_layout(
        title={
            'text': 'Распределение задач по статусам',
            'font': {'size': 24}
        },
        height=500, width=600
    )
    return fig.to_html(full_html=False)


async def bar_chart_completed_tasks_per_user(
    session: AsyncSession = Depends(get_async_session)
):
    """ Подсчет количества задач, выполненных каждым сотрудником """
    query = (
        select(
            Task.completed_by_id.label("employee_id"),
            func.count().label("tasks_count")
        ).where(Task.completed_by_id.isnot(None))
        .group_by(Task.completed_by_id)
    )

    result = await session.execute(query)
    data = result.all()

    if not data:
        return "<p>Нет данных для построения графика.</p>"

    df = pd.DataFrame(data, columns=["employee_id", "tasks_count"])

    # Получаем полные имена сотрудников
    user_query = select(User.id, User.first_name, User.last_name)
    users_result = await session.execute(user_query)
    df_users = pd.DataFrame(users_result.fetchall(), columns=[
                            "id", "first_name", "last_name"])

    employee_names = {}
    for _, row in df_users.iterrows():
        employee_names[row.id] = f"{row.first_name} {row.last_name}"

    df["employee"] = df["employee_id"].map(employee_names)

    colors = [
        'rgba(255, 195, 0, 0.8)',
        'rgba(218, 247, 166, 0.8)',
        'rgba(255, 87, 51, 0.8)',
        'rgba(199, 0, 57, 0.8)',
        'rgba(144, 12, 63, 0.8)'
    ]

    # Создаем красивую гистограмму
    fig = go.Figure()

    for i, emp in enumerate(df['employee']):
        fig.add_trace(go.Bar(
            x=[emp],
            y=[df.loc[i, 'tasks_count']],
            marker=dict(color=colors[i % len(colors)], line=dict(
                width=1)),  # Используем прозрачный градиент
            name=emp,
            text=str(int(df.loc[i, 'tasks_count'])) + ' задач'
        ))

    # Улучшаем внешний вид графика
    fig.update_layout(
        title={'text': 'Количество выполненных задач сотрудниками',
               'font': {'size': 24}},  # Увеличенный размер заголовка
        xaxis_title="Сотрудники",
        yaxis_title="Количество задач",
        font=dict(family="Arial", size=14),  # Шрифт
        showlegend=True,  # Показываем легенду
        margin=dict(l=50, r=50, t=80, b=50)  # Отступы вокруг графика
    )

    return fig.to_html(full_html=False)


async def bar_chart_active_tasks_per_user(
    session: AsyncSession = Depends(get_async_session)
):
    """ Количество задач назначенных сотрудникам """
    query = (
        select(
            Task.assigned_to_id.label("employee_id"),
            func.count().label("tasks_count")
        )
        .where(Task.status == TaskStatus.CREATED.value)
        .where(Task.assigned_to_id.isnot(None))
        .group_by(Task.assigned_to_id)
    )

    result = await session.execute(query)
    data = result.all()

    if not data:
        return "<p>Нет данных для построения графика.</p>"

    df = pd.DataFrame(data, columns=["employee_id", "tasks_count"])

    # Получаем полные имена сотрудников
    user_query = select(User.id, User.first_name, User.last_name)
    users_result = await session.execute(user_query)
    df_users = pd.DataFrame(users_result.fetchall(), columns=[
                            "id", "first_name", "last_name"])

    employee_names = {}
    for _, row in df_users.iterrows():
        employee_names[row.id] = f"{row.first_name} {row.last_name}"

    df["employee"] = df["employee_id"].map(employee_names)

    colors = [
        'rgba(255, 195, 0, 0.8)',
        'rgba(218, 247, 166, 0.8)',
        'rgba(255, 87, 51, 0.8)',
        'rgba(199, 0, 57, 0.8)',
        'rgba(144, 12, 63, 0.8)'
    ]

    # Создаем красивую гистограмму
    fig = go.Figure()

    for i, emp in enumerate(df['employee']):
        fig.add_trace(go.Bar(
            x=[emp],
            y=[df.loc[i, 'tasks_count']],
            marker=dict(color=colors[i % len(colors)], line=dict(
                width=1)),  # Используем прозрачный градиент
            name=emp,
            text=str(int(df.loc[i, 'tasks_count'])) + ' задач'
        ))

    # Улучшаем внешний вид графика
    fig.update_layout(
        title={'text': 'Назначенные задачи сотрудникам',
               'font': {'size': 24}},  # Увеличенный размер заголовка
        xaxis_title="Сотрудники",
        yaxis_title="Количество задач",
        font=dict(family="Arial", size=14),  # Шрифт
        showlegend=True,  # Показываем легенду
        margin=dict(l=50, r=50, t=80, b=50)  # Отступы вокруг графика
    )

    return fig.to_html(full_html=False)
