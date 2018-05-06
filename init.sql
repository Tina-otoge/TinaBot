CREATE TABLE IF NOT EXISTS `users` (
  `id` VARCHAR(18) NOT NULL,
  `super_admin` INTEGER(1) DEFAULT 0,
  `birthday` TEXT
);

CREATE TABLE IF NOT EXISTS `servers` (
  `id` VARCHAR(18) NOT NULL,
  `bot_admins` TEXT,
  `birthday_channel` VARCHAR(18)
);
