CREATE TABLE `dict_rus` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL DEFAULT '<EMPTY>',
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

CREATE TABLE `dict_eng` (
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
	`dict_rus_id` int(11) NOT NULL,
	`word_rus_id` int(11) NOT NULL,
	`word_order` int(11) NOT NULL DEFAULT -1,
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT UNIQUE( `dict_rus_id`, `word_rus_id` ),
	FOREIGN KEY (dict_rus_id) REFERENCES dict_rus(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (word_rus_id) REFERENCES word_rus(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `word_eng_dict` (
	`dict_eng_id` int(11) NOT NULL,
	`word_eng_id` int(11) NOT NULL,
	`word_order` int(11) NOT NULL DEFAULT -1,
	`date_create` datetime NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT UNIQUE( `dict_eng_id`, `word_eng_id` ),
	FOREIGN KEY (dict_eng_id) REFERENCES dict_eng(id) ON DELETE RESTRICT ON UPDATE CASCADE,
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
