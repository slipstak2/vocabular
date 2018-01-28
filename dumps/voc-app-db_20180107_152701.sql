-- Valentina Studio --
-- MySQL dump --
-- ---------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- ---------------------------------------------------------


-- CREATE TABLE "rus_eng" ----------------------------------
CREATE TABLE `rus_eng` ( 
	`word_rus_id` Int( 11 ) NOT NULL,
	`word_eng_id` Int( 11 ) NOT NULL,
	`rus_order` Int( 11 ) NOT NULL,
	`eng_order` Int( 11 ) NOT NULL,
	CONSTRAINT `rus_eng_unique_index` UNIQUE( `word_rus_id`, `word_eng_id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB;
-- ---------------------------------------------------------


-- CREATE TABLE "dictionary" -------------------------------
CREATE TABLE `dictionary` ( 
	`id` Int( 11 ) AUTO_INCREMENT NOT NULL,
	`name` VarChar( 255 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '<EMPTY>',
	`date_create` DateTime NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY ( `id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB
AUTO_INCREMENT = 45;
-- ---------------------------------------------------------


-- CREATE TABLE "word_eng_dict" ----------------------------
CREATE TABLE `word_eng_dict` ( 
	`dict_id` Int( 11 ) NOT NULL,
	`word_eng_id` Int( 11 ) NOT NULL,
	`date_create` DateTime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT `word_eng_dict_unique_index` UNIQUE( `dict_id`, `word_eng_id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB;
-- ---------------------------------------------------------


-- CREATE TABLE "sound" ------------------------------------
CREATE TABLE `sound` ( 
	`sound_id` Int( 11 ) AUTO_INCREMENT NOT NULL,
	`online_path` VarChar( 1024 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
	`local_path` VarChar( 1024 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
	PRIMARY KEY ( `sound_id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- ---------------------------------------------------------


-- CREATE TABLE "word_rus" ---------------------------------
CREATE TABLE `word_rus` ( 
	`word_rus_id` Int( 11 ) AUTO_INCREMENT NOT NULL,
	`value` VarChar( 255 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '<EMPTY>',
	`meaning` Text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
	`sound_id` Int( 11 ) NULL,
	PRIMARY KEY ( `word_rus_id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- ---------------------------------------------------------


-- CREATE TABLE "word_eng" ---------------------------------
CREATE TABLE `word_eng` ( 
	`word_eng_id` Int( 11 ) AUTO_INCREMENT NOT NULL,
	`value` VarChar( 255 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '<EMPTY>',
	`meaning` Text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
	`sound_id` Int( 11 ) NULL,
	PRIMARY KEY ( `word_eng_id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- ---------------------------------------------------------


-- CREATE TABLE "word_rus_dict" ----------------------------
CREATE TABLE `word_rus_dict` ( 
	`dict_id` Int( 11 ) NOT NULL,
	`word_rus_id` Int( 11 ) NOT NULL,
	`date_create` DateTime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT `word_rus_dict_unique_index` UNIQUE( `dict_id`, `word_rus_id` ) )
CHARACTER SET = utf8
COLLATE = utf8_general_ci
ENGINE = InnoDB;
-- ---------------------------------------------------------


-- CREATE INDEX "index_word_eng_id" ------------------------
CREATE INDEX `index_word_eng_id` USING BTREE ON `rus_eng`( `word_eng_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "index_word_rus_id" ------------------------
CREATE INDEX `index_word_rus_id` USING BTREE ON `rus_eng`( `word_rus_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "index_dict_id" ----------------------------
CREATE INDEX `index_dict_id` USING BTREE ON `word_eng_dict`( `dict_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "index_word_eng_id1" -----------------------
CREATE INDEX `index_word_eng_id1` USING BTREE ON `word_eng_dict`( `word_eng_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "sound_id" ---------------------------------
CREATE INDEX `sound_id` USING BTREE ON `word_rus`( `sound_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "sound_id" ---------------------------------
CREATE INDEX `sound_id` USING BTREE ON `word_eng`( `sound_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "index_dict_id" ----------------------------
CREATE INDEX `index_dict_id` USING BTREE ON `word_rus_dict`( `dict_id` );
-- ---------------------------------------------------------


-- CREATE INDEX "index_word_rus_id1" -----------------------
CREATE INDEX `index_word_rus_id1` USING BTREE ON `word_rus_dict`( `word_rus_id` );
-- ---------------------------------------------------------


-- CREATE LINK "word_rus_ibfk_1" ---------------------------
ALTER TABLE `word_rus`
	ADD CONSTRAINT `word_rus_ibfk_1` FOREIGN KEY ( `sound_id` )
	REFERENCES `sound`( `sound_id` )
	ON DELETE Restrict
	ON UPDATE Cascade;
-- ---------------------------------------------------------


-- CREATE LINK "word_eng_ibfk_1" ---------------------------
ALTER TABLE `word_eng`
	ADD CONSTRAINT `word_eng_ibfk_1` FOREIGN KEY ( `sound_id` )
	REFERENCES `sound`( `sound_id` )
	ON DELETE Restrict
	ON UPDATE Cascade;
-- ---------------------------------------------------------


-- CREATE LINK "lnk_rus_eng_word_eng" ----------------------
ALTER TABLE `word_eng`
	ADD CONSTRAINT `lnk_rus_eng_word_eng` FOREIGN KEY ( `word_eng_id` )
	REFERENCES `rus_eng`( `word_eng_id` )
	ON DELETE Restrict
	ON UPDATE Cascade;
-- ---------------------------------------------------------


-- CREATE LINK "lnk_rus_eng_word_rus" ----------------------
ALTER TABLE `word_rus`
	ADD CONSTRAINT `lnk_rus_eng_word_rus` FOREIGN KEY ( `word_rus_id` )
	REFERENCES `rus_eng`( `word_rus_id` )
	ON DELETE Cascade
	ON UPDATE Cascade;
-- ---------------------------------------------------------


-- CREATE LINK "lnk_word_eng_dict_dictionary" --------------
ALTER TABLE `dictionary`
	ADD CONSTRAINT `lnk_word_eng_dict_dictionary` FOREIGN KEY ( `id` )
	REFERENCES `word_eng_dict`( `dict_id` )
	ON DELETE Cascade
	ON UPDATE Cascade;
-- ---------------------------------------------------------


-- CREATE LINK "lnk_word_eng_dict_word_eng" ----------------
ALTER TABLE `word_eng`
	ADD CONSTRAINT `lnk_word_eng_dict_word_eng` FOREIGN KEY ( `word_eng_id` )
	REFERENCES `word_eng_dict`( `word_eng_id` )
	ON DELETE Cascade
	ON UPDATE Cascade;
-- ---------------------------------------------------------


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- ---------------------------------------------------------


