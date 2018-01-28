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
-- ---------------------------------------------------------


-- Dump data of "rus_eng" ----------------------------------
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '2', '1', '2', '2' );
INSERT INTO `rus_eng`(`word_rus_id`,`word_eng_id`,`rus_order`,`eng_order`) VALUES ( '3', '1', '1', '1' );
-- ---------------------------------------------------------


-- Dump data of "sound" ------------------------------------
-- ---------------------------------------------------------


-- Dump data of "word_eng" ---------------------------------
INSERT INTO `word_eng`(`id`,`value`,`meaning`,`sound_id`) VALUES ( '1', 'exicting', NULL, NULL );
-- ---------------------------------------------------------


-- Dump data of "word_eng_dict" ----------------------------
INSERT INTO `word_eng_dict`(`dict_id`,`word_eng_id`,`date_create`) VALUES ( '1', '1', '2018-01-07 17:28:43' );
-- ---------------------------------------------------------


-- Dump data of "word_rus" ---------------------------------
INSERT INTO `word_rus`(`id`,`value`,`meaning`,`sound_id`) VALUES ( '2', 'восхитительный', 'эмоция', NULL );
INSERT INTO `word_rus`(`id`,`value`,`meaning`,`sound_id`) VALUES ( '3', 'захватывающий', NULL, NULL );
-- ---------------------------------------------------------


-- Dump data of "word_rus_dict" ----------------------------
-- ---------------------------------------------------------


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- ---------------------------------------------------------


