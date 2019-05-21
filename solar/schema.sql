DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `ticket`;
DROP TABLE IF EXISTS `firms`;

CREATE TABLE user (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `username` TEXT UNIQUE NOT NULL,
    `email` TEXT UNIQUE NOT NULL,
    `active` INTEGER NOT NULL DEFAULT 0,
    `phone_number` TEXT UNIQUE NOT NULL,
    `password` TEXT NOT NULL,
    `first_name` TEXT,
    `middle_name` TEXT,
    `last_name` TEXT,
    `position` TEXT NOT NULL DEFAULT 'user',
    `firm_id` INTEGER NULL,
    FOREIGN KEY(firm_id) REFERENCES firms(id)
);

CREATE TABLE firms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    info TEXT
);

CREATE TABLE tickets (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INTEGER NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status` INTEGER NOT NULL DEFAULT 0,
    `priority` INTEGER NOT NULL DEFAULT 1,
    `assigned` INTEGER,
    `description` TEXT,
    FOREIGN KEY(user_id)  REFERENCES user(id),
    FOREIGN KEY(assigned) REFERENCES user(id)
);