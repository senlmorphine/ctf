<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if (isset($_FILES["key"])) {
    if ($_FILES["key"]["size"] !== 8) {
      echo "Sorry, your key is the wrong size!";
      return;
    }

    $flag = file_get_contents("/flag.txt");
    $password = file_get_contents("/password.txt");

    $unknown_bytes = read_file_to_bytes("cipher");
    $key_bytes = read_file_to_bytes($_FILES["key"]["tmp_name"]);
    
    $to_check = ($unknown_bytes + hexdec("d34db33f")) ^ $key_bytes;
    
    if ($to_check == $password) {
      echo $flag;
    } else {
      echo "Sorry, your key is incorrect!";
    }
  }
} else {
  echo show_source('decrypt.php', True);
}

function read_file_to_bytes($filename) {
  $file = fopen($filename, "rb");
  $content = fread($file, filesize($filename));
  $bytes = unpack("J", $content);

  return $bytes[1];
}

?>