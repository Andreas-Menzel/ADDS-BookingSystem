DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stocks;





CREATE TABLE warehouses (
    id      TEXT    PRIMARY KEY,
    name    TEXT    NOT NULL,
    address TEXT    NOT NULL
);

CREATE TABLE products (
    id          TEXT    PRIMARY KEY,
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    weight      INT     NOT NULL
);

CREATE TABLE stocks (
    warehouse_id    TEXT    NOT NULL,
    product_id      TEXT    NOT NULL,
    quantity        INT     NOT NULL
);





INSERT INTO warehouses VALUES(
    "demowarehouse",
    "Demo Warehouse",
    "Arcisstraße 21, 80333 München"
);


INSERT INTO products VALUES(
    "prinzregententorte",
    "Prinzregententorte",
    "Sehr leckerer Kuchen!",
    250
);

INSERT INTO products VALUES(
    "erdbeerkuchen",
    "Erdbeerkuchen",
    "Auch ein sehr leckerer Kuchen!",
    300
);


INSERT INTO stocks VALUES(
    "demowarehouse",
    "prinzregententorte",
    3
);

INSERT INTO stocks VALUES(
    "demowarehouse",
    "erdbeerkuchen",
    1
);