/*create table restaurant
(
    name String(80) NOT NULL,
    id Integer primary key
);*/

create table menu_item
(
    id Integer primary key,
    course String(250),
    description String(250),
    price String(8),
    restaurant_id  Integer
);
