from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://pacific_library_user:Fw1u3sIagil9R1JbUNiG9txOc4xR7eIA@dpg-cu0hf15umphs738458h0-a:5432/pacific_library"

DATABASE_URL2 = 'sqlite:///./betatesting.db'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)

Base = declarative_base()