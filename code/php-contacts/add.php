<?php
require_once('config/db_connect.php');


$name = $phone = $mail = $address = "";
$nameWarning = $phoneMailWarning = $addressWarning = "";


if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $name = $_POST['Name'];
    $phone = $_POST['Phone'];
    $email = $_POST['Mail'];
    $address = $_POST['Address'];


    if (empty($name)) {
        $nameWarning = 'style="display: block;"';
    }
    if (empty($phone) && empty($email)) {
        $phoneMailWarning = 'style="display: block;"';
    }
    if (empty($address)) {
        $addressWarning = 'style="display: block;"';
    }


    if (!empty($name) && (!empty($phone) || !empty($email)) && !empty($address)) {

        $sql = "INSERT INTO contact(name, phone, email, address) VALUES ('$name', '$phone', '$email', '$address')";
        
        if ($conn->query($sql) === TRUE) {
            echo "succesful";
            header("Location: index.php");
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    }
}
?>

<header>
    <!-- Link to external stylesheet -->
    <link rel="stylesheet" href="css/styleAdd.css"> 
</header>
<body>

<main>
    
    <!-- Placeholder for header content -->
    <div class="header">
        <!-- Section for displaying "Contacts" -->
        <a href="index.php"><div id="w1">Contacts</div></a>
        <!-- Link to add.php -->
        <a href="add.php"><div id="add">Add</div></a>
    </div>
    
    <!-- Main content box -->
    <div class="box1">
        <!-- Title section -->
        <div class="t1"><h2>Add Contact</h2></div>

        <!-- Form container -->
        <div class="contain">
            <!-- Name input field -->
            <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
                <div><label for="Name">Name:</label></div>
                <input type="text" id="Name" name="Name" value="<?php echo htmlspecialchars($name); ?>">
                <!-- Warning message for name -->
                <div class="word" id="warn1_name" <?php echo $nameWarning; ?>>
                    Name is required
                </div>
                
                <!-- Phone input field -->
                <div><label for="Phone">Phone:</label></div>
                <input type="text" id="Phone" name="Phone" value="<?php echo htmlspecialchars($phone); ?>">
                <!-- Warning message for phone or mail -->
                <div class="word" id="warn1_phone_mail" <?php echo $phoneMailWarning; ?>>
                    You must enter a phone number or an email
                </div>
                
                <!-- Mail input field -->
                <div><label for="Mail">Mail:</label></div>
                <input type="text" id="Mail" name="Mail" value="<?php echo htmlspecialchars($mail); ?>">
                <div class="word" id="warn1_phone_mail" <?php echo $phoneMailWarning; ?>>
                    You must enter a phone number or an email
                </div>
                <!-- Address input field -->
                <div><label for="Address">Address:</label></div>
                <input type="text" id="Address" name="Address" value="<?php echo htmlspecialchars($address); ?>">
                <!-- Warning message for address -->
                <div class="word" id="warn1_address" <?php echo $addressWarning; ?>>
                    You need to enter an address
                </div>
                <!-- Button to submit form -->
                <input type="submit" id="add2" value="Add">
            </form>
        </div>
    </div>
</main>

<!-- Footer section -->
<div class="footer"> 
    <!-- Placeholder for footer content -->
</div>

</body>
