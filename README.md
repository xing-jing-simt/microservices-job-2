## Booking API
Booking API contains the following routes:
- GET /api/bookings/
- GET /api/bookings/{id}
- POST /api/bookings
- PUT /api/bookings/{id}
- DELETE /api/bookings/{id}
- GET /openapi/swagger

## How to install
1. Create a fresh Python 3.10 venv
2. Install provided packages from requirements.txt in venv.
3. Navigate to project root and install `booking_api` package into venv. 

On Windows:

`python -m venv booking_api_venv`

`booking_api_venv\Scripts\activate`

`python -m pip install -r requirements.txt`

`python -m pip install -e .`

## How to run
1. Set a FLASK_APP environment variable to `booking_api.server`
2. Run `flask run` to start the server in production mode. 

On Windows:

`set FLASK_APP=booking_api.server`

`python -m flask run`