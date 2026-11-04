from abc import ABC, abstractmethod
from typing import override
class Rooms(ABC):
    def __str__(self):
        return f"base per night: {self.get_base_price()} Maximum guests:{self.get_maximum_people()} Break fast :{self.is_breakfast_included()}"
    @abstractmethod
    def get_base_price(self):
        pass
    @abstractmethod
    def get_maximum_people(self):
        pass
    @abstractmethod
    def is_breakfast_included(self):
        pass
class StandardRoom(Rooms):
    @override
    def get_base_price(self):
        return 2500
    def get_maximum_people(self):
        return 2
    def is_breakfast_included(self):
        return False
class DeluxeRoom(Rooms):
    def get_base_price(self):
        return 4000
    def get_maximum_people(self):
        return 3
    def is_breakfast_included(self):
        return True
class SuiteRoom(Rooms):
    def get_base_price(self):
        return 7500
    def get_maximum_people(self):
        return 4
    def is_breakfast_included(self):
        return True 
    
class Guest:
    def __init__(self,name,phone_number,email):
        self.name=name
        self.phone_number=phone_number
        self.email=email
    def __str__(self):
        return "guest name :{self.name}  phone number:{self.phone_number} "

class Bookings:
    def __init__(self,guest,room_no,check_in,check_out,room_type,no_of_guests,status):
        
        self.guest=guest
        self.room_no=room_no
        self.check_in=check_in
        self.check_out=check_out
        self.room_type=room_type
        self.no_of_guests=no_of_guests
        self.status=status

class Room:
    def __init__(self,no,type,floor):
        self.no=no
        self.type=type
        self.floor=floor
