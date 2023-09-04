/*
SQLyog Professional v12.08 (64 bit)
MySQL - 8.0.31-0ubuntu0.20.04.1 : Database - inn_reservation
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`inn_reservation` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `inn_reservation`;

/*Table structure for table `inn_customer` */

DROP TABLE IF EXISTS `inn_customer`;

CREATE TABLE `inn_customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `last_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `phone_number` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;

/*Data for the table `inn_customer` */

/*Table structure for table `inn_reservation` */

DROP TABLE IF EXISTS `inn_reservation`;

CREATE TABLE `inn_reservation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_type` int DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `accommodation_days` smallint DEFAULT NULL,
  `cost` decimal(5,2) DEFAULT NULL,
  `checkout` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `room_type` (`room_type`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `inn_reservation_ibfk_1` FOREIGN KEY (`room_type`) REFERENCES `inn_rooms` (`id`),
  CONSTRAINT `inn_reservation_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `inn_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb3;

/*Data for the table `inn_reservation` */

/*Table structure for table `inn_rooms` */

DROP TABLE IF EXISTS `inn_rooms`;

CREATE TABLE `inn_rooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_type` varchar(1) DEFAULT NULL,
  `room_price` decimal(5,2) DEFAULT NULL,
  `availability` smallint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;

/*Data for the table `inn_rooms` */

insert  into `inn_rooms`(`id`,`room_type`,`room_price`,`availability`) values (1,'S','100.00',14),(2,'P','150.00',9),(3,'O','200.00',9);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
