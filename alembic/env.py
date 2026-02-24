from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import Base
from app.models import Activity # noqa

config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Создаём движок вручную, как в Wallet
    connectable = create_engine(settings.DATABASE_URL)
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()