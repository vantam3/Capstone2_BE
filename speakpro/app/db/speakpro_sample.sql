-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_audio`
--

DROP TABLE IF EXISTS `app_audio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_audio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `audio_file` varchar(100) NOT NULL,
  `speaking_text_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_audio_speaking_text_id_065a0edc_fk_app_speakingtext_id` (`speaking_text_id`),
  CONSTRAINT `app_audio_speaking_text_id_065a0edc_fk_app_speakingtext_id` FOREIGN KEY (`speaking_text_id`) REFERENCES `app_speakingtext` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_audio`
--

LOCK TABLES `app_audio` WRITE;
/*!40000 ALTER TABLE `app_audio` DISABLE KEYS */;
INSERT INTO `app_audio` VALUES (1,'file_audio/DailyLife_Beginner_My_Favorite_Meal.mp3',1),(2,'file_audio/DailyLife_Beginner_My_Morning_Routine.mp3',2),(3,'file_audio/DailyLife_Beginner_My_Weekend_Plan.mp3',3),(4,'file_audio/DailyLife_Intermediate_A_Typical_Day_at_School.mp3',4),(5,'file_audio/DailyLife_Intermediate_House_Chores_and_Responsibilities.mp3',5),(6,'file_audio/DailyLife_Intermediate_Managing_My_Time.mp3',6),(7,'file_audio/DailyLife_Advanced_How_My_Daily_Routine_Has_Changed.mp3',7),(8,'file_audio/DailyLife_Advanced_Routine_vs._Spontaneity.mp3',8),(9,'file_audio/DailyLife_Advanced_Work-Life_Balance.mp3',9),(10,'file_audio/Technology_Beginner_Favorite_App.mp3',10),(11,'file_audio/Technology_Beginner_My_Favorite_Device.mp3',11),(12,'file_audio/Technology_Beginner_Phone_Usage.mp3',12),(13,'file_audio/Technology_Advanced_Future_Technology.mp3',13),(14,'file_audio/Technology_Advanced_Managing_Screen_Addiction.mp3',14),(15,'file_audio/Family_Beginner_A_Special_Memory.mp3',15),(16,'file_audio/Family_Beginner_Family_Activities.mp3',16),(17,'file_audio/Family_Beginner_Introducing_My_Family.mp3',17),(18,'file_audio/Family_Intermediate_Family_Celebrations.mp3',18),(19,'file_audio/Family_Intermediate_Family_Roles.mp3',19),(20,'file_audio/Family_Intermediate_Staying_in_Touch.mp3',20),(21,'file_audio/Family_Advanced_Changing_Family_Values.mp3',21),(22,'file_audio/Family_Advanced_Generational_Conflicts.mp3',22),(23,'file_audio/Family_Advanced_Long-Distance_Relationships.mp3',23),(24,'file_audio/Education_Beginner_My_Favorite_Subject.mp3',24),(25,'file_audio/Education_Beginner_My_School.mp3',25),(26,'file_audio/Education_Beginner_My_Teacher.mp3',26),(27,'file_audio/Education_Intermediate_Online_vs._Traditional_Classes.mp3',27),(28,'file_audio/Education_Intermediate_Qualities_of_a_Good_Teacher.mp3',28),(29,'file_audio/Education_Intermediate_Study_Habits.mp3',29),(30,'file_audio/Education_Advanced_AI_in_Learning.mp3',30),(31,'file_audio/Education_Advanced_Education_and_Success.mp3',31),(32,'file_audio/Education_Advanced_Free_Education.mp3',32),(33,'file_audio/Travel_Beginner_A_Place_I_Want_to_Travel.mp3',33),(34,'file_audio/Travel_Beginner_My_Favorite_Place_to_Visit.mp3',34),(35,'file_audio/Travel_Beginner_Packing_for_a_Trip.mp3',35),(36,'file_audio/Travel_Intermediate_A_Memorable_Trip.mp3',36),(37,'file_audio/Travel_Intermediate_Solo_vs._Group_Travel.mp3',37),(38,'file_audio/Travel_Intermediate_Transportation_Preferences.mp3',38),(39,'file_audio/Travel_Advanced_Learning_Through_Travel.mp3',39),(40,'file_audio/Travel_Advanced_Limiting_Tourism.mp3',40),(41,'file_audio/Travel_Advanced_Tourism_and_Local_Culture.mp3',41),(42,'file_audio/Technology_Intermediate_Benefits_and_Risks_of_Smartphones.mp3',42),(43,'file_audio/Technology_Intermediate_Online_Privacy.mp3',43),(44,'file_audio/Technology_Intermediate_Social_Media_Impact.mp3',44);
/*!40000 ALTER TABLE `app_audio` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:36
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_challenge`
--

DROP TABLE IF EXISTS `app_challenge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_challenge` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `difficulty` varchar(10) NOT NULL,
  `reward_points` int NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `participant_count` int NOT NULL,
  `level` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_challenge`
--

LOCK TABLES `app_challenge` WRITE;
/*!40000 ALTER TABLE `app_challenge` DISABLE KEYS */;
INSERT INTO `app_challenge` VALUES (1,'Conversation Starters','Practice starting conversations in various social situations.',1,'easy',100,'2025-05-14 15:01:04.761835','2025-06-01 23:59:59.000000',2,2,'2025-05-14 15:01:04.761835','2025-05-14 15:01:04.761835'),(2,'Business Presentation','Deliver a short business presentation with professional vocabulary.',0,'medium',100,'2025-05-14 15:01:04.765066','2025-06-01 23:59:59.000000',0,2,'2025-05-14 15:01:04.765066','2025-05-14 15:01:04.765066'),(3,'TravelDialogue','Tell a coherent story using past tenses and descriptive vocabulary.',0,'easy',100,'2025-05-14 15:01:04.767419','2025-06-01 23:59:59.000000',1,4,'2025-05-14 15:01:04.767419','2025-05-14 15:01:04.767419'),(4,'Storytelling','Tell a coherent story using past tenses and descriptive vocabulary.',0,'hard',300,'2025-05-14 15:01:04.769489','2025-06-01 23:59:59.000000',0,4,'2025-05-14 15:01:04.769489','2025-05-14 15:01:04.769489'),(5,'PublicSpeech','Tell a coherent story using past tenses and descriptive vocabulary.',0,'hard',100,'2025-05-14 15:01:04.771537','2025-06-01 23:59:59.000000',0,4,'2025-05-14 15:01:04.771537','2025-05-14 15:01:04.771537'),(6,'DebateChallenge','Tell a coherent story using past tenses and descriptive vocabulary.',0,'hard',100,'2025-05-14 15:01:04.772707','2025-06-01 23:59:59.000000',0,4,'2025-05-14 15:01:04.772707','2025-05-14 15:01:04.773707');
/*!40000 ALTER TABLE `app_challenge` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_challengeexercise`
--

DROP TABLE IF EXISTS `app_challengeexercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_challengeexercise` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `order` int NOT NULL,
  `speaking_text_content` longblob NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `challenge_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_challengeexercise_challenge_id_a90fc62e_fk_app_challenge_id` (`challenge_id`),
  CONSTRAINT `app_challengeexercise_challenge_id_a90fc62e_fk_app_challenge_id` FOREIGN KEY (`challenge_id`) REFERENCES `app_challenge` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_challengeexercise`
--

LOCK TABLES `app_challengeexercise` WRITE;
/*!40000 ALTER TABLE `app_challengeexercise` DISABLE KEYS */;
INSERT INTO `app_challengeexercise` VALUES (1,'Hotel Booking','Practice key phrases and vocabulary for reserving rooms and inquiring about hotel services.',1,_binary '476f6f64206d6f726e696e672e20492764206c696b6520746f20696e71756972652061626f757420626f6f6b696e672061207374616e6461726420726f6f6d20666f722074776f206164756c74732066726f6d204a756c79203130746820746f204a756c7920313274682e20436f756c6420796f7520706c65617365206c6574206d65206b6e6f772074686520617661696c6162696c69747920616e64207468652063757272656e74207261746520706572206e696768743f20416c736f2c2061726520746865726520616e79207370656369616c206f666665727320666f7220612074776f2d6e6967687420737461793f','2025-05-14 15:45:05.426566','2025-05-14 15:45:05.426566',1),(2,'Asking for Directions','Learn how to ask for and understand instructions to find various locations.',2,_binary '457863757365206d652c2049276d20747279696e6720746f2066696e6420746865206e65617265737420706f7374206f66666963652e2049276d206e6f742066616d696c6961722077697468207468697320617265612e20436f756c6420796f7520706f737369626c7920706f696e74206d6520696e2074686520726967687420646972656374696f6e206f722074656c6c206d6520686f7720746f206765742074686572652066726f6d20686572653f','2025-05-14 15:45:05.431830','2025-05-14 15:45:05.432337',1),(3,'Ordering Food','Master common expressions and vocabulary for ordering meals and drinks at a restaurant.',3,_binary '48656c6c6f2c2049276d20726561647920746f206f726465722e20492764206c696b6520746f20686176652074686520636869636b656e2073616c6164206173206120737461727465722c20706c656173652e20466f72206d79206d61696e20636f757273652c2049276c6c2074616b65207468652073706167686574746920636172626f6e6172612e20416e6420746f206472696e6b2c206a757374206120626f74746c65206f66207374696c6c2077617465722e','2025-05-14 15:45:05.436083','2025-05-14 15:45:05.436083',1),(4,'Company Overview','Practice presenting essential information about a company\'s mission, services, and structure.',4,_binary '4f757220636f6d70616e792c20496e6e6f7661746520536f6c7574696f6e732c20686173206265656e2061206c656164657220696e2070726f766964696e672063757474696e672d65646765206d61726b6574696e67207374726174656769657320666f72206f7665722061206465636164652e205765207072696465206f757273656c766573206f6e206f757220636c69656e742d63656e7472696320617070726f61636820616e64206f757220636f6d6d69746d656e7420746f2064656c69766572696e67206d656173757261626c6520726573756c74732e204f7572207465616d20636f6e7369737473206f6620657870657269656e6365642070726f66657373696f6e616c732064656469636174656420746f2068656c70696e6720627573696e65737365732067726f772e','2025-05-14 15:45:05.440678','2025-05-14 15:45:05.440678',2),(5,'Product Introduction','Focus on language used to highlight a new product\'s features, benefits, and value.',5,_binary '576527726520746872696c6c656420746f20756e7665696c206f7572206e657720666c61677368697020736d61727470686f6e652c2074686520274e6f766120582e2720497420626f617374732061207265766f6c7574696f6e6172792063616d6572612073797374656d2c20616e20756c7472612d726573706f6e7369766520646973706c61792c20616e6420657874656e6465642062617474657279206c6966652064657369676e656420666f7220746f64617927732064656d616e64696e672075736572732e2057652062656c6965766520746865204e6f766120582077696c6c207265646566696e6520796f7572206d6f62696c6520657870657269656e63652e','2025-05-14 15:45:05.444413','2025-05-14 15:45:05.444413',2),(6,'Closing Remarks','Learn professional phrases to effectively conclude a speech, meeting, or discussion.',6,_binary '546f2073756d2075702c2074686520706f696e74732077652776652064697363757373656420746f64617920686967686c696768742074686520637269746963616c206e65656420666f7220616374696f6e2e20492077616e7420746f207468616e6b2065766572796f6e6520666f722074686569722070617274696369706174696f6e20616e642076616c7561626c6520696e7075742e204c65742773206d6f766520666f7277617264207769746820746865736520696e73696768747320746f2061636869657665206f757220636f6d6d6f6e20676f616c732e','2025-05-14 15:45:05.448242','2025-05-14 15:45:05.448242',2),(7,'Airport Check-In','Practice essential conversations for the airport check-in process, including luggage and flight details.',7,_binary '476f6f642061667465726e6f6f6e2c20492764206c696b6520746f20636865636b20696e20666f72206d7920666c6967687420746f2053696e6761706f72652c20666c69676874206e756d6265722053513137332e2048657265206973206d792070617373706f727420616e6420626f6f6b696e6720636f6e6669726d6174696f6e2e20492068617665206f6e6520737569746361736520746f20636865636b20696e20616e64206f6e652063617272792d6f6e206261672e','2025-05-14 15:45:05.451967','2025-05-14 15:45:05.451967',3),(8,'Asking for Directions','Excuse me, can you help me find the nearest pharmacy? I’m feeling a bit unwell.',8,_binary '457863757365206d652c2049276d207265616c6c7920696e206120687572727920616e642049207365656d20746f206265206c6f73742e2049276d206c6f6f6b696e6720666f722074686520636f6e666572656e63652063656e746572206f6e20456c6d205374726565742e20436f756c6420796f7520757267656e746c792074656c6c206d652074686520717569636b6573742077617920746f206765742074686572652c20706c656173653f','2025-05-14 15:45:05.455244','2025-05-14 15:45:05.455244',3),(9,'Hotel Check-In','Learn the typical phrases and procedures for arriving and registering at a hotel.',9,_binary '48692c204920686176652061207265736572766174696f6e20756e64657220746865206e616d65204a6f686e736f6e2e2049276d20636865636b696e6720696e20746f6461792e20436f756c6420796f7520636f6e6669726d207468652064657461696c7320666f72206d653f20416c736f2c20492764206c696b6520746f206b6e6f7720776861742074696d6520627265616b666173742069732073657276656420616e64206966207468657265277320612067796d20492063616e207573652e','2025-05-14 15:45:05.458511','2025-05-14 15:45:05.458511',3),(10,'My Childhood','Practice using past tenses and descriptive vocabulary to talk about early life experiences.',10,_binary '492068616420612076657279206861707079206368696c64686f6f642067726f77696e6720757020696e206120736d616c6c20746f776e2e2049207573656420746f207370656e64206d792073756d6d65727320706c6179696e67206f7574736964652077697468206d7920667269656e647320756e74696c2073756e7365742e20536f6d65206f66206d7920666f6e64657374206d656d6f72696573206172652066726f6d2074686f73652073696d706c652c20636172656672656520646179732e','2025-05-14 15:45:05.461733','2025-05-14 15:45:05.461733',4),(11,'A Memorable Trip','Focus on narrating a significant travel experience using descriptive language and expressing emotions.',11,_binary '4f6e65206f6620746865206d6f7374206d656d6f7261626c65207472697073204927766520657665722074616b656e2077617320746f2074686520636f617374206f66204974616c792e20546865207374756e6e696e67207669657773206f6620746865204d65646974657272616e65616e205365612c207468652064656c6963696f757320666f6f642c20616e642074686520667269656e646c79206c6f63616c2070656f706c65206d61646520697420616e20756e666f726765747461626c6520657870657269656e63652e204920657370656369616c6c7920656e6a6f796564206578706c6f72696e672074686520616e6369656e74207275696e732e','2025-05-14 15:45:05.465467','2025-05-14 15:45:05.465467',4),(12,'An Unexpected Adventure','Practice storytelling skills by recounting an unforeseen event with clear sequencing and details.',12,_binary '57652077657265206f6e206120706c616e6e65642068696b65207768656e20612073756464656e20666f6720726f6c6c656420696e2c20616e6420776520636f6d706c6574656c79206c6f73742074686520747261696c2e204974207475726e656420696e746f20616e20756e657870656374656420616476656e747572652061732077652068616420746f206e61766967617465207573696e6720616e206f6c64206d617020616e642072656c79206f6e2065616368206f7468657220746f2066696e64206f757220776179206261636b206265666f7265206461726b2e','2025-05-14 15:45:05.469381','2025-05-14 15:45:05.469381',4),(13,'Giving a Speech','Learn fundamental techniques for structuring and delivering an effective public presentation.',13,_binary '476f6f64206d6f726e696e672c2065766572796f6e652e20546f6461792c2049276d206865726520746f2074616c6b2061626f75742074686520696d70616374206f6620736f6369616c206d65646961206f6e20636f6d6d756e69636174696f6e2e20496e206d792070726573656e746174696f6e2c2049276c6c20636f766572207468726565206d61696e20617370656374733a206974732062656e65666974732c2069747320647261776261636b732c20616e6420686f772077652063616e20757365206974206d6f726520726573706f6e7369626c792e','2025-05-14 15:45:05.473733','2025-05-14 15:45:05.473733',5),(14,'Motivational Speech','Explore language and delivery styles aimed at inspiring and encouraging an audience.',14,_binary '4e6f206d617474657220686f77206d616e792074696d657320796f75207374756d626c652c2072656d656d6265722074686174206576657279207365746261636b206973206120736574757020666f72206120636f6d656261636b2e2042656c6965766520696e20796f757220706f74656e7469616c2c207374617920666f6375736564206f6e20796f757220676f616c732c20616e64206e65766572206c6574206665617220686f6c6420796f75206261636b2066726f6d2063686173696e6720796f757220647265616d732e20596f7572206a6f75726e657920697320756e697175652c20736f20656d62726163652069742e','2025-05-14 15:45:05.476879','2025-05-14 15:45:05.476879',5),(15,'Persuasive Speech','Develop skills in constructing arguments and using rhetorical devices to convince listeners.',15,_binary '49207572676520796f7520746f20636f6e7369646572207468652073696e69666963616e7420696d70616374206f6620766f6c756e74656572696e6720696e206f7572206c6f63616c20636f6d6d756e6974792e2042792064656469636174696e67206a75737420612066657720686f7572732061207765656b2c2077652063616e20636f6c6c6563746976656c79206d616b6520612074616e6769626c65206469666572656e636520696e20746865206c69766573206f66206f746865727320616e6420666f737465722061207374726f6e6765722c206d6f726520737570706f7274697665206e696768626f72686f6f6420666f722065766572796f6e652e','2025-05-14 15:45:05.480731','2025-05-14 15:45:05.480731',5),(16,'Agreeing with a Statement','Practice various expressions to affirm an opinion and provide supporting reasons.',16,_binary '49206162736f6c7574656c792061677265652077697468207468652073746174656d656e7420746861742072656164696e6720726567756c61726c7920657870616e6473206f6e65277320686f72697a6f6e732e204974206e6f74206f6e6c7920696d70726f76657320766f636162756c61727920616e6420637269746963616c207468696e6b696e672062757420616c736f206f6666657273206e65772070657273706563746976657320616e6420612064656570657220756e6465727374616e64696e67206f662074686520776f726c642061726f756e642075732e','2025-05-14 15:45:05.485252','2025-05-14 15:45:05.485252',6),(17,'Disagreeing with a Statement','Learn how to politely and clearly express dissent and offer alternative viewpoints.',17,_binary '5768696c6520492073656520796f757220706f696e742061626f75742074686520636f6e76656e69656e6365206f66206f6e6c696e652073686f7070696e672c2049207265737065637466756c6c792064697361677265652074686174206974277320616c7761797320626574746572207468616e20696e2d73746f72652073686f7070696e672e20492062656c6965766520706879736963616c2073746f726573206f6666657220612076616c7561626c6520736f6369616c20696e746572616374696f6e20616e6420746865206162696c69747920746f206173736573732070726f64756374207175616c69747920666972737468616e642c207768696368206f6e6c696e6520706c6174666f726d73206f6674656e206c61636b2e','2025-05-14 15:45:05.488311','2025-05-14 15:45:05.488311',6),(18,'Arguing Both Sides','Practice presenting and contrasting arguments for different perspectives on a single topic.',18,_binary '54686520746f706963206f662072656d6f746520776f726b206365727461696e6c79206861732074776f2064697374696e63742073696465732e204f6e206f6e652068616e642c206974206f666665727320666c65786962696c69747920616e642063616e20696d70726f766520776f726b2d6c6966652062616c616e636520666f7220656d706c6f796565732e204f6e20746865206f746865722068616e642c2069742063616e2070726573656e74206368616c6c656e67657320696e207465726d73206f66207465616d20636f6c6c61626f726174696f6e20616e64206d61696e7461696e696e672061207374726f6e6720636f6d70616e792063756c747572652e','2025-05-14 15:45:05.492307','2025-05-14 15:45:05.492307',6);
/*!40000 ALTER TABLE `app_challengeexercise` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:36
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_genre`
--

DROP TABLE IF EXISTS `app_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_genre` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_genre`
--

LOCK TABLES `app_genre` WRITE;
/*!40000 ALTER TABLE `app_genre` DISABLE KEYS */;
INSERT INTO `app_genre` VALUES (1,'Daily Life'),(4,'Education'),(5,'Family'),(2,'Technology'),(3,'Travel');
/*!40000 ALTER TABLE `app_genre` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_level`
--

DROP TABLE IF EXISTS `app_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_level` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_level`
--

LOCK TABLES `app_level` WRITE;
/*!40000 ALTER TABLE `app_level` DISABLE KEYS */;
INSERT INTO `app_level` VALUES (3,'Advanced'),(1,'Beginner'),(2,'Intermediate');
/*!40000 ALTER TABLE `app_level` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:36
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_speakingresult`
--

DROP TABLE IF EXISTS `app_speakingresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_speakingresult` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_text` longtext NOT NULL,
  `score` decimal(5,2) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `speaking_text_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_speakingresult_speaking_text_id_0f2bc5f1_fk_app_speak` (`speaking_text_id`),
  CONSTRAINT `app_speakingresult_speaking_text_id_0f2bc5f1_fk_app_speak` FOREIGN KEY (`speaking_text_id`) REFERENCES `app_speakingtext` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_speakingresult`
--

LOCK TABLES `app_speakingresult` WRITE;
/*!40000 ALTER TABLE `app_speakingresult` DISABLE KEYS */;
INSERT INTO `app_speakingresult` VALUES (1,'my father Wake Me Up 9:39 My World family sit down and eat together',4.90,'2025-05-25 20:49:47.230737',1),(2,'fine',0.00,'2025-05-28 08:10:37.877411',16),(3,'I will die out what about 30 in this morning I stopped my dresses for a few minutes and monthly my battery and I broke my what might find to feel more I used to eat a simple breakfast and do not open you are some time right now',18.26,'2025-05-28 09:30:19.431901',2),(4,'I will die out what about 30 in this morning I stopped my dresses for a few minutes and monthly my battery and I broke my what might find to feel more I used to eat a simple breakfast and do not open you are some time right now',18.26,'2025-05-28 09:30:28.594300',2),(5,'my family have fire number my father my mother my younger sister my younger brother and me when I asked my house is Mickey and call home on the last one upload and louder my phone at and leave early every morning my mother\'s cell give me a sub and also put this card me fat my sister is in pricing and my brother is shut up baby so I have to take care add kids in time we are not having dinner together and doing now with some story from our day I can with some time we have to sit back and all right brother Austin what a movie at home I love my family very much it cost us about me in everything and on why the power of me to do my bed in school no matter what happen if you don\'t know why be there for me',42.00,'2025-05-28 18:52:06.000030',17);
/*!40000 ALTER TABLE `app_speakingresult` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:36
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_speakingtext`
--

DROP TABLE IF EXISTS `app_speakingtext`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_speakingtext` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` longblob,
  `language` varchar(50) DEFAULT NULL,
  `genre_id` bigint NOT NULL,
  `level_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_speakingtext_genre_id_a2fb145d_fk_app_genre_id` (`genre_id`),
  KEY `app_speakingtext_level_id_21821ad3_fk_app_level_id` (`level_id`),
  CONSTRAINT `app_speakingtext_genre_id_a2fb145d_fk_app_genre_id` FOREIGN KEY (`genre_id`) REFERENCES `app_genre` (`id`),
  CONSTRAINT `app_speakingtext_level_id_21821ad3_fk_app_level_id` FOREIGN KEY (`level_id`) REFERENCES `app_level` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_speakingtext`
--

LOCK TABLES `app_speakingtext` WRITE;
/*!40000 ALTER TABLE `app_speakingtext` DISABLE KEYS */;
INSERT INTO `app_speakingtext` VALUES (1,'My Favorite Meal',_binary 'My favorite meal of the day is dinner because it\'s when my whole family sits down and eats together. We usually have rice, meat, vegetables, and sometimes soup. My mom is a great cook, and I especially love her grilled chicken with fish sauce. During dinner, we talk about what happened during the day, share funny stories, or sometimes discuss serious topics like school or work. It\'s a time when we relax and enjoy each other\'s company. On weekends, we sometimes order pizza or cook something special like hotpot. Dinner is more than just eating for me; it\'s about connection and comfort.','en',1,1),(2,'My Morning Routine',_binary 'Every day, I wake up at around 6:30 in the morning. I start by stretching for a few minutes and making my bed. Then, I brush my teeth and wash my face to feel more awake. I usually eat a simple breakfast like bread, eggs, and a glass of milk or sometimes rice with some meat. After breakfast, I check my school bag to make sure I have all my books and homework. I get dressed in my school uniform and leave the house around 7:15 to catch the bus. I like mornings because the air is fresh and quiet. This morning routine helps me feel ready and positive for the rest of the day.','en',1,1),(3,'My Weekend Plan',_binary 'On weekends, I don\'t have school, so I usually wake up later than usual, around 8:30. In the morning, I eat breakfast with my family, then I do some light cleaning around the house like sweeping or folding laundry. After that, I usually watch a movie or play video games with my younger brother. In the afternoon, we sometimes go out to the park or visit my grandparents. If it\'s raining, I might read a book or scroll through social media. I also try to do some homework before Sunday evening so I don\'t rush on Monday. My weekends help me rest, recharge, and spend time with my loved ones.','en',1,1),(4,'A Typical Day at School',_binary 'On a normal school day, I wake up at 6:30 and get ready by 7:00. I leave the house by 7:15 and arrive at school around 7:45. My classes usually start at 8:00. In the morning, we have math, science, and English, which are my favorite subjects. During the 15-minute break, I usually chat with friends or buy a snack. At noon, we eat lunch in the school canteen. In the afternoon, we often have group work, history, or physical education. Sometimes, we have club activities or extra classes. I go home around 4:30 PM, rest for a bit, and then start my homework. My school days are busy, but I enjoy learning and being with my friends.','en',1,2),(5,'House Chores and Responsibilities',_binary 'At home, I help with several chores. On weekdays, I sweep the floor and clean the dishes after dinner. On weekends, I vacuum the house and help my mom do the laundry. I also take care of my younger sister when my parents are busy. Sometimes I don\'t enjoy doing chores, especially when I\'m tired, but I know it\'s important to share responsibilities. Helping at home teaches me how to be responsible and care about others. I think it also prepares me for the future, when I will need to manage my own home or support my family.','en',1,2),(6,'Managing My Time',_binary 'Time management is something I\'ve been trying to improve. I usually plan my day in the morning or the night before. I write down a list of tasks I need to do, such as homework, chores, or study sessions. I use my phone calendar to set reminders. After school, I rest for a while, then do homework from 5 to 6:30 PM. I try to stop using social media during that time to avoid distractions. In the evening, I relax by reading or watching a short video. Having a clear schedule helps me stay organized and feel less stressed. It also gives me more time for fun and personal goals.','en',1,2),(7,'How My Daily Routine Has Changed',_binary 'My daily routine has changed a lot over the years. When I was younger, I used to wake up late and rush to get ready for school, often skipping breakfast. I didn\'t really plan my time well and would procrastinate on homework. Now, I wake up at 6:30 and start my day with a glass of water and a short stretch. I eat a healthy breakfast and review my to-do list. I use digital tools like apps or notes to organize tasks. I try to balance school, exercise, and rest. I also go to bed earlier than before. These changes have made me more productive and focused. They help me stay calm and confident throughout the day.','en',1,3),(8,'Routine vs. Spontaneity',_binary 'Some people prefer routines, while others like spontaneity. Personally, I enjoy having a routine because it keeps me organized. I wake up at the same time, plan my study sessions, and go to bed early. However, I also like adding something spontaneous to my day, like going for ice cream or visiting a new place. I believe routines give structure, but spontaneity brings excitement. A perfect day, to me, is one that has a mix of both. You know what to expect, but also leave space for surprises. This balance makes life feel more enjoyable and less stressful.','en',1,3),(9,'Work-Life Balance',_binary 'Work-life balance is becoming more important in today\'s fast-paced world. I try to keep a healthy balance between school, personal time, and rest. I set a rule for myself to not do schoolwork after 9 PM so I have time to read or talk with family. On weekends, I sometimes study but also make time for fun like going to the movies or hanging out with friends. If I only focus on studying, I feel stressed. If I only rest, I fall behind. So, I believe finding the right mix is the key to staying happy and productive. This balance keeps my energy high and helps me do better in everything.','en',1,3),(10,'Favorite App',_binary 'My favorite app is YouTube because I can learn and have fun at the same time. There are so many videos about different topics, like English lessons, science experiments, and how to draw. When I don\'t understand something from school, I search for videos to help me. I also watch music videos and cooking shows with my family. I like that I can choose what I want to watch. Sometimes I follow channels that teach new skills, like making crafts or editing videos. YouTube is not only fun but also useful for learning. I think it\'s a great app for students if we use it the right way.','en',2,1),(11,'My Favorite Device',_binary 'My favorite device is my smartphone because I can do many things with it. I use it every day to study, talk to my friends, and relax after school. It\'s small and easy to carry, so I can use it almost anywhere. When I study, I use apps like dictionaries and YouTube to learn new words or watch educational videos. I also listen to music, take pictures, and sometimes play games. The most useful part of my smartphone is the internet because it gives me quick access to information. I try not to use it too much so I can focus on my homework. Even though my phone is not the newest model, it still works well and helps me a lot. I think smartphones are very helpful if we use them in a smart way.','en',2,1),(12,'Phone Usage',_binary 'I use my phone for about two to three hours a day. Most of the time, I use it to chat with friends and check my social media. I also use it to learn English and do research for school projects. Sometimes, I play games or watch funny videos when I need to relax. I try not to use my phone during meals or when I\'m talking to someone face-to-face. At night, I stop using it before going to bed so I can sleep better. Using a phone is fun, but I think we should be careful not to use it too much. It\'s important to find a balance between study, rest, and phone time.','en',2,1),(13,'Future Technology',_binary 'I think future technology will change our lives in amazing ways. We may see robots helping with housework, smart cars that drive themselves, and more advanced tools for learning and communication. I\'m excited about the idea of using virtual reality in classrooms or using apps to learn languages by speaking to AI. Technology will make things faster and more convenient, but it also brings new challenges. For example, some people might lose their jobs because machines can do their work. Others might rely too much on technology and forget how to do things on their own. To prepare for the future, we need to learn how to use technology wisely and keep improving our skills. The future is full of possibilities, and we should be ready to use them in smart and helpful ways.','en',2,3),(14,'Managing Screen Addiction',_binary 'Many people today, especially students, spend hours on their phones or computers every day. We use screens for school, entertainment, and communication. But too much screen time can lead to tired eyes, poor sleep, and less time for family or exercise. I sometimes find it hard to stop watching videos or playing games, even when I know I should study. To manage this, I set time limits for certain apps and take short breaks every hour. I also try to do other activities like reading, walking, or playing sports. It\'s not easy, but having a routine helps. Parents and teachers can guide students by setting good examples and encouraging healthy screen habits.','en',2,3),(15,'A Special Memory',_binary 'One of my favorite memories with my family was our trip to the mountains last summer. It was the first time we went on a vacation together. We stayed in a small wooden house surrounded by trees and fresh air. During the day, we went hiking, took lots of pictures, and had picnics by the river. At night, we sat around a campfire, roasted sweet potatoes, and told stories. It was very cold, but we kept warm with jackets and hot drinks. I remember looking at the stars and feeling very happy to be with my family. That trip made us even closer, and we still talk about it sometimes. It\'s a memory I will never forget because it was full of joy and togetherness.','en',5,1),(16,'Family Activities',_binary 'Every weekend, my family tries to spend time together, no matter how busy we are. Sometimes, we go to the supermarket to buy food and snacks, and other times, we visit the park or go for a walk around the lake. My father enjoys playing badminton, and I sometimes play with him. My mom and I often cook together, especially when she tries a new recipe. We also watch movies or listen to music in the evening. One of my favorite family activities is playing board games because we laugh a lot. Doing things together helps us stay close and understand each other better. Even when we don\'t go out, just talking and eating together at home is special to me.','en',5,1),(17,'Introducing My Family',_binary 'My family has five members: my father, my mother, my younger sister, my younger brother, and me. We live in a small house near the market, and our home is always full of love and laughter. My father works as a driver and leaves early every morning. My mother sells clothes in a shop and also cooks delicious meals for us. My sister is in grade six, and my brother is just a baby, so I help take care of him sometimes. We always have dinner together, and during meals, we share stories from our day. On weekends, we sometimes go to the park, visit our grandparents, or just watch a movie at home. I love my family very much because they support me in everything and always encourage me to do my best in school. No matter what happens, I know my family will always be there for me.','en',5,1),(18,'Family Celebrations',_binary 'In my family, we love to celebrate special occasions together. On birthdays, we decorate the house, cook favorite dishes, and enjoy a small party. We sing, eat cake, and take photos to remember the day. Tet is the biggest celebration for us. Before Tet, we clean the house and prepare traditional foods like banh chung. On New Year\'s Eve, we gather to eat together and wait for fireworks. The next day, we wear new clothes, visit our relatives, and receive lucky money. It\'s a fun time when everyone is happy and relaxed. These celebrations help us feel connected, and we create beautiful memories together. No matter how busy life gets, we always try to make time for family traditions.','en',5,2),(19,'Family Roles',_binary 'In my family, everyone has different roles, and we all help each other. My father works to earn money for our needs, and my mother takes care of the house and cooks for us. Even though she doesn\'t go to an office, she works very hard every day. As the oldest child, I help with small chores like washing dishes, folding clothes, and helping my younger sister with her homework. We also have a routine where my dad does the grocery shopping, and I carry the bags. Sometimes, when my parents are tired, I try to make tea for them or prepare the table for dinner. Doing these small tasks makes me feel responsible and closer to my family. I\'ve learned that sharing the work at home is important and that everyone, no matter their age, can contribute something. It also teaches me to be more caring and respectful toward others.','en',5,2),(20,'Staying in Touch',_binary 'Most of my relatives don\'t live in the same city, so we try our best to stay in touch. We often call each other using video apps, especially on weekends or holidays. My cousins and I also chat online almost every day. We send pictures, play mobile games together, or even help each other with schoolwork. Even though we\'re far apart, technology helps us stay close. During special times like Tet or birthdays, we send greetings and sometimes even gifts through delivery services. These small efforts make our relationships stronger. When we finally meet in person, it feels like we were never far away. I think staying in touch with family is important because it gives us love and support, no matter the distance.','en',5,2),(21,'Changing Family Values',_binary 'Over the years, the values and structure of families have changed a lot. In the past, most families were large and lived together in the same house. Grandparents, parents, and children shared responsibilities and followed strict traditions. Nowadays, many families are smaller, and people focus more on personal freedom and career. Young adults often move out to live independently or even in different countries. Even though people are physically apart, they stay connected through phones and the internet. I think both old and modern family styles have good points. Traditional families teach respect and unity, while modern ones give space for growth and independence. The most important thing is that family members still care for each other, support one another, and maintain strong relationships, no matter where they live or how often they meet.','en',5,3),(22,'Generational Conflicts',_binary 'Sometimes, I have different opinions from my parents or grandparents because we grew up in different times. Older people often value discipline, hard work, and saving money. Young people like me care more about creativity, mental health, and trying new things. For example, I may want to follow a job that I\'m passionate about, while my parents prefer something more stable. These differences can lead to arguments, but I try to understand their point of view. We often talk things out during meals or family meetings. I think the key is to listen, stay calm, and respect each other\'s experiences. Every generation has something valuable to share, and by learning from each other, families can grow stronger together.','en',5,3),(23,'Long-Distance Relationships',_binary 'Living far away from your family or partner can be hard, but it is more common today because of study, work, or migration. At first, it may feel lonely or frustrating not to see your loved ones every day. But with video calls, voice messages, and social media, we can still feel close. My cousin studies in another country, and we talk weekly to share news or give advice. Although we miss each other, we\'ve become better at expressing emotions and solving problems on our own. Long-distance relationships need trust, communication, and effort from both sides. If people stay honest and make time for each other, the relationship can stay strong even with distance.','en',5,3),(24,'My Favorite Subject',_binary 'My favorite subject is English because it is both fun and useful. I enjoy learning new vocabulary, practicing conversations, and listening to short English stories. Our teacher often plays games or uses songs to help us remember words better, which makes the lessons exciting. I also like reading short texts and answering questions because it helps me understand the language more. English is important to me because I want to travel to different countries and be able to talk to people around the world. One day, I hope to study abroad or work in a job where I can use English every day. I also watch English videos on YouTube or listen to English music to improve my skills. Sometimes, I even try to speak English at home with my younger sister, and it helps both of us learn faster. Among all the subjects I study, English makes me feel confident and inspired. I know that if I keep practicing, I will become fluent one day.','en',4,1),(25,'My School',_binary 'I go to a small high school near my house, and I really enjoy studying there. The school is not very big, but it has enough classrooms, a nice library, and a large yard where we can play during breaks. I study many subjects, including English, math, science, and history. Among them, I enjoy English the most because I want to travel in the future. Every day, I look forward to seeing my friends and learning new things. Our teachers are kind and always ready to help us when we don’t understand something. During break time, my friends and I like to sit under a tree, talk about our lessons, or share snacks. Sometimes we play sports like badminton or football if the weather is good. The school also has fun events like Sports Day and the Mid-Autumn Festival. I feel happy going to school because I can grow my knowledge and spend time with good people. My school is a special place that helps me become a better student and a better person every day.','en',4,1),(26,'My Teacher',_binary 'One of the teachers I admire the most is my math teacher, Mr. Minh. He is very friendly, patient, and always explains things clearly. Whenever students don’t understand something, he takes time to go over it again until everyone feels confident. He also uses examples from real life to make lessons more interesting. Although math can be difficult, Mr. Minh makes it fun by turning lessons into small games or group activities. I also like that he gives us helpful feedback on our homework, which helps us avoid making the same mistakes. Outside of class, he sometimes tells us jokes or interesting stories to make us laugh and relax. I feel very lucky to be in his class because I have learned to enjoy math more than I used to. Thanks to him, my grades have improved, and I feel more confident solving math problems. Mr. Minh is not just a good teacher—he is also someone I look up to and respect very much.','en',4,1),(27,'Online vs. Traditional Classes',_binary 'Both online and traditional classes have their advantages and disadvantages, and I\'ve had experience with both. Online learning is convenient because I can study at home and review materials anytime I want. However, sometimes it\'s hard to concentrate during online classes, and I can\'t ask questions easily. Traditional classes allow more interaction with teachers and classmates. I enjoy being in a classroom because I can join group discussions and receive direct help from the teacher. Although online learning saves time, I learn better in face-to-face classes where I feel more engaged and focused.','en',4,2),(28,'Qualities of a Good Teacher',_binary 'A good teacher can make a big difference in how well students learn and how much they enjoy a subject. In my opinion, a good teacher is someone who is patient, explains things clearly, and cares about their students. They listen to questions and help students solve problems without making them feel bad. Good teachers also know how to make lessons fun and interesting. For example, they might use games, real-life examples, or group work to make learning easier. When I have a teacher like this, I feel more motivated to study and do well in class.','en',4,2),(29,'Study Habits',_binary 'I try to maintain good study habits so I can learn better and manage my time well. Every evening after dinner, I spend one to two hours reviewing the lessons I studied during the day. I begin by reading my notes and completing homework assignments. When I don\'t understand something, I search for videos or use apps to help explain the topic. I try to study in a quiet room without my phone nearby, so I don\'t get distracted. On weekends, I spend extra time on subjects that are more difficult for me, such as math. These habits help me stay organized, reduce stress, and improve my learning results.','en',4,2),(30,'AI in Learning',_binary 'Artificial intelligence is becoming a powerful tool in modern education. It can help students learn faster by offering personalized lessons and instant feedback. For example, AI tools can correct grammar mistakes or help students practice speaking with virtual assistants. Teachers can also use AI to track students\' progress and identify areas where they need more help. However, AI cannot replace teachers completely. Human teachers understand emotions, motivate students, and create a real connection that technology lacks. In the future, I think the best classrooms will combine technology with human guidance to give students the best learning experience.','en',4,3),(31,'Education and Success',_binary 'Many people believe that education is the most important factor in achieving success. While it\'s true that education provides us with knowledge and skills needed for many careers, I think it\'s not the only path to success. Some people succeed because of their creativity, hard work, or unique talents. However, education can open doors and give people more choices in life. For example, someone with a good education might find it easier to get a stable job or start their own business. In my opinion, success depends on a mix of education, experience, attitude, and continuous learning. Even after finishing school, we should keep learning new things to improve ourselves. Education is a strong foundation, but what we do with it matters even more.','en',4,3),(32,'Free Education',_binary 'I believe that education should be free for everyone, at least at the basic level. Free education gives children from poor families a chance to go to school and improve their future. It helps reduce the gap between the rich and the poor. However, offering free education is not easy for governments because it requires a lot of money and good management. Besides building schools and paying teachers, they need to make sure the quality stays high. In some countries, free education has already changed lives by helping more people get degrees and find good jobs. If managed properly, free education can benefit the whole society and lead to a stronger economy.','en',4,3),(33,'A Place I Want to Travel',_binary 'I really want to travel to Japan one day. I have seen many videos and pictures of the country, and it looks amazing. I want to visit Tokyo and see the tall buildings and colorful lights. I also want to try sushi and wear a traditional kimono. During the spring, I would love to see the cherry blossoms. They look so beautiful in the photos. I also want to visit old temples and learn more about Japanese culture. It\'s a dream of mine, and I hope I can go there someday with my best friend. I think traveling to Japan would be fun, exciting, and a great learning experience.','en',3,1),(34,'My Favorite Place to Visit',_binary 'My favorite place to visit is the beach. Every summer, my family and I take a short trip to the seaside, and I always look forward to it. I love the feeling of walking barefoot on the soft sand and listening to the sound of the waves. My siblings and I often build sandcastles and play in the water. Sometimes we bring snacks and have a picnic near the shore. My dad usually takes photos of the sunset, and they always look beautiful. I feel relaxed and happy when I go to the beach. It helps me forget stress and enjoy nature. The fresh air and gentle breeze make me feel calm. If I could, I would go to the beach every weekend.','en',3,1),(35,'Packing for a Trip',_binary 'When I go on a trip, I always make a list to help me pack. First, I pack clothes depending on the weather. If it\'s cold, I bring jackets and sweaters. If it\'s hot, I pack T-shirts and shorts. I also bring my toothbrush, shampoo, and other personal things. I never forget my phone charger and a book to read. My mom helps me remember important things like my ID card or money. Packing early helps me feel calm before the trip. I like being ready so I can enjoy the travel without worrying. I also bring a camera to take pictures of special moments.','en',3,1),(36,'A Memorable Trip',_binary 'One of the most memorable trips I\'ve taken was to Da Lat with my family during summer vacation. We stayed in a cozy guesthouse surrounded by flowers and hills. The weather was cool and refreshing, which was a big change from the heat in my hometown. We visited beautiful gardens, explored waterfalls, and went to the night market. I really enjoyed riding a bicycle around Xuan Huong Lake and eating sweet strawberries from local farms. At night, we gathered around a small fire to drink hot soy milk and talk about our day. It was peaceful and meaningful. This trip brought our family closer together and gave me wonderful memories that I will never forget.','en',3,2),(37,'Solo vs. Group Travel',_binary 'Traveling alone and traveling with friends are two very different experiences. When I travel alone, I have more freedom to decide where to go, what to eat, and how long to stay. It\'s a great way to learn about myself and enjoy peace and quiet. However, traveling with friends is more fun. We can laugh together, take group photos, and help each other if something goes wrong. Also, it feels safer to have someone with me in a new place. I think both solo and group travel are valuable, and I enjoy mixing both types depending on the situation.','en',3,2),(38,'Transportation Preferences',_binary 'When it comes to traveling, I prefer going by airplane, especially for long distances. It\'s fast, comfortable, and saves time. I enjoy looking out of the window and watching the clouds during the flight. For short trips, I like traveling by train because it\'s smooth and I can enjoy the countryside views. I don\'t really enjoy bus rides because they are often crowded and take too long. Trains are more relaxing, but planes are the best for time-saving. Each mode of transportation has its pros and cons, and I choose based on the distance, cost, and how quickly I want to get there.','en',3,2),(39,'Learning Through Travel',_binary 'Traveling teaches us much more than school alone. It opens our eyes to different ways of life and helps us become more understanding and adaptable. For example, when I visited a small village in the mountains, I stayed with a local family and helped them with their daily work. I learned how they cooked, grew vegetables, and worked together. This experience gave me a deep appreciation for simple things and showed me how different life can be. Travel helps us grow emotionally, improve communication, and learn real-life problem-solving skills.','en',3,3),(40,'Limiting Tourism',_binary 'Tourism is important for many countries, but too much of it can cause harm. Over-tourism can damage the environment, raise prices for local people, and overcrowd cities. To solve this, I think governments should limit the number of tourists in popular places. For example, they can set daily visitor limits or increase ticket prices to protect important landmarks. They should also promote travel during off-peak seasons. Sustainable tourism helps keep places clean and safe for both visitors and local people. We should all travel more responsibly.','en',3,3),(41,'Tourism and Local Culture',_binary 'Tourism can greatly influence local culture, both positively and negatively. On the positive side, tourism creates jobs, increases income, and helps people learn about different cultures. However, too many tourists can lead to pollution, disrespect for traditions, and the loss of cultural identity. In some places, local traditions are changed just to entertain visitors. I believe tourists should make an effort to understand and respect the local culture. Governments can also help by setting rules to protect heritage sites and promoting responsible tourism.','en',3,3),(42,'Benefits and Risks of Smartphones',_binary 'Smartphones have changed how we live, study, and communicate. They help us find information quickly, stay in touch with friends, and learn new things. I use my phone to check emails, take photos, listen to music, and study English. It\'s very convenient and saves time. But using a smartphone too much can also be a problem. Some people spend hours looking at screens, which can hurt their eyes and cause them to sleep late. Sometimes we forget to talk to people face-to-face because we\'re busy texting or watching videos. I think smartphones are very useful tools, but we must use them carefully. Setting time limits and turning off notifications can help us avoid becoming addicted.','en',2,2),(43,'Online Privacy',_binary 'Online privacy is something I\'ve started thinking about more as I use the internet every day. I know that when I post pictures or write something online, other people can see it, even if I delete it later. That\'s why I don\'t share personal information like my address or phone number on social media. I also try to use strong passwords and don\'t click on strange links. Some of my friends have had their accounts hacked, and they lost photos or messages. I believe schools should teach students how to stay safe online because not everyone knows about digital risks. Being smart and careful online helps protect our privacy and keeps us safe from cyber problems.','en',2,2),(44,'Social Media Impact',_binary 'Social media has become a big part of our lives, especially for young people like me. I use apps like Facebook, Instagram, and TikTok to stay in touch with friends and share moments from my day. It\'s a great way to connect with people and see what\'s happening in the world. However, I sometimes spend too much time scrolling and watching short videos. This makes it hard to focus on my homework or spend time with my family. I also see posts that make me feel I have to look perfect or be popular, which can be stressful. Even though social media is useful, I think we should learn to use it wisely. I try to check my apps only a few times a day and take breaks when I need to. Using social media in a healthy way can help us stay connected without losing control of our time or emotions.','en',2,2);
/*!40000 ALTER TABLE `app_speakingtext` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_useraudio`
--

DROP TABLE IF EXISTS `app_useraudio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_useraudio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `audio_file` varchar(100) DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_useraudio_user_id_ee18ad0a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `app_useraudio_user_id_ee18ad0a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_useraudio`
--

LOCK TABLES `app_useraudio` WRITE;
/*!40000 ALTER TABLE `app_useraudio` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_useraudio` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_userchallengeprogress`
--

DROP TABLE IF EXISTS `app_userchallengeprogress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_userchallengeprogress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` int NOT NULL,
  `completion_percentage` double NOT NULL,
  `status` varchar(20) NOT NULL,
  `last_attempted_date` datetime(6) NOT NULL,
  `completed_date` datetime(6) DEFAULT NULL,
  `challenge_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_userchallengeprogress_user_id_challenge_id_60dd877e_uniq` (`user_id`,`challenge_id`),
  KEY `app_userchallengepro_challenge_id_8fdf6838_fk_app_chall` (`challenge_id`),
  CONSTRAINT `app_userchallengepro_challenge_id_8fdf6838_fk_app_chall` FOREIGN KEY (`challenge_id`) REFERENCES `app_challenge` (`id`),
  CONSTRAINT `app_userchallengeprogress_user_id_507a0399_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_userchallengeprogress`
--

LOCK TABLES `app_userchallengeprogress` WRITE;
/*!40000 ALTER TABLE `app_userchallengeprogress` DISABLE KEYS */;
INSERT INTO `app_userchallengeprogress` VALUES (1,75,100,'completed','2025-05-29 07:25:32.776257','2025-05-29 07:25:32.776257',1,6),(2,89,100,'completed','2025-05-28 08:03:33.954237','2025-05-28 08:03:33.954237',1,2),(3,165,100,'completed','2025-05-29 07:31:59.285724','2025-05-29 07:31:59.285724',3,3);
/*!40000 ALTER TABLE `app_userchallengeprogress` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_userexerciseattempt`
--

DROP TABLE IF EXISTS `app_userexerciseattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_userexerciseattempt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_audio_file_path` varchar(100) DEFAULT NULL,
  `transcribed_text` longtext NOT NULL,
  `score` double NOT NULL,
  `detailed_feedback` json NOT NULL,
  `attempted_at` datetime(6) NOT NULL,
  `challenge_exercise_id` bigint NOT NULL,
  `user_challenge_progress_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_userexerciseatte_challenge_exercise_i_b58dbfba_fk_app_chall` (`challenge_exercise_id`),
  KEY `app_userexerciseatte_user_challenge_progr_adb34305_fk_app_userc` (`user_challenge_progress_id`),
  CONSTRAINT `app_userexerciseatte_challenge_exercise_i_b58dbfba_fk_app_chall` FOREIGN KEY (`challenge_exercise_id`) REFERENCES `app_challengeexercise` (`id`),
  CONSTRAINT `app_userexerciseatte_user_challenge_progr_adb34305_fk_app_userc` FOREIGN KEY (`user_challenge_progress_id`) REFERENCES `app_userchallengeprogress` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_userexerciseattempt`
--

LOCK TABLES `app_userexerciseattempt` WRITE;
/*!40000 ALTER TABLE `app_userexerciseattempt` DISABLE KEYS */;
INSERT INTO `app_userexerciseattempt` VALUES (1,'challenge_audio/exercise_1.webm','good morning good about what\'s the temperature at 4:20',6.82,'{\"score\": 6.82, \"user_text\": [{\"word\": \"good\", \"status\": \"correct\"}, {\"word\": \"morning\", \"status\": \"wrong\", \"expected\": \"morning.\"}, {\"word\": \"good\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"about\", \"status\": \"correct\"}, {\"word\": \"what\'s\", \"status\": \"wrong\", \"expected\": \"booking\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"temperature\", \"status\": \"wrong\", \"expected\": \"availability\"}, {\"word\": \"at\", \"status\": \"wrong\", \"expected\": \"and\"}, {\"word\": \"4:20\", \"status\": \"wrong\", \"expected\": \"the\"}], \"original_text\": \"Good morning. I\'d like to inquire about booking a standard room for two adults from July 10th to July 12th. Could you please let me know the availability and the current rate per night? Also, are there any special offers for a two-night stay?\"}','2025-05-24 07:48:19.761330',1,1),(2,'challenge_audio/exercise.webm','hello I stopped my baby',0,'{\"score\": 0.0, \"user_text\": [{\"word\": \"hello\", \"status\": \"wrong\", \"expected\": \"good\"}, {\"word\": \"i\", \"status\": \"wrong\", \"expected\": \"morning.\"}, {\"word\": \"stopped\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"my\", \"status\": \"wrong\", \"expected\": \"like\"}, {\"word\": \"baby\", \"status\": \"wrong\", \"expected\": \"to\"}], \"original_text\": \"Good morning. I\'d like to inquire about booking a standard room for two adults from July 10th to July 12th. Could you please let me know the availability and the current rate per night? Also, are there any special offers for a two-night stay?\"}','2025-05-24 08:13:28.453830',1,1),(3,'challenge_audio/exercise_FoGuT4F.webm','okay',0,'{\"score\": 0.0, \"user_text\": [{\"word\": \"okay\", \"status\": \"wrong\", \"expected\": \"good\"}], \"original_text\": \"Good morning. I\'d like to inquire about booking a standard room for two adults from July 10th to July 12th. Could you please let me know the availability and the current rate per night? Also, are there any special offers for a two-night stay?\"}','2025-05-25 08:14:56.907091',1,1),(4,'challenge_audio/exercise.webm','good morning I would like to inquire about food',11.36,'{\"score\": 11.36, \"user_text\": [{\"word\": \"good\", \"status\": \"correct\"}, {\"word\": \"morning\", \"status\": \"wrong\", \"expected\": \"morning.\"}, {\"word\": \"i\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"like\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"inquire\", \"status\": \"correct\"}, {\"word\": \"about\", \"status\": \"correct\"}, {\"word\": \"food\", \"status\": \"wrong\", \"expected\": \"booking\"}], \"original_text\": \"Good morning. I\'d like to inquire about booking a standard room for two adults from July 10th to July 12th. Could you please let me know the availability and the current rate per night? Also, are there any special offers for a two-night stay?\"}','2025-05-28 08:01:38.339385',1,2),(5,'challenge_audio/exercise_A8zAepW.webm','kill me I am trying to find the nearest post office can you possibly for me the right direction not tell me how to get there from here',55.88,'{\"score\": 55.88, \"user_text\": [{\"word\": \"kill\", \"status\": \"wrong\", \"expected\": \"excuse\"}, {\"word\": \"me\", \"status\": \"wrong\", \"expected\": \"me,\"}, {\"word\": \"i\", \"status\": \"wrong\", \"expected\": \"i\'m\"}, {\"word\": \"trying\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"find\", \"status\": \"correct\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"nearest\", \"status\": \"correct\"}, {\"word\": \"post\", \"status\": \"correct\"}, {\"word\": \"office\", \"status\": \"wrong\", \"expected\": \"office.\"}, {\"word\": \"can\", \"status\": \"wrong\", \"expected\": \"i\'m\"}, {\"word\": \"you\", \"status\": \"correct\"}, {\"word\": \"possibly\", \"status\": \"correct\"}, {\"word\": \"for\", \"status\": \"wrong\", \"expected\": \"point\"}, {\"word\": \"me\", \"status\": \"correct\"}, {\"word\": \"in\", \"status\": \"missing\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"right\", \"status\": \"correct\"}, {\"word\": \"direction\", \"status\": \"correct\"}, {\"word\": \"not\", \"status\": \"wrong\", \"expected\": \"or\"}, {\"word\": \"tell\", \"status\": \"correct\"}, {\"word\": \"me\", \"status\": \"correct\"}, {\"word\": \"how\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"get\", \"status\": \"correct\"}, {\"word\": \"there\", \"status\": \"correct\"}, {\"word\": \"from\", \"status\": \"correct\"}, {\"word\": \"here\", \"status\": \"wrong\", \"expected\": \"here?\"}], \"original_text\": \"Excuse me, I\'m trying to find the nearest post office. I\'m not familiar with this area. Could you possibly point me in the right direction or tell me how to get there from here?\"}','2025-05-28 08:02:58.526467',2,2),(6,'challenge_audio/exercise_IKiuNps.webm','hello I\'m ready to offer I would like to have a chicken salad recipe',23.53,'{\"score\": 23.53, \"user_text\": [{\"word\": \"hello\", \"status\": \"wrong\", \"expected\": \"hello,\"}, {\"word\": \"i\'m\", \"status\": \"correct\"}, {\"word\": \"ready\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"offer\", \"status\": \"wrong\", \"expected\": \"order.\"}, {\"word\": \"i\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"like\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"have\", \"status\": \"correct\"}, {\"word\": \"a\", \"status\": \"wrong\", \"expected\": \"the\"}, {\"word\": \"chicken\", \"status\": \"correct\"}, {\"word\": \"salad\", \"status\": \"correct\"}, {\"word\": \"recipe\", \"status\": \"wrong\", \"expected\": \"as\"}], \"original_text\": \"Hello, I\'m ready to order. I\'d like to have the chicken salad as a starter, please. For my main course, I\'ll take the spaghetti carbonara. And to drink, just a bottle of still water.\"}','2025-05-28 08:03:33.811486',3,2),(7,'challenge_audio/exercise_1GAeusE.webm','excuse me I\'m trying to find another office on the family with this area here possibly upon me in the Riders and I\'ll tell me how to get there from here',55.88,'{\"score\": 55.88, \"user_text\": [{\"word\": \"excuse\", \"status\": \"correct\"}, {\"word\": \"me\", \"status\": \"wrong\", \"expected\": \"me,\"}, {\"word\": \"i\'m\", \"status\": \"correct\"}, {\"word\": \"trying\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"find\", \"status\": \"correct\"}, {\"word\": \"another\", \"status\": \"wrong\", \"expected\": null}, {\"word\": \"office\", \"status\": \"wrong\", \"expected\": null}, {\"word\": \"on\", \"status\": \"wrong\", \"expected\": null}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"family\", \"status\": \"wrong\", \"expected\": \"nearest\"}, {\"word\": \"with\", \"status\": \"correct\"}, {\"word\": \"this\", \"status\": \"correct\"}, {\"word\": \"area\", \"status\": \"wrong\", \"expected\": \"area.\"}, {\"word\": \"here\", \"status\": \"wrong\", \"expected\": \"could\"}, {\"word\": \"possibly\", \"status\": \"correct\"}, {\"word\": \"upon\", \"status\": \"wrong\", \"expected\": \"point\"}, {\"word\": \"me\", \"status\": \"correct\"}, {\"word\": \"in\", \"status\": \"correct\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"riders\", \"status\": \"wrong\", \"expected\": \"right\"}, {\"word\": \"and\", \"status\": \"wrong\", \"expected\": \"direction\"}, {\"word\": \"i\'ll\", \"status\": \"wrong\", \"expected\": \"or\"}, {\"word\": \"tell\", \"status\": \"correct\"}, {\"word\": \"me\", \"status\": \"correct\"}, {\"word\": \"how\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"get\", \"status\": \"correct\"}, {\"word\": \"there\", \"status\": \"correct\"}, {\"word\": \"from\", \"status\": \"correct\"}, {\"word\": \"here\", \"status\": \"wrong\", \"expected\": \"here?\"}], \"original_text\": \"Excuse me, I\'m trying to find the nearest post office. I\'m not familiar with this area. Could you possibly point me in the right direction or tell me how to get there from here?\"}','2025-05-29 07:25:07.566566',2,1),(8,'challenge_audio/exercise_tiqKVDI.webm','hello I\'m ready to order a lot of head chicken salad recipe',14.71,'{\"score\": 14.71, \"user_text\": [{\"word\": \"hello\", \"status\": \"wrong\", \"expected\": \"hello,\"}, {\"word\": \"i\'m\", \"status\": \"correct\"}, {\"word\": \"ready\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"order\", \"status\": \"wrong\", \"expected\": \"order.\"}, {\"word\": \"a\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"lot\", \"status\": \"wrong\", \"expected\": \"like\"}, {\"word\": \"of\", \"status\": \"wrong\", \"expected\": \"to\"}, {\"word\": \"head\", \"status\": \"wrong\", \"expected\": \"have\"}, {\"word\": \"chicken\", \"status\": \"correct\"}, {\"word\": \"salad\", \"status\": \"correct\"}, {\"word\": \"recipe\", \"status\": \"wrong\", \"expected\": \"as\"}], \"original_text\": \"Hello, I\'m ready to order. I\'d like to have the chicken salad as a starter, please. For my main course, I\'ll take the spaghetti carbonara. And to drink, just a bottle of still water.\"}','2025-05-29 07:25:32.768302',3,1),(9,'challenge_audio/exercise_1BwCwwZ.webm','good afternoon I like to check in my department like those Singapore by the SQL 173 yeah in my passport and booking confirmation I have one just got to change in one carry on',48.48,'{\"score\": 48.48, \"user_text\": [{\"word\": \"good\", \"status\": \"correct\"}, {\"word\": \"afternoon\", \"status\": \"wrong\", \"expected\": \"afternoon,\"}, {\"word\": \"i\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"like\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"check\", \"status\": \"correct\"}, {\"word\": \"in\", \"status\": \"correct\"}, {\"word\": \"for\", \"status\": \"missing\"}, {\"word\": \"my\", \"status\": \"correct\"}, {\"word\": \"department\", \"status\": \"wrong\", \"expected\": \"flight\"}, {\"word\": \"like\", \"status\": \"wrong\", \"expected\": \"to\"}, {\"word\": \"those\", \"status\": \"wrong\", \"expected\": \"singapore,\"}, {\"word\": \"singapore\", \"status\": \"wrong\", \"expected\": \"flight\"}, {\"word\": \"by\", \"status\": \"wrong\", \"expected\": \"number\"}, {\"word\": \"the\", \"status\": \"wrong\", \"expected\": \"sq173.\"}, {\"word\": \"sql\", \"status\": \"wrong\", \"expected\": \"here\"}, {\"word\": \"173\", \"status\": \"wrong\", \"expected\": \"is\"}, {\"word\": \"my\", \"status\": \"correct\"}, {\"word\": \"passport\", \"status\": \"correct\"}, {\"word\": \"and\", \"status\": \"correct\"}, {\"word\": \"booking\", \"status\": \"correct\"}, {\"word\": \"confirmation\", \"status\": \"wrong\", \"expected\": \"confirmation.\"}, {\"word\": \"i\", \"status\": \"correct\"}, {\"word\": \"have\", \"status\": \"correct\"}, {\"word\": \"one\", \"status\": \"correct\"}, {\"word\": \"just\", \"status\": \"wrong\", \"expected\": \"suitcase\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"change\", \"status\": \"wrong\", \"expected\": \"check\"}, {\"word\": \"in\", \"status\": \"correct\"}, {\"word\": \"and\", \"status\": \"missing\"}, {\"word\": \"one\", \"status\": \"correct\"}, {\"word\": \"carry\", \"status\": \"wrong\", \"expected\": \"carry-on\"}, {\"word\": \"on\", \"status\": \"wrong\", \"expected\": \"bag.\"}], \"original_text\": \"Good afternoon, I\'d like to check in for my flight to Singapore, flight number SQ173. Here is my passport and booking confirmation. I have one suitcase to check in and one carry-on bag.\"}','2025-05-29 07:30:43.546723',7,3),(10,'challenge_audio/exercise_ykjWU8o.webm','excuse me I\'m ready in a hurry and seem to be lost I\'m looking for your conference center on Elm Street tell me the quickest way to get there please',67.65,'{\"score\": 67.65, \"user_text\": [{\"word\": \"excuse\", \"status\": \"correct\"}, {\"word\": \"me\", \"status\": \"wrong\", \"expected\": \"me,\"}, {\"word\": \"i\'m\", \"status\": \"correct\"}, {\"word\": \"ready\", \"status\": \"wrong\", \"expected\": \"really\"}, {\"word\": \"in\", \"status\": \"correct\"}, {\"word\": \"a\", \"status\": \"correct\"}, {\"word\": \"hurry\", \"status\": \"correct\"}, {\"word\": \"and\", \"status\": \"correct\"}, {\"word\": \"i\", \"status\": \"missing\"}, {\"word\": \"seem\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"be\", \"status\": \"correct\"}, {\"word\": \"lost\", \"status\": \"wrong\", \"expected\": \"lost.\"}, {\"word\": \"i\'m\", \"status\": \"correct\"}, {\"word\": \"looking\", \"status\": \"correct\"}, {\"word\": \"for\", \"status\": \"correct\"}, {\"word\": \"your\", \"status\": \"wrong\", \"expected\": \"the\"}, {\"word\": \"conference\", \"status\": \"correct\"}, {\"word\": \"center\", \"status\": \"correct\"}, {\"word\": \"on\", \"status\": \"correct\"}, {\"word\": \"elm\", \"status\": \"correct\"}, {\"word\": \"street\", \"status\": \"wrong\", \"expected\": \"street.\"}, {\"word\": \"tell\", \"status\": \"correct\"}, {\"word\": \"me\", \"status\": \"correct\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"quickest\", \"status\": \"correct\"}, {\"word\": \"way\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"get\", \"status\": \"correct\"}, {\"word\": \"there\", \"status\": \"wrong\", \"expected\": \"there,\"}, {\"word\": \"please\", \"status\": \"wrong\", \"expected\": \"please?\"}], \"original_text\": \"Excuse me, I\'m really in a hurry and I seem to be lost. I\'m looking for the conference center on Elm Street. Could you urgently tell me the quickest way to get there, please?\"}','2025-05-29 07:31:29.854298',8,3),(11,'challenge_audio/exercise_9MOq4s9.webm','I had a reverse situation under the name Johnson I\'m checking in today could you confirm the detail for me also I would like to know what time breakfast',50,'{\"score\": 50.0, \"user_text\": [{\"word\": \"hi,\", \"status\": \"missing\"}, {\"word\": \"i\", \"status\": \"correct\"}, {\"word\": \"had\", \"status\": \"wrong\", \"expected\": \"have\"}, {\"word\": \"a\", \"status\": \"correct\"}, {\"word\": \"reverse\", \"status\": \"wrong\", \"expected\": \"reservation\"}, {\"word\": \"under\", \"status\": \"correct\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"name\", \"status\": \"correct\"}, {\"word\": \"johnson\", \"status\": \"wrong\", \"expected\": \"johnson.\"}, {\"word\": \"i\'m\", \"status\": \"correct\"}, {\"word\": \"checking\", \"status\": \"correct\"}, {\"word\": \"in\", \"status\": \"correct\"}, {\"word\": \"today\", \"status\": \"wrong\", \"expected\": \"today.\"}, {\"word\": \"could\", \"status\": \"correct\"}, {\"word\": \"you\", \"status\": \"correct\"}, {\"word\": \"confirm\", \"status\": \"correct\"}, {\"word\": \"the\", \"status\": \"correct\"}, {\"word\": \"detail\", \"status\": \"wrong\", \"expected\": \"details\"}, {\"word\": \"for\", \"status\": \"correct\"}, {\"word\": \"me\", \"status\": \"wrong\", \"expected\": \"me?\"}, {\"word\": \"also\", \"status\": \"wrong\", \"expected\": \"also,\"}, {\"word\": \"i\", \"status\": \"wrong\", \"expected\": \"i\'d\"}, {\"word\": \"like\", \"status\": \"correct\"}, {\"word\": \"to\", \"status\": \"correct\"}, {\"word\": \"know\", \"status\": \"correct\"}, {\"word\": \"what\", \"status\": \"correct\"}, {\"word\": \"time\", \"status\": \"correct\"}, {\"word\": \"breakfast\", \"status\": \"correct\"}, {\"word\": \"is\", \"status\": \"missing\"}, {\"word\": \"served\", \"status\": \"missing\"}, {\"word\": \"and\", \"status\": \"missing\"}, {\"word\": \"if\", \"status\": \"missing\"}, {\"word\": \"there\'s\", \"status\": \"missing\"}, {\"word\": \"a\", \"status\": \"missing\"}, {\"word\": \"gym\", \"status\": \"missing\"}, {\"word\": \"i\", \"status\": \"missing\"}, {\"word\": \"can\", \"status\": \"missing\"}, {\"word\": \"use.\", \"status\": \"missing\"}], \"original_text\": \"Hi, I have a reservation under the name Johnson. I\'m checking in today. Could you confirm the details for me? Also, I\'d like to know what time breakfast is served and if there\'s a gym I can use.\"}','2025-05-29 07:31:59.277885',9,3);
/*!40000 ALTER TABLE `app_userexerciseattempt` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_userloginstreak`
--

DROP TABLE IF EXISTS `app_userloginstreak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_userloginstreak` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login_date` date DEFAULT NULL,
  `streak_count` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `app_userloginstreak_user_id_5e155f93_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_userloginstreak`
--

LOCK TABLES `app_userloginstreak` WRITE;
/*!40000 ALTER TABLE `app_userloginstreak` DISABLE KEYS */;
INSERT INTO `app_userloginstreak` VALUES (1,'2025-05-29',2,1),(2,'2025-05-29',2,2),(3,'2025-05-29',1,11),(4,'2025-05-29',1,6),(5,'2025-05-29',1,7),(6,'2025-05-29',1,3);
/*!40000 ALTER TABLE `app_userloginstreak` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_userweeklyscore`
--

DROP TABLE IF EXISTS `app_userweeklyscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_userweeklyscore` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL,
  `week` int NOT NULL,
  `total_score` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_userweeklyscore_user_id_year_week_fbfceb01_uniq` (`user_id`,`year`,`week`),
  CONSTRAINT `app_userweeklyscore_user_id_04939d3a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_userweeklyscore`
--

LOCK TABLES `app_userweeklyscore` WRITE;
/*!40000 ALTER TABLE `app_userweeklyscore` DISABLE KEYS */;
INSERT INTO `app_userweeklyscore` VALUES (1,2025,22,89,2),(2,2025,22,69,6),(3,2025,22,165,3);
/*!40000 ALTER TABLE `app_userweeklyscore` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:36
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add genre',7,'add_genre'),(26,'Can change genre',7,'change_genre'),(27,'Can delete genre',7,'delete_genre'),(28,'Can view genre',7,'view_genre'),(29,'Can add speaking text',8,'add_speakingtext'),(30,'Can change speaking text',8,'change_speakingtext'),(31,'Can delete speaking text',8,'delete_speakingtext'),(32,'Can view speaking text',8,'view_speakingtext'),(33,'Can add audio',9,'add_audio'),(34,'Can change audio',9,'change_audio'),(35,'Can delete audio',9,'delete_audio'),(36,'Can view audio',9,'view_audio'),(37,'Can add speaking result',10,'add_speakingresult'),(38,'Can change speaking result',10,'change_speakingresult'),(39,'Can delete speaking result',10,'delete_speakingresult'),(40,'Can view speaking result',10,'view_speakingresult'),(41,'Can add level',11,'add_level'),(42,'Can change level',11,'change_level'),(43,'Can delete level',11,'delete_level'),(44,'Can view level',11,'view_level'),(45,'Can add user audio',12,'add_useraudio'),(46,'Can change user audio',12,'change_useraudio'),(47,'Can delete user audio',12,'delete_useraudio'),(48,'Can view user audio',12,'view_useraudio'),(49,'Can add challenge',13,'add_challenge'),(50,'Can change challenge',13,'change_challenge'),(51,'Can delete challenge',13,'delete_challenge'),(52,'Can view challenge',13,'view_challenge'),(53,'Can add challenge exercise',14,'add_challengeexercise'),(54,'Can change challenge exercise',14,'change_challengeexercise'),(55,'Can delete challenge exercise',14,'delete_challengeexercise'),(56,'Can view challenge exercise',14,'view_challengeexercise'),(57,'Can add user challenge progress',15,'add_userchallengeprogress'),(58,'Can change user challenge progress',15,'change_userchallengeprogress'),(59,'Can delete user challenge progress',15,'delete_userchallengeprogress'),(60,'Can view user challenge progress',15,'view_userchallengeprogress'),(61,'Can add user exercise attempt',16,'add_userexerciseattempt'),(62,'Can change user exercise attempt',16,'change_userexerciseattempt'),(63,'Can delete user exercise attempt',16,'delete_userexerciseattempt'),(64,'Can view user exercise attempt',16,'view_userexerciseattempt'),(65,'Can add user login streak',17,'add_userloginstreak'),(66,'Can change user login streak',17,'change_userloginstreak'),(67,'Can delete user login streak',17,'delete_userloginstreak'),(68,'Can view user login streak',17,'view_userloginstreak'),(69,'Can add user weekly score',18,'add_userweeklyscore'),(70,'Can change user weekly score',18,'change_userweeklyscore'),(71,'Can delete user weekly score',18,'delete_userweeklyscore'),(72,'Can view user weekly score',18,'view_userweeklyscore');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$9T3RQtNXhdWNOdcRVOh0YE$aqiWTyrWiSRYOn36nq+UwpA1dBs6QFkOwToAbrkxmY0=',NULL,1,'admin','','','',1,1,'2025-05-25 20:20:39.616684'),(2,'pbkdf2_sha256$1000000$yyD4rc2fSh6CHbK9O7cUp6$7gC1mIhylvAkdxCPY4w3QMC9HoWoTfB3zuEXBLuF/bw=',NULL,0,'Rice','Tran','Van Tam','vtam0805@gmail.com',0,1,'2025-05-25 20:29:42.835438'),(3,'pbkdf2_sha256$1000000$RHjoojQOPuAVjhhAXqhbyv$puWUMtZP/ScfJgaD5QpqURFcYLiND1eFzCWwmE5i24E=',NULL,0,'Khanh','','','khanh@gmail.com',0,1,'2025-05-25 08:32:33.625131'),(4,'pbkdf2_sha256$870000$FBRSafAUzO2WL9BMiPLPsl$CW7MNmT+e9jWC1T7iZzyqY/VSBgCIyxfvyA0fFNgv4I=',NULL,1,'tam','','','TRANVANTAM080503@GMAIL.COM',1,0,'2025-04-20 18:28:53.373318'),(5,'pbkdf2_sha256$1000000$aoxpylFyzQXGj4Rl57IGSc$1k0EYFeQHOoe6TmnD2vnaeqQmJ0F84SuBsNhO0jTmTM=',NULL,0,'ttt','','','anh3tam203@gmail.com',0,1,'2025-05-13 08:57:00.993630'),(6,'pbkdf2_sha256$1000000$xN6TmfgexUaHL890On9n3U$Nq1UAN2LmpYIv2SBqj3eff1RCtZP8sHzpyI3y86etnM=',NULL,0,'long','Long','Nguyễn Hạ','rongbayphuongnam@gmail.com',0,1,'2025-05-14 21:30:42.435307'),(7,'pbkdf2_sha256$1000000$uIMumCQsQ9CRqawwnJipzG$Os3qVW1P4Uo8er6jKDC58tZAPT583oJMqptsQfV5hT0=',NULL,1,'Hlg','','','Hlg@gmail.com',1,1,'2025-05-17 07:17:21.667047'),(8,'pbkdf2_sha256$1000000$WkJj5DU69PeMiJAKxzO23n$0MQEefyJI6diAPkfKHK7NEE62/v394wZCe/CQTQN/Lo=',NULL,0,'DuyTan','','','duytan@gmail.com',0,1,'2025-05-25 08:30:39.095731'),(9,'pbkdf2_sha256$1000000$A7GB3AB5cR2RQldCGP9vcQ$c6/8LbkmJVBda3plgU34/0SQGDnKheYOcq6kddnnYco=',NULL,0,'Hoang','','','hoang@gmail.com',0,1,'2025-05-25 08:31:50.528168'),(10,'pbkdf2_sha256$1000000$mgXHW4KzY2xdUpRFuzBKvc$g+1JIKomc7cZs81W5KvMy/XFO+nHG7EvsYg1Yu1+Ihg=',NULL,0,'Nhut','','','nhut@gmail.com',0,1,'2025-05-25 08:32:11.879442'),(11,'pbkdf2_sha256$1000000$LxhgLYKha60MfjNZagDjb1$Fetw48fijW4AQSkKCSKdYlQOGnxpkSaA37xsrjP7xds=',NULL,0,'nguyenhalong','','','nguyenhalong102@gmail.com',0,1,'2025-05-29 03:01:40.979023');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:36
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(9,'app','audio'),(13,'app','challenge'),(14,'app','challengeexercise'),(7,'app','genre'),(11,'app','level'),(10,'app','speakingresult'),(8,'app','speakingtext'),(12,'app','useraudio'),(15,'app','userchallengeprogress'),(16,'app','userexerciseattempt'),(17,'app','userloginstreak'),(18,'app','userweeklyscore'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-25 18:47:48.157356'),(2,'auth','0001_initial','2025-05-25 18:47:48.966794'),(3,'admin','0001_initial','2025-05-25 18:47:49.130313'),(4,'admin','0002_logentry_remove_auto_add','2025-05-25 18:47:49.137303'),(5,'admin','0003_logentry_add_action_flag_choices','2025-05-25 18:47:49.145303'),(6,'contenttypes','0002_remove_content_type_name','2025-05-25 18:47:49.246042'),(7,'auth','0002_alter_permission_name_max_length','2025-05-25 18:47:49.354910'),(8,'auth','0003_alter_user_email_max_length','2025-05-25 18:47:49.377061'),(9,'auth','0004_alter_user_username_opts','2025-05-25 18:47:49.386060'),(10,'auth','0005_alter_user_last_login_null','2025-05-25 18:47:49.468494'),(11,'auth','0006_require_contenttypes_0002','2025-05-25 18:47:49.471493'),(12,'auth','0007_alter_validators_add_error_messages','2025-05-25 18:47:49.479869'),(13,'auth','0008_alter_user_username_max_length','2025-05-25 18:47:49.562595'),(14,'auth','0009_alter_user_last_name_max_length','2025-05-25 18:47:49.641539'),(15,'auth','0010_alter_group_name_max_length','2025-05-25 18:47:49.662884'),(16,'auth','0011_update_proxy_permissions','2025-05-25 18:47:49.671867'),(17,'auth','0012_alter_user_first_name_max_length','2025-05-25 18:47:49.759486'),(18,'app','0001_initial','2025-05-25 18:47:50.403912'),(19,'app','0002_readingmaterial_file_readingmaterial_user_and_more','2025-05-25 18:47:50.673641'),(20,'app','0003_remove_readingmaterial_file_and_more','2025-05-25 18:47:50.807086'),(21,'app','0004_genre_remove_readingmaterial_user_and_more','2025-05-25 18:47:51.401974'),(22,'app','0005_alter_speakingtext_content','2025-05-25 18:47:51.530471'),(23,'app','0006_remove_speakingtext_created_at','2025-05-25 18:47:51.569603'),(24,'app','0007_remove_audio_upload_time','2025-05-25 18:47:51.602358'),(25,'app','0008_alter_audio_audio_file','2025-05-25 18:47:51.711203'),(26,'app','0009_speakingresult','2025-05-25 18:47:51.822224'),(27,'app','0010_level','2025-05-25 18:47:51.860111'),(28,'app','0011_speakingtext_level','2025-05-25 18:47:51.964614'),(29,'app','0012_useraudio','2025-05-25 18:47:52.100518'),(30,'app','0013_alter_useraudio_user','2025-05-25 18:47:52.328971'),(31,'app','0014_alter_useraudio_user','2025-05-25 18:47:52.501694'),(32,'app','0015_challenge_challengeexercise_userchallengeprogress_and_more','2025-05-25 18:47:53.116373'),(33,'app','0016_userloginstreak_userweeklyscore','2025-05-25 18:47:53.387710'),(34,'sessions','0001_initial','2025-05-25 18:47:53.438450');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:35
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: speaking_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 14:50:34
