DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    offerer INTEGER NOT NULL,
    email TEXT NOT NULL,
    title TEXT UNIQUE NOT NULL,
    body TEXT NOT NULL,
    subject TEXT NOT NULL,
    grade_from TEXT NOT NULL,
    grade_to TEXT NOT NULL,
    FOREIGN KEY (offerer) REFERENCES user (id)
);