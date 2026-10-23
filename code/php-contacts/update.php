<?php
$conn = mysqli_connect(getenv("DB_HOST") ?: "localhost", getenv("DB_USER") ?: "root", getenv("DB_PASSWORD") ?: "", getenv("DB_NAME") ?: "compx222-assignment3-2024");
if (!$conn) {
    die('Connection failed: ' . mysqli_connect_error());
}

$contact_id = null; 

if (isset($_GET['contact_id'])) {
    $contact_id = $_GET['contact_id'];

    $query = "SELECT id, name, email, phone, address FROM contact WHERE id = ?";
    $stmt = mysqli_prepare($conn, $query);
    mysqli_stmt_bind_param($stmt, 'i', $contact_id);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    if ($row = mysqli_fetch_assoc($result)) {
        $name = $row['name'];
        $email = $row['email'];
        $phone = $row['phone'];
        $address = $row['address'];
    } else {
        $name = 'Unknown';
        $email = 'No email provided';
        $phone = 'No phone provided';
        $address = 'No address provided';
    }
    mysqli_stmt_close($stmt);
} else {
    $name = 'Unknown';
    $email = 'No email provided';
    $phone = 'No phone provided';
    $address = 'No address provided';
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = isset($_POST['Name']) ? $_POST['Name'] : $name;
    $phone = isset($_POST['Phone']) ? $_POST['Phone'] : $phone;
    $email = isset($_POST['Mail']) ? $_POST['Mail'] : $email;
    $address = isset($_POST['Address']) ? $_POST['Address'] : $address;

    $sql = "UPDATE contact SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?";
    $stmt = mysqli_prepare($conn, $sql);
    if ($stmt === false) {
        die('MySQL prepare error: ' . mysqli_error($conn));
    }

    mysqli_stmt_bind_param($stmt, "ssssi", $name, $email, $phone, $address, $contact_id);
    mysqli_stmt_execute($stmt);

    if (mysqli_stmt_affected_rows($stmt) > 0) {
        // to detail.php
        header("Location: index.php?contact_id=$contact_id");
        exit;
    } else {
        // error
        echo '<div style="text-align: center; margin-top: 80px;color : red;width : 100px;heigh : 40px;background-color :white">';
        echo "<p>No changes made or error updating record: " . mysqli_stmt_error($stmt) . "</p>";
        echo '</div>';
    }

    mysqli_stmt_close($stmt);
}
mysqli_close($conn);
?>




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Contact</title>
    <link rel="stylesheet" href="css/styleupdate.css">
</head>
<body>

<main>
    <div class="header">
        <a href="index.php"><div id="w1">Contacts</div></a>
        <a href="add.php"><div id="add">Add</div></a>
    </div>
    
    <div class="box1">
        <div class="t1"><h2>Update Contact</h2></div>
        <div class="contain">
            <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>?contact_id=<?php echo htmlspecialchars($contact_id); ?>">

                <div><label for="Name">Name:</label></div>
                <input type="text" id="Name" name="Name" value="<?php echo htmlspecialchars($name); ?>">
                
                <div><label for="Phone">Phone:</label></div>
                <input type="text" id="Phone" name="Phone" value="<?php echo htmlspecialchars($phone); ?>">
                
                <div><label for="Mail">Mail:</label></div>
                <input type="text" id="Mail" name="Mail" value="<?php echo htmlspecialchars($email); ?>">
                
                <div><label for="Address">Address:</label></div>
                <input type="text" id="Address" name="Address" value="<?php echo htmlspecialchars($address); ?>">
                
                <button type="submit"id="APP2">Update</button>
            </form>
        </div>
    </div>
</main>

<div class="footer"> 
    <!-- Placeholder for footer content -->
</div>

</body>
</html>
