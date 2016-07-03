DROP TABLE item;


DROP TABLE category;


DROP TABLE USER;


CREATE TABLE USER (id Integer PRIMARY KEY, username String(250), password String(250));

--DROP TABLE restaurant;

CREATE TABLE category (name String(80) NOT NULL, id Integer PRIMARY KEY, user_id String(250),
                       FOREIGN KEY(user_id) REFERENCES USER(id));

--DROP TABLE menu_item;

CREATE TABLE item (id Integer PRIMARY KEY, title String(250), description String(250), category_id Integer, user_id Integer,
                   FOREIGN KEY(user_id) REFERENCES USER(id),
                   FOREIGN KEY(category_id) REFERENCES category(id));