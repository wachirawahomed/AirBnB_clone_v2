#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage
from os import environ


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def cities(self):
        """
        Getter method to return the list of City objects from storage
        linked to the current State
        """
        city_objs = []
        if storage.all(City):
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_objs.append(city)
        return city_objs
