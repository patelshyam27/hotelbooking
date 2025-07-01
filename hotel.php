<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
$hotel = $_POST['hotel'] ?? 'Unknown Hotel';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hotel Details</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar-right">
    <a href="profile.php"><img src="images/user.png" class="icon"> Profile</a>
    <a href="logout.php"><img src="images/logout.png" class="icon"> Logout</a>
</div>
<h1><?php echo $hotel; ?> - Hotel Details</h1>
<h2>Available Rooms</h2>
<form action="book.php" method="POST" class="room-list">
    <input type="hidden" name="hotel" value="<?php echo $hotel; ?>">
    <div class="room-option">
        <span>Deluxe Room - ₹100</span>
        <button type="submit" name="room" value="Deluxe">Book</button>
    </div>
    <div class="room-option">
        <span>Suite - ₹200</span>
        <button type="submit" name="room" value="Suite">Book</button>
    </div>
</form>
<h2>Restaurant Menu</h2>
<div class="restaurant-menu">
    <div class="menu-item">Pasta - ₹10</div>
    <div class="menu-item">Pizza - ₹12</div>
    <div class="menu-item">Burger - ₹8</div>
</div>
</body>
</html>
