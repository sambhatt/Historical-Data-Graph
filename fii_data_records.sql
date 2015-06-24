CREATE DATABASE  IF NOT EXISTS `fii_data` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `fii_data`;
DROP TABLE IF EXISTS `records`;
CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(45) DEFAULT NULL,
  `gross_purchase` varchar(45) DEFAULT NULL,
  `gross_sales` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `records` WRITE;
UNLOCK TABLES;
