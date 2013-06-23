DROP DATABASE IF EXISTS GuessWord;

CREATE DATABASE GuessWord;

CREATE TABLE IF NOT EXISTS GuessWord.user (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Login` nvarchar(15) NOT NULL,
  `Password` nvarchar(15) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `DOB` DATE NOT NULL,
  `Location` nvarchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
