SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `compx222-assignment3-2024`
--
CREATE DATABASE IF NOT EXISTS `compx222-assignment3-2024` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `compx222-assignment3-2024`;

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contact`;
CREATE TABLE `contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) NULL,
  `email` varchar(255) NULL,
  `address` varchar(255) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contact` (`name`, `phone`,`email`, `address`) 
VALUES ('Mario', '12345678910', 'mario@nintendo.com', '120 Mushroom Alley, Toad Town, Mushroom Kingdom, MSH4 K12');