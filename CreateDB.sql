CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
avatar BLOB DEFAULT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS posts(
id integer PRIMARY KEY AUTOINCREMENT,
user_id integer,
content text NOT NULL,
time integer NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id)
)