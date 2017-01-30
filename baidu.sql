CREATE DATABASE `baidu`;
USE `baidu`;
CREATE TABLE IF NOT EXISTS `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `uk` varchar(200) NOT NULL,
  `url` varchar(200) NOT NULL,
  `key` varchar(1000) NOT NULL,
  `type` int(11) NOT NULL
) ENGINE=InnoDB CHARSET=utf8;