CREATE TABLE session (
  id          SERIAL NOT NULL
    CONSTRAINT session_pkey
      PRIMARY KEY,
  description CHAR(6),
  active      BOOLEAN DEFAULT FALSE
);


CREATE TABLE camper (
  id          SERIAL NOT NULL
    CONSTRAINT camper_pkey
      PRIMARY KEY,
  name        VARCHAR(20),
  swim_number INT,
  prompt      VARCHAR(20),
  session_id  INT
    CONSTRAINT session_id_fk
      REFERENCES "session"
);

CREATE TABLE item (
  id        SERIAL NOT NULL
    CONSTRAINT item_pkey
      PRIMARY KEY,
  item_desc VARCHAR(20),
  is_debit  BOOLEAN DEFAULT TRUE
);


CREATE TABLE transaction (
  id        SERIAL NOT NULL
    CONSTRAINT transaction_pkey
      PRIMARY KEY,
  camper_id INTEGER
    CONSTRAINT camper_id_fk
      REFERENCES "camper",
  time      VARCHAR(30),
  item_id   INT
    CONSTRAINT item_id_fk
      REFERENCES "item",
  amount    INT
)