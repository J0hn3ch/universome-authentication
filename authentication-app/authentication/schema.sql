DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS member;
CREATE TABLE member (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    member_role TEXT NOT NULL,
    student_id TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    authorized BOOLEAN NOT NULL,
    card_id TEXT NOT NULL
);

DROP TABLE IF EXISTS smart_card;
CREATE TABLE smart_card (
    id TEXT NOT NULL UNIQUE,
    model TEXT NOT NULL,
    member INTEGER,
    FOREIGN KEY(member) REFERENCES member(id)
);

DROP TABLE IF EXISTS room;
CREATE TABLE room (
    id TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    building TEXT NOT NULL
);

DROP TABLE IF EXISTS entrance;
CREATE TABLE entrance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrance_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    full_name TEXT NOT NULL,
    card_id TEXT NOT NULL,
    authorized BOOLEAN NOT NULL
    /*room_id TEXT NOT NULL,*/
    /*FOREIGN KEY(card_id) REFERENCES smart_card(id),*/
    /*FOREIGN KEY(room_id) REFERENCES room(id)*/
);

INSERT INTO user VALUES (1, 'admin', 'password');
INSERT INTO user VALUES (2, 'subscriber', 'password2');

INSERT INTO member VALUES (1,'Gianluca Carbone','coordinator','gianluca.carbone', CURRENT_TIMESTAMP, TRUE, '0791B093');
INSERT INTO member VALUES (2,'Carl Johnson','secretary','carl.johnson', CURRENT_TIMESTAMP, FALSE, '576918B5');
INSERT INTO member VALUES (3,'Geronimo Stilton','newspaper','geronimo.stilton', CURRENT_TIMESTAMP, TRUE, '001122AADD');
INSERT INTO member VALUES (4,'Gal Gadot','social','gal.gadot', CURRENT_TIMESTAMP, FALSE, '001122AAEE');

INSERT INTO entrance(entrance_date, full_name, card_id, authorized) VALUES ('2024-06-28 20:53:09','Carl Johnson','576918B5',FALSE);
INSERT INTO entrance(entrance_date, full_name, card_id, authorized) VALUES ('2024-06-28 20:54:10','Gal Gadot','001122AAEE',FALSE);
INSERT INTO entrance(entrance_date, full_name, card_id, authorized) VALUES ('2024-06-28 20:55:30','Gianluca Carbone','7145176147',TRUE);

/*
INSERT INTO room(id, full_name, building) VALUES ('A01','CERIP','A.O.U. Policlinico');
INSERT INTO room(id, full_name, building) VALUES ('B01','UniVersoMe','Palazzo Mariani');
INSERT INTO room(id, full_name, building) VALUES ('B02','UniversiTeatrali','COSPECS');
INSERT INTO room(id, full_name, building) VALUES ('C01','Palestra - Annunziata','S.S.D. UniMe');
INSERT INTO room(id, full_name, building) VALUES ('D01','SmartMe','INGEGNERIA');
*/