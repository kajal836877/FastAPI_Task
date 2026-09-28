from sqlmodel import create_engine, Session

sqlite_url = "sqlite:///lost_found.db"

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session