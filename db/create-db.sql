CREATE TABLE session
(
    id serial NOT NULL
      CONSTRAINT session_pkey
      PRIMARY KEY,
    description CHAR(6),
    active boolean DEFAULT FALSE
);


CREATE TABLE camper
(
    id serial NOT NULL
      CONSTRAINT camper_pkey
      PRIMARY KEY,
    name VARCHAR(20),
    prompt varchar(20),
    session_id INT
      CONSTRAINT session_id_fk
      REFERENCES "session"
);

CREATE TABLE item
(
    id serial NOT NULL
      CONSTRAINT item_pkey
      PRIMARY KEY,
    item_desc VARCHAR(20),
    is_debit boolean DEFAULT TRUE
);


CREATE TABLE transaction
(
    id serial NOT NULL
      CONSTRAINT transaction_pkey
      PRIMARY KEY,
    camper_id INTEGER
      CONSTRAINT camper_id_fk
      REFERENCES "camper",
    time timestamp,
    item_id INT
      CONSTRAINT item_id_fk
      REFERENCES "item",
    amount int
)