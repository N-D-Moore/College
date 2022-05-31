<?php
require_once "connection.php";


// get the q parameter from URL
$q = $_REQUEST["q"];

$tables = array(
	2 => 10,
	4 => 5,
	6 => 4
);

$db = new MyDB();
if (!$db) {
	echo $db -> lastErrorMsg();
}

for ($i = 1; $i <= 3; $i++) {
	$statement = $db->prepare("SELECT tables as taken FROM reservations WHERE date LIKE :date and tables LIKE :tables");
	$temp = '%' . $q . '%';
	$tempNum = $i*2;
	$tempNumStr = '%' . $tempNum . '%';
	$statement->bindValue(':date', $temp);
	$statement->bindValue(':tables', $tempNumStr);
	$result = $statement->execute();
	
	$numOfTakenTables = 0;
	
	while($row = $result->fetchArray()) { 
		if (strlen($row['taken']) > 1) {
			$split = explode("+", $row['taken']);
			for ($j = 0; $j < count($split); $j++) {
				if ($split[$j] == $tempNum) {
					$numOfTakenTables += 1;
				}
			}
		} else {
			if ($row['taken'] == $tempNum) {
				$numOfTakenTables += 1;
			}
		}
	}
	$tables[$tempNum] -= $numOfTakenTables;
	//echo $numOfTakenTables;
}

$db->close();

$currentCapacity = 0;

for ($i = 1; $i <= 3; $i++) {
	$tempNum = $i*2;
	//echo $tables[$tempNum];
	//echo " ";
	$currentCapacity += ($tempNum * $tables[$tempNum]);
}

echo $currentCapacity;
//2021-12-03
//echo getReservationSeatsStr(16, "2021-12-03");

/*
*/

// Output "no suggestion" if no hint was found or output correct values
//echo $hint === "" ? "no suggestion" : $hint;
//echo $strSeats;
?>

