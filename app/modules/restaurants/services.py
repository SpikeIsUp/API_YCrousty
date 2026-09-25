"""Regles metier du module restaurants."""

from sqlalchemy.orm import Session

from app.modules.restaurants.models import Restaurant
from app.modules.restaurants.schemas import (
    RestaurantAvailabilityUpdate,
    RestaurantUpdate,
)


def get_restaurants(db: Session) -> list[Restaurant]:
    """Retourne tous les restaurants."""
    return db.query(Restaurant).all()


def get_restaurant(db: Session, restaurant_id: int) -> Restaurant | None:
    """Retourne un restaurant a partir de son identifiant."""
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def update_restaurant(
    db: Session,
    restaurant: Restaurant,
    restaurant_data: RestaurantUpdate,
) -> Restaurant:
    """Modifie les informations d'un restaurant."""

    update_data = restaurant_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)

    return restaurant


def update_availability(
    db: Session,
    restaurant: Restaurant,
    availability_data: RestaurantAvailabilityUpdate,
) -> Restaurant:
    """Modifie la disponibilite d'un restaurant."""

    restaurant.is_open = availability_data.is_open

    db.commit()
    db.refresh(restaurant)

    return restaurant


def seed_restaurants(db: Session) -> None:
    """Cree les restaurants par defaut s'ils n'existent pas deja."""

    restaurants = [
        {
            "name": "Ytasty Crousty Aix",
            "city": "Aix-en-Provence",
            "address": "1 rue Ytasty",
            "is_open": True,
            "opening_hours": {
                "monday": "11:00-23:00",
                "tuesday": "11:00-23:00",
                "wednesday": "11:00-23:00",
                "thursday": "11:00-23:00",
                "friday": "11:00-23:00",
                "saturday": "11:00-23:00",
                "sunday": "11:00-23:00",
            },
            "contact": "0100000001",
        },
        {
            "name": "Ytasty Crousty Lyon",
            "city": "Lyon",
            "address": "2 rue Ytasty",
            "is_open": True,
            "opening_hours": {
                "monday": "11:00-23:00",
                "tuesday": "11:00-23:00",
                "wednesday": "11:00-23:00",
                "thursday": "11:00-23:00",
                "friday": "11:00-23:00",
                "saturday": "11:00-23:00",
                "sunday": "11:00-23:00",
            },
            "contact": "0100000002",
        },
        {
            "name": "Ytasty Crousty Paris",
            "city": "Paris",
            "address": "3 rue Ytasty",
            "is_open": True,
            "opening_hours": {
                "monday": "11:00-23:00",
                "tuesday": "11:00-23:00",
                "wednesday": "11:00-23:00",
                "thursday": "11:00-23:00",
                "friday": "11:00-23:00",
                "saturday": "11:00-23:00",
                "sunday": "11:00-23:00",
            },
            "contact": "0100000003",
        },
    ]

    for restaurant_data in restaurants:
        exists = (
            db.query(Restaurant)
            .filter(Restaurant.name == restaurant_data["name"])
            .first()
        )

        if exists is None:
            db.add(Restaurant(**restaurant_data))

    db.commit()