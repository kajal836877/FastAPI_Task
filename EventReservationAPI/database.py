from sqlmodel import create_engine, Session

sqlite_url = "sqlite:///event_reservation.db"

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session