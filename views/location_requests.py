import json
import sqlite3
from models import Location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.address
        FROM location a
        """)

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            location = Location(row['id'], row['address'])

            locations.append(location.__dict__) # see the notes below for an explanation on this line of code.

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Fetch location details
        db_cursor.execute("""
            SELECT id, address
            FROM location
            WHERE id = ?
        """, (id,))

        # Load the single result into memory
        location_data = db_cursor.fetchone()

        if location_data:
            # Fetch employees associated with the location
            db_cursor.execute("""
                SELECT id, name
                FROM employee
                WHERE location_id = ?
            """, (id,))
            employees_data = db_cursor.fetchall()

            # Fetch animals associated with the location
            db_cursor.execute("""
                SELECT id, name
                FROM animal
                WHERE location_id = ?
            """, (id,))
            animals_data = db_cursor.fetchall()

            # Create a dictionary to store location details, employees, and animals
            location = {
                "id": location_data['id'],
                "address": location_data['address'],
                "employees": [{"id": employee['id'], "name": employee['name']} for employee in employees_data],
                "animals": [{"id": animal['id'], "name": animal['name']} for animal in animals_data]
            }

            return location
        else:
            return None


def create_location(location):
    """Returns a new location"""
    # Get the id value of the last locatoin in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    """DELETE LOCATIONS"""
    # Initial -1 value for location index, in case one isn't found
    location_index = -1

    # Iterate the LOCATIONS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the animal was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)

def update_location(id, new_location):
    """EDIT LOCATION"""
    # Iterate the LOCATION list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Update the value.
            LOCATIONS[index] = new_location
            break
