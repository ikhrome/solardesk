DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `ticket`;
DROP TABLE IF EXISTS `firms`;

CREATE TABLE user
(
    `id`           INTEGER PRIMARY KEY AUTOINCREMENT,
    `username`     TEXT UNIQUE NOT NULL,
    `email`        TEXT UNIQUE NOT NULL,
    `active`       INTEGER     NOT NULL DEFAULT 0,
    `phone_number` TEXT UNIQUE NOT NULL,
    `password`     TEXT        NOT NULL,
    `first_name`   TEXT,
    `middle_name`  TEXT,
    `last_name`    TEXT,
    `position`     TEXT        NOT NULL DEFAULT 'user',
    `firm_id`      INTEGER     NULL,
    FOREIGN KEY (firm_id) REFERENCES firms (id)
);

CREATE TABLE firms
(
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    info  TEXT
);

CREATE TABLE tickets
(
    `id`          INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id`     INTEGER   NOT NULL,
    `created`     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status`      INTEGER   NOT NULL DEFAULT 0,
    `priority`    INTEGER   NOT NULL DEFAULT 1,
    `assigned`    INTEGER,
    `description` TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (assigned) REFERENCES user (id)
);

-- Default users. DELETE them in production!
INSERT INTO user(username, email, active, phone_number, password, first_name, middle_name, last_name, position, firm_id)
VALUES ('ikhrome',
        'khromov.ivan@gmail.com',
        1,
        '89634414949',
        'pbkdf2:sha256:50000$8uUY6OA2$ed1e0b01191dc5758c2846a39dcb8e71d9f351f0473b90c698930778889ac1fc',
        'Ivan', 'Andreevich', 'Khromov',
        NULL, NULL);