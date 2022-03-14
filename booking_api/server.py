from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_openapi3 import Info, Tag, OpenAPI
import sqlite3
from booking_api.model import (
    NoBooking,
    SingleBooking,
    SingleBookingPost,
    MultipleBookings,
    BookingPath,
    BookingQuery,
)

info = Info(title="Booking API", version="1.0.0")
app = OpenAPI(__name__, info=info)


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    if query.split()[0] == "insert":
        lastrowid = cur.lastrowid
        cur.close()
        cur = db.execute(f"select * from bookings where rowid={lastrowid};", ())
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    else:
        cur.close()
        return (rv[0] if rv else None) if one else rv


DATABASE = "./bookings.db"
init_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.get("/api/bookings", responses={"200": MultipleBookings})
def get_bookings():
    # View all bookings
    all_bookings = query_db("select * from bookings;")
    return jsonify(all_bookings)


@app.get("/api/bookings/<booking_id>", responses={"200": SingleBooking})
def get_booking(path: BookingPath):
    # View booking
    booking_id = path.dict()["booking_id"]
    query = f"select * from bookings where booking_id = {booking_id};"
    bookings = query_db(query)
    booking = bookings[0]
    return jsonify(booking), {"location": f"/api/bookings/{str(booking_id)}"}


@app.post("/api/bookings", responses={"202": SingleBooking})
def post_thing(body: SingleBookingPost):
    # Add new booking
    booking = body.dict()
    date = booking["date"]
    time = booking["time"]
    pick_up_pt = booking["pick_up_pt"]
    dest = booking["dest"]
    curr_lat = booking["curr_lat"]
    curr_long = booking["curr_long"]
    query = f'insert into bookings (date, time, pick_up_pt, dest, curr_lat, curr_long) values ("{date}","{time}","{pick_up_pt}","{dest}","{curr_lat}","{curr_long}");'
    inserted_booking = query_db(query)[0]
    booking_id = inserted_booking["booking_id"]
    return jsonify(inserted_booking), {"location": f"/api/bookings/{str(booking_id)}"}


@app.put("/api/bookings/<booking_id>", responses={"204": NoBooking})
def put_thing(path: BookingPath, body: SingleBooking):
    # Update booking
    # TODO: SingleBooking response. 201 and 204 responses should have Location header
    booking_id = path.dict()["booking_id"]
    booking = body.dict()
    date = booking["date"]
    time = booking["time"]
    pick_up_pt = booking["pick_up_pt"]
    dest = booking["dest"]
    curr_lat = booking["curr_lat"]
    curr_long = booking["curr_long"]
    # TODO if booking == existing booking from SQL, return jsonify(NoBooking.empty_json()), 204
    # TODO if booking != existing booking from SQL, return jsonify(new_booking), 201
    query = f'update bookings set date="{date}", time="{time}", pick_up_pt="{pick_up_pt}", dest="{dest}", curr_lat="{curr_lat}", curr_long="{curr_long}" where booking_id={booking_id};'
    query_db(query)
    # if id != thing["id"]:
    #     return "Bad Request", 400
    # all_bookings[thing["id"]] = thing["detail"]
    return jsonify(NoBooking.empty_json()), 204


@app.delete("/api/bookings/<booking_id>", responses={"204": NoBooking})
def delete_thing(path: BookingPath):
    # TODO Delete booking from sql
    booking_id = path.dict()["booking_id"]
    query = f"delete from bookings where booking_id = {booking_id}"
    query_db(query)
    return jsonify(NoBooking.empty_json())


CORS(app)
