<?php 
    // this is the code that establishes a connection to the database
    // you do not need to modify any of this code
    // you should incldue this file all your .php files using: include('config/db_connect.php');

    // might log to XAMPP > xamppfiles > logs folder
    ini_set("error_reporting", E_ALL);
    ini_set("log_errors", "1");
    ini_set("error_log", "php_errors.txt");

    // connect to the database
    $conn = mysqli_connect(getenv("DB_HOST") ?: "localhost", getenv("DB_USER") ?: "root", getenv("DB_PASSWORD") ?: "", getenv("DB_NAME") ?: "compx222-assignment3-2024");  // 这个地方数据库密码是空  你设置上密码肯定不行的

    // check connection
    if(!$conn){
        die('Connection error: '. mysqli_connect_error());
    }

?>
