<?php
$conn = mysqli_connect(getenv("DB_HOST") ?: "localhost", getenv("DB_USER") ?: "root", getenv("DB_PASSWORD") ?: "", getenv("DB_NAME") ?: "compx222-assignment3-2024");

if (!$conn) {
    die('Connection failed: ' . mysqli_connect_error());
}

$query = "SELECT id, name, email, phone FROM contact ORDER BY name";
$result = mysqli_query($conn, $query);

if (!$result) {
    die('Query failed: ' . mysqli_error($conn));
}

mysqli_close($conn);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact List</title>
    <link rel="stylesheet" href="css/styleindex.css">
</head>
<body>

<main>
    <div class="header">
        <div id="w1">Contacts</div>
        <a href="add.php"><div id="add">Add</div></a>
    </div>
    
    <div class="bigBox">
        <ul class="contact-list">
            <?php while ($row = mysqli_fetch_assoc($result)): ?>
                <?php
                // Generate a unique identifier as the key for the cookie, using the contact's ID here
                $cookie_key = 'contact_' . $row['id'];
                // Set a cookie that includes information such as name, email, phone number, etc
                setcookie($cookie_key . '[name]', $row['name'], time() + 3600, '/');
                ?>
                <li class="contact-item">
                    <a href="details.php?contact=<?= $row['id']; ?>">
                        <div class="name"><?= $row['name']; ?></div>
                        <div>Email: <?= $row['email']; ?></div>
                        <div>Phone: <?= $row['phone']; ?></div>
               
                    </a>
                </li>
            <?php endwhile; ?>
        </ul>
    </div>
</main>

</body>
</html>

