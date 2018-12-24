DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS hotels;

CREATE TABLE hotels (
    id serial PRIMARY KEY NOT NULL,
    name varchar NOT NULL
);

CREATE TABLE rooms (
    id serial PRIMARY KEY NOT NULL,
    room_number smallint NOT NULL,
    hotel_id integer NOT NULL,
    floor_number smallint NOT NULL,
    UNIQUE (hotel_id, room_number),
    FOREIGN KEY (hotel_id) REFERENCES hotels (id) ON DELETE CASCADE
);

CREATE TABLE booking (
    room_id integer PRIMARY KEY NOT NULL,
    guest_name varchar NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE RESTRICT
);
