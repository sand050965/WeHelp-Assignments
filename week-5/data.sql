-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `like_detail`
--

DROP TABLE IF EXISTS `like_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `like_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '按讚資料編號',
  `member_id` bigint NOT NULL COMMENT '按讚會員id',
  `message_id` bigint NOT NULL COMMENT '按讚留言id',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '按讚時間',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UC_like_detail` (`member_id`,`message_id`),
  KEY `memberId_idx` (`member_id`),
  KEY `messageIn_idx` (`message_id`),
  CONSTRAINT `like_detail_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`),
  CONSTRAINT `like_detail_ibfk_2` FOREIGN KEY (`message_id`) REFERENCES `message` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `like_detail`
--

LOCK TABLES `like_detail` WRITE;
/*!40000 ALTER TABLE `like_detail` DISABLE KEYS */;
INSERT INTO `like_detail` VALUES (1,1,1,'2022-10-25 16:13:03'),(2,1,2,'2022-10-25 16:13:17');
/*!40000 ALTER TABLE `like_detail` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_message_like_count` AFTER INSERT ON `like_detail` FOR EACH ROW UPDATE message
SET like_count= like_count+1
WHERE id = NEW.message_id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '獨立編號',
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `username` varchar(255) NOT NULL COMMENT '帳戶名稱',
  `password` varchar(255) NOT NULL COMMENT '帳戶密碼',
  `follower_count` int unsigned NOT NULL DEFAULT '0' COMMENT '追蹤者數量',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '註冊時間',
  PRIMARY KEY (`id`),
  KEY `username_idx` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'test2','test','test',246469,'2022-10-17 19:54:16'),(2,'Amber','acct1','pwd1',172974,'2022-10-17 17:45:59'),(3,'Leyla','acct2','pwd2',341192,'2022-10-17 17:46:42'),(4,'Max','acct3','pwd3',146469,'2022-10-17 17:47:17'),(5,'Harry','acct4','pwd4',180142,'2022-10-17 17:48:26'),(6,'Mike','acct5','pwd5',3291,'2022-10-17 17:49:12'),(7,'Eve','acct6','pwd6',312469,'2022-10-17 17:49:51'),(8,'Andrew','acct7','pwd7',44169,'2022-10-17 17:50:26');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '獨立編號',
  `member_id` bigint NOT NULL COMMENT '留言者會員編號',
  `content` varchar(255) NOT NULL COMMENT '留言內容',
  `like_count` int unsigned DEFAULT '0' COMMENT '按讚的數量',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '留言時間',
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,3,'Good~Good~',101,'2022-10-25 16:13:03'),(2,1,'Exellent!!!',1241,'2022-10-25 16:13:17'),(3,1,'AWESOME',332,'2022-10-17 20:21:43'),(4,8,'One Of A Kind!',520,'2022-10-17 20:21:51'),(5,1,'Hello World!',728,'2022-10-17 20:21:59'),(6,4,'I Hate U',593,'2022-10-17 20:22:06'),(7,4,'Bad~Bad~',100,'2022-10-17 20:22:13'),(8,7,'I Like It~^^',982,'2022-10-17 20:22:20'),(9,2,'YOLO~~~~',493,'2022-10-17 20:22:27'),(10,3,'SHY~SHY~SHY~',777,'2022-10-17 20:22:34'),(11,5,'Whats UP!!',135,'2022-10-17 20:22:41'),(12,6,'Let it go~~',951,'2022-10-17 20:22:49'),(13,1,'Lovely~><',1141,'2022-10-17 20:22:56');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-25 19:01:28
