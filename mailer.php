<?php
$email_to = "cj@silencekillsdesign.com";
$name = $_POST["name"];
$company = $_POST["company"];
$email = $_POST["email"];
$message = $_POST["message"];
$text = "NAME: $name<br>
									COMPANY: $company<br>
									EMAIL: $email<br>
									MESSAGE: $message";
$headers = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type:text/html; charset=utf-8" . "\r\n";
$headers .= "From: <$email>" . "\r\n";
mail($email_to, "Message", $text, $headers);
?>
