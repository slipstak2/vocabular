CREATE TABLE `dictionary` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `sound` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`online_path` varchar(1024) NULL,
	`local_path` varchar(1024) NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `word_rus` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`value` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`meaning` text NULL,
	`sound_id` int(11) NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (sound_id) REFERENCES sound(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `word_eng` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`value` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`meaning` text NULL,
	`sound_id` int(11) NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (sound_id) REFERENCES sound(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


CREATE TABLE `rus_eng` (
	`word_rus_id` int(11) NOT NULL,
	`word_eng_id` int(11) NOT NULL,
	`rus_order`   int(11) NOT NULL DEFAULT -1,
	`eng_order`   int(11) NOT NULL DEFAULT -1,
	CONSTRAINT UNIQUE( `word_rus_id`, `word_eng_id` ),
	INDEX (`word_rus_id`),
	INDEX (`word_eng_id`),
	FOREIGN KEY (word_rus_id) REFERENCES word_rus(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (word_eng_id) REFERENCES word_eng(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_rus_dict` (
	`dict_id` int(11) NOT NULL,
	`word_rus_id` int(11) NOT NULL,
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT UNIQUE( `dict_id`, `word_rus_id` ),
	FOREIGN KEY (dict_id) REFERENCES dictionary(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (word_rus_id) REFERENCES word_rus(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_eng_dict` (
	`dict_id` int(11) NOT NULL,
	`word_eng_id` int(11) NOT NULL,
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT UNIQUE( `dict_id`, `word_eng_id` ),
	FOREIGN KEY (dict_id) REFERENCES dictionary(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (word_eng_id) REFERENCES word_eng(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
