from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select

from database import engine, get_session
from models import Event, Reservation
from schemas import EventCreate, EventUpdate, ReservationCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


# Create event
@app.post("/events")
def create_event(
    event_data: EventCreate,
    session: Session = Depends(get_session)
):
    event = Event(
        title=event_data.title,
        venue=event_data.venue,
        capacity=event_data.capacity,
        organizer=event_data.organizer,
        status=event_data.status
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


# Get all events
@app.get("/events")
def get_events(session: Session = Depends(get_session)):
    events = session.exec(select(Event)).all()

    return events


# Get event by ID
@app.get("/events/{event_id}")
def get_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# Update event
@app.put("/events/{event_id}")
def update_event(
    event_id: int,
    event_data: EventUpdate,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    event.title = event_data.title
    event.venue = event_data.venue
    event.capacity = event_data.capacity
    event.organizer = event_data.organizer
    event.status = event_data.status

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


# Delete event
@app.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    session.delete(event)
    session.commit()

    return {"message": "Event deleted successfully"}


# Reserve a seat
@app.post("/events/{event_id}/reserve")
def reserve_seat(
    event_id: int,
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session)
):
    # Check if event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Check if event is open
    if event.status != "Open":
        raise HTTPException(
            status_code=400,
            detail="Event is closed"
        )

    # Count existing reservations
    reservations = session.exec(
        select(Reservation).where(
            Reservation.event_id == event_id
        )
    ).all()

    booked = len(reservations)

    # Prevent overbooking
    if booked >= event.capacity:
        raise HTTPException(
            status_code=400,
            detail="Event is full"
        )

    reservation = Reservation(
        event_id=event_id,
        student_name=reservation_data.student_name,
        roll_number=reservation_data.roll_number,
        email=reservation_data.email
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


# Get event reservations
@app.get("/events/{event_id}/reservations")
def get_reservations(
    event_id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    reservations = session.exec(
        select(Reservation).where(
            Reservation.event_id == event_id
        )
    ).all()

    return reservations


# Cancel reservation
@app.delete("/reservations/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    session: Session = Depends(get_session)
):
    reservation = session.get(Reservation, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    session.delete(reservation)
    session.commit()

    return {"message": "Reservation cancelled successfully"}


# Check availability
@app.get("/events/{event_id}/availability")
def get_availability(
    event_id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    reservations = session.exec(
        select(Reservation).where(
            Reservation.event_id == event_id
        )
    ).all()

    booked = len(reservations)
    remaining = event.capacity - booked

    return {
        "capacity": event.capacity,
        "booked": booked,
        "remaining": remaining
    }