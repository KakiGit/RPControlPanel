<?php
$myfile = fopen("ajax/pistats.txt", "r") or die("Unable to open file!");
$read = fread($myfile,filesize("ajax/pistats.txt"))
fclose($myfile);
echo "let data='$read'";
?>