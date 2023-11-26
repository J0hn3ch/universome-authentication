DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS member;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE member (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    member_role TEXT NOT NULL,
    student_id TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    authorized BOOLEAN NOT NULL
);

INSERT INTO user VALUES (1, 'admin', 'password');
INSERT INTO user VALUES (2, 'subscriber', 'password2');

INSERT INTO member VALUES (1,'Gianluca Carbone','coordinator','gianluca.carbone', CURRENT_TIMESTAMP, TRUE);
INSERT INTO member VALUES (2,'Domenico Leonello','secretary','domenico.leonello', CURRENT_TIMESTAMP, FALSE);
INSERT INTO member VALUES (3,'Francesco Pullella','newspaper','francesco.pullella', CURRENT_TIMESTAMP, TRUE);
INSERT INTO member VALUES (4,'Roberta Leone','social','roberta.leone', CURRENT_TIMESTAMP, FALSE);