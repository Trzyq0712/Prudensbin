<?php
$name=$_GET["fname"]
$mail=$_GET["email"]
$message1=$_GET["mess"]
$to = "support@prudensbin.live";
$subject = "Checking PHP mail" . $mail;
$message = "PHP mail works just fine" . $message1;
$headers = "From:" . $mail;
mail($to,$subject,$message, $headers);
echo "The email message was sent.";
?>
