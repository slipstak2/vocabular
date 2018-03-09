DROP TABLE IF EXISTS `word_eng_sound` CASCADE;
DROP TABLE IF EXISTS `word_rus_sound` CASCADE;
DROP TABLE IF EXISTS `word_eng_dict` CASCADE;
DROP TABLE IF EXISTS `word_rus_dict` CASCADE;
DROP TABLE IF EXISTS `rus_eng` CASCADE;
DROP TABLE IF EXISTS `word_eng` CASCADE;
DROP TABLE IF EXISTS `word_rus` CASCADE;
DROP TABLE IF EXISTS `sound` CASCADE;
DROP TABLE IF EXISTS `dictionary` CASCADE;

CREATE TABLE `dictionary` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `sound` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`online_path` varchar(1024) NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `word_rus` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`value` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`meaning` text NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `word_eng` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`value` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`meaning` text NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `rus_eng` (
	`word_rus_id` int(11) NOT NULL,
	`word_eng_id` int(11) NOT NULL,
	`rus_order`   int(11) NOT NULL DEFAULT -1,
	`eng_order`   int(11) NOT NULL DEFAULT -1,
	CONSTRAINT UNIQUE( `word_rus_id`, `word_eng_id` ),
	INDEX (`word_rus_id`),
	INDEX (`word_eng_id`),
	FOREIGN KEY (word_rus_id) REFERENCES word_rus(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (word_eng_id) REFERENCES word_eng(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_rus_dict` (
	`dict_id` int(11) NOT NULL,
	`word_rus_id` int(11) NOT NULL,
	`word_rus_order` int(11) NOT NULL DEFAULT -1,
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT UNIQUE( `dict_id`, `word_rus_id` ),
	FOREIGN KEY (dict_id) REFERENCES dictionary(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (word_rus_id) REFERENCES word_rus(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_eng_dict` (
	`dict_id` int(11) NOT NULL,
	`word_eng_id` int(11) NOT NULL,
	`word_eng_order` int(11) NOT NULL DEFAULT -1,
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT UNIQUE( `dict_id`, `word_eng_id` ),
	FOREIGN KEY (dict_id) REFERENCES dictionary(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (word_eng_id) REFERENCES word_eng(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_rus_sound` (
	`word_rus_id` int(11) NOT NULL,
	`sound_id`    int(11) NULL,
	`sound_order` int(11) NOT NULL DEFAULT -1,
	CONSTRAINT UNIQUE( `word_rus_id`, `sound_id` ),
	INDEX (`word_rus_id`),
	FOREIGN KEY (word_rus_id) REFERENCES word_rus(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (sound_id) REFERENCES sound(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_eng_sound` (
	`word_eng_id` int(11) NOT NULL,
	`sound_id`    int(11) NULL,
	`sound_order` int(11) NOT NULL DEFAULT -1,
	CONSTRAINT UNIQUE( `word_eng_id`, `sound_id` ),
	INDEX (`word_eng_id`),
	FOREIGN KEY (word_eng_id) REFERENCES word_eng(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (sound_id) REFERENCES sound(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Valentina Studio --
-- MySQL dump --
-- ---------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- ---------------------------------------------------------


-- Dump data of "dictionary" -------------------------------
INSERT INTO `dictionary`(`id`,`name`,`date_create`) VALUES ( '1', 'SFML Game Development by example', '2018-01-07 17:20:44' );
INSERT INTO `dictionary`(`id`,`name`,`date_create`) VALUES ( '2', 'Effective Modern C++, 2014', '2018-01-09 10:57:44' );
-- ---------------------------------------------------------


-- Dump data of "rus_eng" ----------------------------------
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '2', '1', '2', '2' );
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '3', '1', '1', '1' );
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '4', '1', '3', '3' );
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '5', '2', '1', '1' );
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '6', '3', '1', '1' );
-- ---------------------------------------------------------


-- Dump data of "sound" ------------------------------------
-- ---------------------------------------------------------


-- Dump data of "word_eng" ---------------------------------
INSERT INTO `word_eng`(`id`,`value`,`meaning`) VALUES ( '1', 'exicting', NULL );
INSERT INTO `word_eng`(`id`,`value`,`meaning`) VALUES ( '2', 'retrieval system', NULL );
INSERT INTO `word_eng`(`id`,`value`,`meaning`) VALUES ( '3', 'deduced type', NULL );
-- ---------------------------------------------------------


-- Dump data of "word_eng_dict" ----------------------------
INSERT INTO `word_eng_dict`(`dict_id`,`word_eng_id`,`date_create`) VALUES ( '1', '1', '2018-01-07 17:28:43' );
INSERT INTO `word_eng_dict`(`dict_id`,`word_eng_id`,`date_create`) VALUES ( '1', '2', '2018-01-07 19:28:43' );
INSERT INTO `word_eng_dict`(`dict_id`,`word_eng_id`,`date_create`) VALUES ( '2', '3', '2018-01-09 11:02:43' );
-- ---------------------------------------------------------


-- Dump data of "word_rus" ---------------------------------
INSERT INTO `word_rus`(`id`,`value`,`meaning`) VALUES ( '2', 'восхитительный', 'эмоция' );
INSERT INTO `word_rus`(`id`,`value`,`meaning`) VALUES ( '3', 'захватывающий', NULL );
INSERT INTO `word_rus`(`id`,`value`,`meaning`) VALUES ( '4', 'еще одно слово', NULL );
INSERT INTO `word_rus`(`id`,`value`,`meaning`) VALUES ( '5', 'поисковая система', NULL );
INSERT INTO `word_rus`(`id`,`value`,`meaning`) VALUES ( '6', 'выводимый тип', NULL );
-- ---------------------------------------------------------


-- Dump data of "word_rus_dict" ----------------------------
-- ---------------------------------------------------------


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- ---------------------------------------------------------



