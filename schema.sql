-- schema.sql
CREATE TABLE donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    blood_group TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    eligibility TEXT NOT NULL
);


sqlite3 donors.db < schema.sql