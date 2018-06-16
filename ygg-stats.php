<?php
$host = "127.0.0.1";
$port = 9001;

set_time_limit(2);

$getPeers = '{"request": "getPeers","keepalive":true}';
$getSessions = '{"request": "getSessions","keepalive":true}';
$getSelf = '{"request":"getSelf"}';

// open socket
$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
$result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");

// getPeers request
socket_write($socket, $getPeers, strlen($getPeers)) or die("Could not send data to server\n");
$gpeers = socket_read ($socket, 1024) or die("Could not read server response\n");
// getSessions
socket_write($socket, $getSessions, strlen($getSessions)) or die("Could not send data to server\n");
$gsessions = socket_read ($socket, 1024) or die("Could not read server response\n");
// getSelf
socket_write($socket, $getSelf, strlen($getSelf)) or die("Could not send data to server\n");
$gself = socket_read ($socket, 1024) or die("Could not read server response\n");
// make sure connection is closed
socket_close($socket);

// convert to arrays
$getSelf_json_array = json_decode($gself, true);
$getSessions_json_array = json_decode($gsessions, true);
$getPeers_json_array = json_decode($gpeers, true);

// convert bytes to something human readable
function humanFileSize($size,$unit="") {
  if( (!$unit && $size >= 1<<30) || $unit == "GB")
    return number_format($size/(1<<30),2)."GB";
  if( (!$unit && $size >= 1<<20) || $unit == "MB")
    return number_format($size/(1<<20),2)."MB";
  if( (!$unit && $size >= 1<<10) || $unit == "KB")
    return number_format($size/(1<<10),2)."KB";
  return number_format($size)." bytes";
}
// convert seconds to human readable time
function secondsToTime($seconds) {
    $dtF = new \DateTime('@0');
    $dtT = new \DateTime("@$seconds");
    return $dtF->diff($dtT)->format('%a days, %h:%i.%s');
}
?>
<!-- body of starts here -->
<!DOCTYPE html>
<html>
<head>
<title><?php echo key($getSelf_json_array{"response"}{"self"}); ?></title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
<div id="header">
	<div id="title"><?php echo key($getSelf_json_array{"response"}{"self"}); ?></div>
</div>
<div id="wrapper">
<h3>Connected Peers</h3>
<?php
// getPeers display and oragnise data pretty here
foreach ($getPeers_json_array{"response"}{"peers"} as $key => $value) {
	if ($value{"port"}) {
		echo '<div class="peer">' . $key . '</div>';
		echo '<div class="data"><div class="col1">' . secondsToTime((int)$value{"uptime"}) . '</div>';
		echo '<div class="col2">Rx: ' . humanFileSize($value{"bytes_recvd"}) . '</div>';
		echo '<div class="col2">Tx: ' . humanFileSize($value{"bytes_sent"}). '</div>';
		echo '<div class="col2">Port: ' . $value{"port"} . '</div>';
		echo '<div class="clear"></div></div>';
	}
}
echo '<h3>Current Sessions</h3>';
// getSessions display and oragnise data pretty here
foreach ($getSessions_json_array{"response"}{"sessions"} as $key => $value) {
	echo '<div class="peer">' . $key . '</div>';
	echo '<div class="data">';
	echo '<div class="col2">Rx: ' . humanFileSize($value{"bytes_recvd"}) . '</div>';
	echo '<div class="col2">Tx: ' . humanFileSize($value{"bytes_sent"}) . '</div>';
	echo '<div class="col2">Coords: ' . $value{"coords"} . '</div>';
	echo '<div class="clear"></div></div>';
}
?>
<div class="updated">Last updated: <?php echo date("Y-m-d H:i:s"); ?> </div>
<br />
<a href="https://github.com/yakamok/yggdrasil-stats">ygg-stats</a>
</div>
</body>
</html>
