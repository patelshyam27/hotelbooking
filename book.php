<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
$hotel = $_POST['hotel'] ?? '';
$room = $_POST['room'] ?? '';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Book a Room</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar-right">
    <a href="profile.php"><img src="images/user.png" class="icon"> Profile</a>
    <a href="logout.php"><img src="images/logout.png" class="icon"> Logout</a>
</div>
<h1>Booking for <?php echo $room; ?> at <?php echo $hotel; ?></h1>
<form action="confirm.php" method="POST" class="booking-form">
    <input type="hidden" name="hotel" value="<?php echo $hotel; ?>">
    <input type="hidden" name="room" value="<?php echo $room; ?>">
    <label>Name:</label>
    <input type="text" name="name" required>
    <label>Email:</label>
    <input type="email" name="email" required>
    <label>Check-in Date:</label>
    <input type="date" name="checkin" required>
    <label>Check-out Date:</label>
    <input type="date" name="checkout" required>
    <button type="submit">Confirm Booking</button>
</form>
<a href="index.php" class="btn">← Back to Home</a>
</body>
</html>
