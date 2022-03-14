CREATE TABLE IF NOT EXISTS BOOKINGS (
    booking_id integer primary key autoincrement,
    date text,
    time text,
    pick_up_pt text,
    dest text,
    curr_lat numeric,
    curr_long numeric
)