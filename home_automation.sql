-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2018 at 11:49 AM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `home_automation`
--

-- --------------------------------------------------------

--
-- Table structure for table `controller`
--

CREATE TABLE `controller` (
  `CONTROLLER_NO` int(10) NOT NULL,
  `CONTROLLER_USER_ID` varchar(50) NOT NULL,
  `CONTROLLER_NUMBER` int(3) NOT NULL,
  `CONTROLLER_NAME` varchar(35) NOT NULL,
  `CONTROLLER_CREATE_TS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CONTROLLER_UPDATE_TS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `controller`
--

INSERT INTO `controller` (`CONTROLLER_USER_ID`, `CONTROLLER_NUMBER`, `CONTROLLER_NAME`, `CONTROLLER_SSID`, `CONTROLLER_PASSWORD`, `CONTROLLER_CREATE_TS`, `CONTROLLER_UPDATE_TS`) VALUES
('rk3@gmail.com', 1, 'machine1', '123', 'sha256$aD1u8Yj9$29a48cd935eb45fb', '2018-02-23 16:04:33', '2018-02-23 16:04:33');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `USER_NO` int(11) NOT NULL,
  `USER_EMAIL_ID` varchar(50) NOT NULL,
  `USER_PASSWORD` varchar(80) NOT NULL,
  `USER_MOBILE` int(12) NOT NULL,
  `USER_NAME` varchar(30) NOT NULL,
  `USER_COMPANY_NAME` varchar(30) NOT NULL,
  `USER_COMPANY_ADDRESS` varchar(50) NOT NULL,
  `USER_ACTIVE` int(1) NOT NULL,
  `USER_CREATE_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `USER_UPDATE_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`USER_NO`, `USER_EMAIL_ID`, `USER_PASSWORD`, `USER_MOBILE`, `USER_NAME`, `USER_COMPANY_NAME`, `USER_COMPANY_ADDRESS`, `USER_ACTIVE`, `USER_CREATE_TS`, `USER_UPDATE_TS`) VALUES
(8, 'rk3@gmail.com', 'sha256$Bal3Ek6z$fff657c829758e07cdb90feb7fb82854d31d64aa7e566182600d4873d5965c7f', 8300, 'Naveen', 'abcd', 'tf', 0, '2018-02-15 05:18:07', '2018-02-15 05:18:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `controller`
--
ALTER TABLE `controller`
  ADD KEY `CONFKUSE_idx` (`CONTROLLER_USER_ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`USER_NO`),
  ADD UNIQUE KEY `USER_EMAIL_ID_UNIQUE` (`USER_EMAIL_ID`);


--
-- Constraints for dumped tables
--

--
-- Constraints for table `controller`
--
ALTER TABLE `controller`
  ADD CONSTRAINT `CONFKUSE` FOREIGN KEY (`CONTROLLER_USER_ID`) REFERENCES `user` (`USER_NO`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
