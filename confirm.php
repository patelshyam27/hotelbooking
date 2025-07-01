<?php
session_start();
include "db_connect.php";

if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user_id = $_SESSION['user']['id'];
    $hotel = $_POST['hotel'];
    $room = $_POST['room'];
    $name = $_POST['name'];
    $email = $_POST['email'];
    $checkin = $_POST['checkin'];
    $checkout = $_POST['checkout'];

    $sql = "INSERT INTO bookings (hotel_name, room_type, customer_name, email, checkin_date, checkout_date, user_id)
            VALUES ('$hotel', '$room', '$name', '$email', '$checkin', '$checkout', '$user_id')";

    $inserted = mysqli_query($conn, $sql);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Booking Confirmed</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar-right">
    <a href="profile.php"><img src="images/user.png" class="icon"> Profile</a>
    <a href="logout.php"><img src="images/logout.png" class="icon"> Logout</a>
</div>
<?php if (isset($inserted) && $inserted): ?>
    <div class="confirmation-card">
        <h1>✅ Booking Confirmed!</h1>
        <p><strong>Hotel:</strong> <?php echo $hotel; ?></p>
        <p><strong>Room:</strong> <?php echo $room; ?></p>
        <p><strong>Name:</strong> <?php echo $name; ?></p>
        <p><strong>Email:</strong> <?php echo $email; ?></p>
        <p><strong>Check-in:</strong> <?php echo $checkin; ?></p>
        <p><strong>Check-out:</strong> <?php echo $checkout; ?></p>
        <a href="index.php" class="btn">Back to Home</a>
    </div>
<?php else: ?>
    <p style="color: red; text-align: center;">❌ Error saving booking. Please try again.</p>
<?php endif; ?>
</body>
</html>
