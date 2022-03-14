from pydantic import BaseModel
from typing import List

# models for validation and description
class NoBooking(BaseModel):
    def empty_json():
        return []


class SingleBookingPost(BaseModel):
    date: str
    time: str
    pick_up_pt: str
    dest: str
    curr_lat: str
    curr_long: str


class SingleBooking(BaseModel):
    booking_id: int
    date: str
    time: str
    pick_up_pt: str
    dest: str
    curr_lat: str
    curr_long: str


class MultipleBookings(BaseModel):
    bookings: List[SingleBooking]


class BookingPath(BaseModel):
    booking_id: int


class BookingQuery(BaseModel):
    title: str
    author: str
