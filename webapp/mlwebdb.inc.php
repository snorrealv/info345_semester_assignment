<?php
// 	mlwebdb.inc.php: db settings for MouselabWEB 
//
//       v 2.00, Nov 2017
//		
//     (c) 2003-2017 Martijn C. Willemsen and Eric J. Johnson 
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program; if not, write to the Free Software
//    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

// $DBhost = "mysql"; 		// hostname of the mySQL database 
// $DBuser = "myuser"; 		// username of user on this database
// $DBpass = "secret";		// user password
// $DBname = "mydb";			// name of the database
// $table = "mlweb";			// name of the table containing MLWEB Data (can be left to mlweb)
// $table_exps = 'exps';

$DBhost = $_ENV["DB_HOST"];   // hostname of the mySQL database 
$DBuser = $_ENV["DB_USER"];
$DBpass = $_ENV["DB_PASSWORD"];  // user password
$DBname = $_ENV["DB_NAME"];     // name of the database
$DBport = $_ENV["DB_PORT"]; 
$table = "mlweb";			    // name of the table containing MLWEB Data (can be left to mlweb)
$table_exps = 'exps';


// $link = mysqli_connect('p:'.host = $DBhost, username = $DBuser, password = $DBpass, dbname = $DBname, port = $DBport);
$link = mysqli_connect($DBhost, $DBuser, $DBpass, $DBname, $DBport);
if (!$link) {
    echo "".'p:'.$DBhost. ' '. $DBuser, $DBpass, $DBname;
    echo "Error: Unable to connect to MySQL." . PHP_EOL;
    echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    exit;
}
?>