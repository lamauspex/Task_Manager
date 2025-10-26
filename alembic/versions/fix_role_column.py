"""fix_role_column

Revision ID: fix_role_column
Revises: fd70f2a1b9f6
Create Date: 2025-10-27 00:06:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fix_role_column'
down_revision: Union[str, Sequence[str], None] = 'fd70f2a1b9f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Изменяем колонку role с Enum на String
    # Для SQLite нужно пересоздать таблицу
    op.execute("PRAGMA foreign_keys=off")
    
    # Создаем временную таблицу
    op.execute("""
        CREATE TABLE users_new (
            id VARCHAR(36) PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(10) NOT NULL DEFAULT 'USER',
            active BOOLEAN NOT NULL DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Копируем данные
    op.execute("""
        INSERT INTO users_new (id, first_name, last_name, email, password_hash, role, active, created_at, updated_at)
        SELECT id, first_name, last_name, email, password_hash, role, active, created_at, updated_at FROM users
    """)
    
    # Удаляем старую таблицу
    op.drop_table('users')
    
    # Переименовываем новую таблицу
    op.execute("ALTER TABLE users_new RENAME TO users")
    
    # Создаем индекс
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    op.execute("PRAGMA foreign_keys=on")


def downgrade() -> None:
    """Downgrade schema."""
    # Возвращаемся к Enum
    op.execute("PRAGMA foreign_keys=off")
    
    op.execute("""
        CREATE TABLE users_new (
            id VARCHAR(36) PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(10) NOT NULL DEFAULT 'USER',
            active BOOLEAN NOT NULL DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute("""
        INSERT INTO users_new (id, first_name, last_name, email, password_hash, role, active, created_at, updated_at)
        SELECT id, first_name, last_name, email, password_hash, role, active, created_at, updated_at FROM users
    """)
    
    op.drop_table('users')
    op.execute("ALTER TABLE users_new RENAME TO users")
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    op.execute("PRAGMA foreign_keys=on")