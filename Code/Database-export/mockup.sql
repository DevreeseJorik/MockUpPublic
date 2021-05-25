SET
  SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET
  time_zone = "+00:00";
--
  -- Database: `homecontrol`
  --
  DROP DATABASE IF EXISTS homecontrol;
CREATE DATABASE IF NOT EXISTS `homecontrol` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `homecontrol`;
CREATE USER IF NOT EXISTS 'root_fswd' @'localhost' IDENTIFIED BY 'root_fswd';
GRANT ALL PRIVILEGES ON *.* TO 'root_fswd' @'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `action` (
  `actionId` int NOT NULL,
  `description` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`actionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action`
--

LOCK TABLES `action` WRITE;
/*!40000 ALTER TABLE `action` DISABLE KEYS */;
/*!40000 ALTER TABLE `action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beverages`
--

DROP TABLE IF EXISTS `beverages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beverages` (
  `beverageId` int NOT NULL,
  `beverageName` varchar(145) DEFAULT NULL,
  `alcoholPercentage` float NOT NULL DEFAULT '0',
  `description` varchar(264) DEFAULT NULL,
  `volumeLeft` float DEFAULT NULL,
  `totalVolume` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`beverageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beverages`
--

LOCK TABLES `beverages` WRITE;
/*!40000 ALTER TABLE `beverages` DISABLE KEYS */;
INSERT INTO `beverages` VALUES (1,'Blue Curaçua',0.21,'Curaçao is a liqueur flavored with the dried peel of the bitter orange laraha, a citrus fruit, grown on the Dutch island of Curaçao.',0.7,0.7,14.5),(2,'Vodka',0.4,'Vodka is traditionally made by distilling the liquid from cereal grains that have been fermented, with potatoes arising as a substitute in more recent times, and some modern brands using fruits, honey or maple sap as the base.',0.7,0.7,30),(3,'Rum',0.35,'Rum is a liquor made by fermenting then distilling sugarcane molasses or sugarcane juice. The distillate, a clear liquid, is usually aged in oak barrels.',0.7,0.7,17.85),(4,'Tonic',0,'Tonic water is a carbonated soft drink used in a variety of cocktails. With it\'s fluorescent color it makes parties even more fun.',1.5,1.5,2),(5,'Orange Juice',0,'Orange juice is a liquid extract of the orange tree fruit, produced by squeezing or reaming oranges. It is a classic mixing ingredient in thousands of cocktails and mocktails alike.',2,2,2),(6,'Gin',0.375,'Gin is a distilled alcoholic drink that derives its predominant flavour from juniper berries.',0.7,0.7,16.75),(7,'Lemon juice',0,'Lemon is a core ingredient in many cocktails involving Gin',0.7,0.7,4);
/*!40000 ALTER TABLE `beverages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cocktail`
--

DROP TABLE IF EXISTS `cocktail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cocktail` (
  `cocktailId` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `alcoholPercentage` float DEFAULT '0',
  `description` varchar(145) DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`cocktailId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cocktail`
--

LOCK TABLES `cocktail` WRITE;
/*!40000 ALTER TABLE `cocktail` DISABLE KEYS */;
INSERT INTO `cocktail` VALUES (1,'Indianapolis',0.3,'If you enjoy vodka, this is a must try. Mixed with the cocktail staple Blue Curaçua, this drink gets anyone loose.',7.5),(2,'Blue Lagoon',0.21,'Enjoy an Indianapolis with a lemon-tasting twist? Blue lagoon is the drink for you.',4.5),(3,'Bluebird',0.275,'Blue bird? No this isn\'t a twitter advertisement. But you\'ll be saying anything coming to mind with this one too!',6),(4,'Blue Punch',0.3,'Are you more of a classical cocktail enjoyer? If so, this drink might be your next target. But careful, this one packs a punch!',6),(5,'Gimlet Gin',0.24,'Gin, lemon juice. A simple cocktail to get the night started.',7.5),(6,'Gimlet Vodka',0.3,'Unlke it\'s gin counterpart, a Vodka gimlet is served strong. Proceed with caution',7.5),(7,'Gin and Tonic',0.24,'Who doesn\'t love a Gin and Tonic? A simple drink you can\'t go wrong with.',4.5),(8,'Screwdriver',0.18,'Can\'t find what you\'re looking for? Screw it, grab this vodka mix and get wildin!',7.5),(9,'Basic Blue',0.24,'It\'s basic, it\'s blue. What more can I say?',6),(10,'The Greyhound',0.35,'A true classic for strong cocktail lovers. If you\'re one of them, this one doesn\'t need an explanation.',8);
/*!40000 ALTER TABLE `cocktail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cocktailhistory`
--

DROP TABLE IF EXISTS `cocktailhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cocktailhistory` (
  `HistoryId` int NOT NULL,
  `actionDate` datetime NOT NULL,
  `mixId` int DEFAULT NULL,
  `comments` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`HistoryId`),
  KEY `FK1_idx` (`mixId`),
  CONSTRAINT `FK1_m2` FOREIGN KEY (`mixId`) REFERENCES `cocktail` (`cocktailId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cocktailhistory`
--

LOCK TABLES `cocktailhistory` WRITE;
/*!40000 ALTER TABLE `cocktailhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `cocktailhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `deviceId` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `brand` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `purchaseCost` float DEFAULT NULL,
  `description` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`deviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devicehistory`
--

DROP TABLE IF EXISTS `devicehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devicehistory` (
  `historyId` int NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deviceId` int DEFAULT NULL,
  `actionId` int DEFAULT NULL,
  `value` float DEFAULT NULL,
  `DeviceHistorycol` varchar(45) DEFAULT NULL,
  `comments` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`historyId`),
  KEY `FK1_idx` (`deviceId`),
  KEY `FK2_idx` (`actionId`),
  CONSTRAINT `FK1` FOREIGN KEY (`deviceId`) REFERENCES `device` (`deviceId`),
  CONSTRAINT `FK2` FOREIGN KEY (`actionId`) REFERENCES `action` (`actionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devicehistory`
--

LOCK TABLES `devicehistory` WRITE;
/*!40000 ALTER TABLE `devicehistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `devicehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mix`
--

DROP TABLE IF EXISTS `mix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mix` (
  `mixId` int NOT NULL,
  `cocktailId` int DEFAULT NULL,
  `beverageId` int DEFAULT NULL,
  `volume` float DEFAULT NULL,
  PRIMARY KEY (`mixId`),
  KEY `FK1_idx` (`cocktailId`),
  KEY `FK2_idx` (`beverageId`),
  CONSTRAINT `FK1_m` FOREIGN KEY (`cocktailId`) REFERENCES `cocktail` (`cocktailId`),
  CONSTRAINT `FK2_m` FOREIGN KEY (`beverageId`) REFERENCES `beverages` (`beverageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mix`
--

LOCK TABLES `mix` WRITE;
/*!40000 ALTER TABLE `mix` DISABLE KEYS */;
INSERT INTO `mix` VALUES (1,1,1,0.1),(2,1,2,0.1),(3,2,1,0.05),(4,2,2,0.02),(5,2,7,0.1),(6,3,1,0.1),(7,3,6,0.15),(8,3,7,0.05),(9,4,1,0.1),(10,4,6,0.15),(11,4,7,0.05),(12,4,5,0.05),(13,5,6,0.15),(14,5,7,0.1),(15,6,2,0.1),(16,6,7,0.15),(17,7,6,0.1),(18,7,4,0.1),(19,8,2,0.1),(20,8,5,0.15),(21,9,1,0.1),(22,9,2,0.4),(23,9,5,0.6),(24,10,2,0.16),(25,10,5,0.4);
/*!40000 ALTER TABLE `mix` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-25 10:34:59
