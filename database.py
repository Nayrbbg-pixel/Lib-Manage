from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://pacific_library_jqt6_user:lA5XZaPTHez0foBtyhd8kKmZ3Y5UELK4@dpg-cusuv32j1k6c738838tg-a/pacific_library_jqt6"

DATABASE_URL2 = 'sqlite:///./betatesting.db'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)

Base = declarative_base()