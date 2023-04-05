-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: state_migrations
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

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
-- Table structure for table `census_states`
--

DROP TABLE IF EXISTS `census_states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `census_states` (
  `id` int NOT NULL AUTO_INCREMENT,
  `census_id` varchar(5) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `abbrv` varchar(5) NOT NULL,
  `level` varchar(25) NOT NULL,
  `parent_id` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `migrations`
--

DROP TABLE IF EXISTS `migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `current_state` varchar(5) NOT NULL,
  `previous_state` varchar(5) NOT NULL,
  `estimate` int NOT NULL,
  `margin_of_error` decimal(9,2) NOT NULL,
  `year` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32768 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `percent_migrate_nc`
--

DROP TABLE IF EXISTS `percent_migrate_nc`;
/*!50001 DROP VIEW IF EXISTS `percent_migrate_nc`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `percent_migrate_nc` AS SELECT 
 1 AS `previous_state`,
 1 AS `estimate`,
 1 AS `population`,
 1 AS `percent`,
 1 AS `year`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `regions_and_divisions`
--

DROP TABLE IF EXISTS `regions_and_divisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regions_and_divisions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `census_id` varchar(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `abbrv` varchar(5) DEFAULT NULL,
  `level` varchar(25) NOT NULL,
  `parent_id` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `state_div_reg`
--

DROP TABLE IF EXISTS `state_div_reg`;
/*!50001 DROP VIEW IF EXISTS `state_div_reg`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `state_div_reg` AS SELECT 
 1 AS `abbrv`,
 1 AS `census_id`,
 1 AS `div_id`,
 1 AS `reg_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `state_pop`
--

DROP TABLE IF EXISTS `state_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `state_pop` (
  `id` int NOT NULL AUTO_INCREMENT,
  `state` varchar(5) NOT NULL,
  `year` int NOT NULL,
  `population` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `percent_migrate_nc`
--

/*!50001 DROP VIEW IF EXISTS `percent_migrate_nc`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `percent_migrate_nc` (`previous_state`,`estimate`,`population`,`percent`,`year`) AS select `m`.`previous_state` AS `previous_state`,`m`.`estimate` AS `estimate`,`p`.`population` AS `population`,(`m`.`estimate` / `p`.`population`) AS `(m.estimate/p.population)`,`m`.`year` AS `year` from (`migrations` `m` join `state_pop` `p` on(((`m`.`previous_state` = `p`.`state`) and (`m`.`year` = `p`.`year`)))) where (`m`.`current_state` = 'NC') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `state_div_reg`
--

/*!50001 DROP VIEW IF EXISTS `state_div_reg`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `state_div_reg` (`abbrv`,`census_id`,`div_id`,`reg_id`) AS select `s`.`abbrv` AS `abbrv`,`s`.`census_id` AS `census_id`,`s`.`parent_id` AS `parent_id`,`d`.`parent_id` AS `parent_id` from (`census_states` `s` left join `regions_and_divisions` `d` on((`s`.`parent_id` = `d`.`census_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-13 23:58:00
