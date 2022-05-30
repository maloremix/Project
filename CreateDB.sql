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
);


CREATE TABLE IF NOT EXISTS likes(
id integer PRIMARY KEY AUTOINCREMENT,
user_id integer,
post_id integer,
isLike integer,
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (post_id) REFERENCES posts(id)
);

CREATE TABLE IF NOT EXISTS messages(
id integer PRIMARY KEY AUTOINCREMENT,
user_id1 integer,
user_id2 integer,
content text,
FOREIGN KEY (user_id1) REFERENCES users(id),
FOREIGN KEY (user_id2) REFERENCES users(id)
)