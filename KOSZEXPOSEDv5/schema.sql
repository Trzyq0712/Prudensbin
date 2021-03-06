DROP TABLE IF EXISTS bins;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS pics;

CREATE TABLE bins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lng FLOAT,
    lat FLOAT,
    bintype TEXT,
    rating_sum FLOAT,
    rating_count INTEGER
);

CREATE TABLE pics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bin INTEGER,
    img BLOB
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bin INTEGER,
    posted DATETIME DEFAULT CURRENT_TIMESTAMP,
    content TEXT
);