/*
SQLyog Ultimate v11.11 (32 bit)
MySQL - 5.5.5-10.4.28-MariaDB : Database - dbusers
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`dbusers` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `dbusers`;

/*Table structure for table `usuarios` */

DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(30) NOT NULL,
  `APELLIDO` varchar(30) NOT NULL,
  `CORREO` varchar(100) NOT NULL,
  `NOMBRE_USUARIO` varchar(60) NOT NULL,
  `CLAVE_USUARIO` varchar(50) NOT NULL,
  `ROL` varchar(30) NOT NULL DEFAULT 'general',
  `Estado` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `usuarios` */

insert  into `usuarios`(`ID`,`NOMBRE`,`APELLIDO`,`CORREO`,`NOMBRE_USUARIO`,`CLAVE_USUARIO`,`ROL`,`Estado`) values (1,'Juan','Perez','juanperez@gmail.com','juanperez','nuevaclave','admin',1),(2,'Maria','Gomez','maria.gomez@gmail.com','mariag','clave456','general',1),(3,'Luis','Ramirez','luis.ramirez@hotmail.com','luisr','clave789','general',1),(4,'Ana','Martinez','ana.martinez@gmail.com','anam','clave1011','general',1),(5,'Carlos','Fernandez','carlos.fernandez@gmail.com','carlosf','clave1213','general',0),(6,'Andres','Andrade','andresA@gmail.com','andresa','ang','general',1),(7,'Samuel','Suarez','ssuarez@gmail.com','sasuaz','1234','general',1),(8,'Maria','Lopez','malo@gmail.com','malopez','1234','general',1),(9,'Sara','Manrique','smanrique@gmail.com','samanrique','1234','general',1),(10,'Jose','Cea','jcea@gmail.com','jcea','1234','general',1);

/* Procedure structure for procedure `SP_CREAR_USUARIO` */

/*!50003 DROP PROCEDURE IF EXISTS  `SP_CREAR_USUARIO` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_CREAR_USUARIO`(
    IN p_nombre VARCHAR(30),
    IN p_apellido VARCHAR(30),
    IN p_correo VARCHAR(100),
    IN p_nombre_usuario VARCHAR(60),
    IN p_clave_usuario VARCHAR(50)
)
BEGIN
    INSERT INTO usuarios (Nombre, Apellido, Correo, Nombre_Usuario, Clave_Usuario)
    VALUES (p_nombre, p_apellido, p_correo, p_nombre_usuario, p_clave_usuario);
END */$$
DELIMITER ;

/* Procedure structure for procedure `sp_editar_usuario` */

/*!50003 DROP PROCEDURE IF EXISTS  `sp_editar_usuario` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_editar_usuario`(
    IN p_id INT,               --  ID para identificar al usuario
    IN p_nombre VARCHAR(30),
    IN p_apellido VARCHAR(30),
    IN p_correo VARCHAR(100),
    IN p_nombre_usuario VARCHAR(60),
    IN p_clave_usuario VARCHAR(50)
)
BEGIN
    UPDATE usuarios
    SET 
        Nombre = p_nombre,
        Apellido = p_apellido,
        Correo = p_correo,
        Nombre_Usuario = p_nombre_usuario,
        Clave_Usuario = p_clave_usuario
    WHERE 
        Id = p_id;      
END */$$
DELIMITER ;

/* Procedure structure for procedure `SP_ObtenerEstadoUsuarioPorId` */

/*!50003 DROP PROCEDURE IF EXISTS  `SP_ObtenerEstadoUsuarioPorId` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_ObtenerEstadoUsuarioPorId`(IN p_id INT)
BEGIN
    SELECT Id, Nombre, Apellido,
           CASE
               WHEN estado = 1 THEN 'Activo'
               ELSE 'Inactivo'
           END AS Estado_Actual_Usuario
    FROM usuarios
    WHERE id = p_id;
END */$$
DELIMITER ;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
