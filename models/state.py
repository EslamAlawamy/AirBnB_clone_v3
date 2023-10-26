#!/usr/bin/python3
""" Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")

    else:
        name = ""

        @property
        def cities(self):
            """ returns the list of City instances """
            from models import storage
            all_city = storage.all(City)
            list = []

            for city in all_city.values():
                if self.id == city.state_id:
                    list.append(city)
            return list
