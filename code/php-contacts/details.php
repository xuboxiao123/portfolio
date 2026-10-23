<?php
// Database Connection
$conn = mysqli_connect(getenv("DB_HOST") ?: "localhost", getenv("DB_USER") ?: "root", getenv("DB_PASSWORD") ?: "", getenv("DB_NAME") ?: "compx222-assignment3-2024");
if (!$conn) {
    die('Connection failed: ' . mysqli_connect_error());
}

// Initialize $contact variable
$contact = null;

// Check if there is a passed contact ID
if (isset($_GET['contact'])) {
    $contact_id = $_GET['contact'];

    // Obtain contact information, including address
    $query = "SELECT id, name, email, phone, address FROM contact WHERE id = ?";
    $stmt = mysqli_prepare($conn, $query);
    mysqli_stmt_bind_param($stmt, 'i', $contact_id);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    // Check if there are any results
    if (mysqli_num_rows($result) > 0) {
        $contact = mysqli_fetch_assoc($result);
        
        // Set cookies related to contacts
        $cookie_key = 'contact_' . $contact['id'];
        setcookie($cookie_key . '[name]', $contact['name'], time() + 3600, '/');
        setcookie($cookie_key . '[email]', $contact['email'], time() + 3600, '/');
        setcookie($cookie_key . '[phone]', $contact['phone'], time() + 3600, '/');
        setcookie($cookie_key . '[address]', $contact['address'], time() + 3600, '/');
    }
    mysqli_stmt_close($stmt);
}

// Process contact deletion request
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['delete_contact'])) {
    $contact_id = $_POST['contact_id'];

    $delete_query = "DELETE FROM contact WHERE id = ?";
    $delete_stmt = mysqli_prepare($conn, $delete_query);
    mysqli_stmt_bind_param($delete_stmt, 'i', $contact_id);

    if (mysqli_stmt_execute($delete_stmt)) {
        // After successful deletion, redirection or other operations can be performed
        header("Location: index.php");
        exit;
    } else {
        echo "Error: Failed to delete contact.";
    }
}

mysqli_close($conn);
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Details</title>
    <link rel="stylesheet" href="css/styledetails.css">
</head>
<body>

<main>
    <div class="header">
        <a href="index.php"><div id="w1">Contacts</div></a>
        <a href="add.php"><div id="add">Add</div></a>
    </div>
    
    <div class="bigBox">
        <?php
        if ($contact) {
    
            echo '<div class="details">';
             echo '<div class="name">';
              echo '<h2>' . htmlspecialchars($contact['name']) . '</h2><br>';
             echo '</div>';
             echo 'Email: ' .  '<br>'. htmlspecialchars($contact['email']) . '<br>';
             echo 'Phone: ' .  '<br>'. htmlspecialchars($contact['phone']) . '<br>';
             echo 'Address: ' .  '<br>'. htmlspecialchars($contact['address']);
             echo '</div>';
        } else {
            echo 'none';
        }
        
        ?>
        <form method="post">
                <input type="hidden" name="contact_id" value="<?php echo $contact['id']; ?>">
                <button type="submit" name="delete_contact">Delete</button>
                 
            </form>
          
              <a href="update.php?contact_id=<?= $contact['id'] ?>"><button>Update</button></a>
                
                

                
               
                    </a>
                </li>
       
             
      


    </div>
</main>

</body>
</html>
