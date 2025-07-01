<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hotel Selection</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
   

<div class="topbar-right">
    <?php if (isset($_SESSION['user'])): ?>
        <a href="profile.php"><img src="images/user.png" class="icon"> Profile</a>
        <a href="logout.php"><img src="images/logout.png" class="icon"> Logout</a>
    <?php else: ?>
        <a href="login.php"><img src="images/login.png" class="icon"> Login</a>
        <a href="register.php"><img src="images/add-user.png" class="icon"> Create Account</a>
    <?php endif; ?>
</div>

<h1>Select a Hotel</h1>
<form action="hotel.php" method="POST" class="hotel-list">
    <button type="submit" name="hotel" value="Taj Ahmedabad">Taj Ahmedabad</button>
    <button type="submit" name="hotel" value="Taj Surat">Taj Surat</button>
    <button type="submit" name="hotel" value="Taj Vadodara">Taj Vadodara</button>
</form>
</body>
</html>
