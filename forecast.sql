-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               5.7.24 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for forecast
CREATE DATABASE IF NOT EXISTS `sql6632871` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `sql6632871`;

-- Dumping structure for table forecast.user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `password` varchar(255) NOT NULL,
  `type` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

-- Dumping data for table forecast.user: ~12 rows (approximately)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `username`, `password`, `type`) VALUES
	(2, 'itachi', 'asas', 7),
	(3, 'cobaaja', 'pbkdf2:sha256:260000$RPic3FU8qTixv50M$5ef80f3d6a4346ec321491c99008e566de76b32a3b753852797847b661fce46b', 0),
	(4, 'wedusgembel', 'pbkdf2:sha256:260000$ISU9oQpDWDO0KX00$eead72339a1af7352246fbf252e1bb34662482f7a8b084555c9f24474fa8604c', 0),
	(5, 'xixixi', 'pbkdf2:sha256:260000$dtQpWGSkVq6CAyhr$a30b73cb766565299f0ce419db58cabcf1ca8c5cf23842f3e37ec7e81c2a5ac1', 0),
	(6, 'jajal', 'pbkdf2:sha256:260000$AnYgSmR3NXoFNtcN$ec9adb531d598ca759bbfc4cc685670fc898033667ddbabfb2aee7068ae2c327', 0),
	(7, 'sasuke', 'pbkdf2:sha256:260000$5pcVgXc3ggTYi1uk$98462727eeac803dcda124c253cbfe2e157adc050315cf9b3512723a2457b1ff', 0),
	(8, 'naruto', 'pbkdf2:sha256:260000$AtE0mPkI13i7nars$63da788f9445a49669333cd5628dfcf9b73eddf72bcaa882b6bbdbde8c602dc9', 7),
	(9, 'waduh', 'pbkdf2:sha256:260000$zOeeBJaQN88HDa4j$2dbc7882024794f154b0a79df0fa0314f77e622c147c55091165608bd6cbd5dc', 0),
	(10, 'waduh1', 'pbkdf2:sha256:260000$Vz8zs8DwYz8g6otT$af39314c8b0f3d192860a5b79014e0ac2712b07a2a242df871c0a679252cad54', 0),
	(11, 'waduh2', 'pbkdf2:sha256:260000$l8njXUOFbnyo3aGZ$c22f1b171f13e9eb052f843cc8c05a7d1ce129bc92526d024f8231233b884b67', 0),
	(12, 'dummy', 'pbkdf2:sha256:260000$iajA1sTeNQNvTstC$a47fa8ceb39d6de9dce976da9feeb2029695068ebe9f33aa6c1c01bfccb56368', 0),
	(13, 'dummyuser', 'pbkdf2:sha256:260000$g1ODYLjemGF1IxRA$3f84152bcc9e81cd2f29137f92591ad118bf317e46a11bc8160afe69f3a5a903', 0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
