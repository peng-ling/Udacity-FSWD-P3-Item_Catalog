CREATE DATABASE ITEMLIST;

CREATE ROLE cataloge WITH LOGIN PASSWORD 'A1See2D3See'

CREATE SCHEMA itemlist;

GRANT SELECT ON ALL TABLES IN SCHEMA itemlist TO cataloge;

GRANT INSERT ON ALL TABLES IN SCHEMA itemlist TO cataloge;

GRANT DELETE ON ALL TABLES IN SCHEMA itemlist TO cataloge;

GRANT UPDATE ON ALL TABLES IN SCHEMA itemlist TO cataloge;



DROP TABLE item;


DROP TABLE category;


DROP TABLE USER;


CREATE TABLE USER (id Integer PRIMARY KEY,
                                      username String(250),
                                      email String (250));

--DROP TABLE restaurant;

CREATE TABLE category (name String(80) NOT NULL, id Integer PRIMARY KEY, user_id String(250),
                       FOREIGN KEY(user_id) REFERENCES USER(id));

--DROP TABLE menu_item;

CREATE TABLE item (id Integer PRIMARY KEY, title String(250), description String(250), category_id Integer, user_id Integer,
                   FOREIGN KEY(user_id) REFERENCES USER(id),
                   FOREIGN KEY(category_id) REFERENCES category(id));


CREATE VIEW Serialize AS
SELECT i.id AS item_id,
       u.username,
       c.id AS category_id,
       c.name AS category_name,
       i.title AS item_title,
       i.description AS item_description,
       u.id AS user_id
FROM USER u
LEFT OUTER JOIN category c ON u.id = c.user_id
LEFT OUTER JOIN item i ON i.category_id = C.id ;
