<?php
$action=$_POST["action"];
$cmd=$_POST["cmd"];
if($action=="set-connection"){ 
	$myfile=fopen("connect.txt","w") or die("unable to open file!");
    fwrite($myfile,$cmd); 
    fclose($myfile);
    $str=file_get_contents("connect.txt");
	echo($str);	
}
?>