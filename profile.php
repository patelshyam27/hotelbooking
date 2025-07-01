<?php
session_start();
include "db_connect.php";

if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}

$user_id = $_SESSION['user']['id'];
$name = $_SESSION['user']['name'];

$result = mysqli_query($conn, "SELECT * FROM bookings WHERE user_id = $user_id ORDER BY id DESC");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Bookings</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar-right">
    <a href="index.php"><img src="images/home.png" class="icon"> Home</a>
    <a href="logout.php"><img src="images/logout.png" class="icon"> Logout</a>
</div>
<h1><?php echo $name; ?>'s Bookings</h1>
<?php if (mysqli_num_rows($result) > 0): ?>
    <div class="booking-list">
        <?php while ($row = mysqli_fetch_assoc($result)): ?>
            <div class="booking-card">
                <p><strong>Hotel:</strong> <?php echo $row['hotel_name']; ?></p>
                <p><strong>Room:</strong> <?php echo $row['room_type']; ?></p>
                <p><strong>Check-in:</strong> <?php echo $row['checkin_date']; ?></p>
                <p><strong>Check-out:</strong> <?php echo $row['checkout_date']; ?></p>
            </div>
        <?php endwhile; ?>
    </div>
<?php else: ?>
    <p style="text-align:center;">You have no bookings yet.</p>
<?php endif; ?>
</body>
</html>
