<?php
require_once "connection.php";

//resetDb();

$db = new MyDB();
if (!$db) {
	echo $db -> lastErrorMsg();
}

$statement = $db->prepare("SELECT * FROM users");
$result = $statement->execute();

echo("USER TABLE: \n");
echo('<p>');
echo '<style>';
echo 'table, th, td {';
echo '  border: 1px solid black;';
echo '  border-collapse: collapse;}';
echo '</style>';
echo '<table>';
echo '<tr>';
echo '  <th>preferred_diner_id </th>';
echo '  <th>name </th>';
echo '  <th>mailing_address </th>';
echo '  <th>billing_address </th>';
echo '  <th>points </th>';
echo '  <th>payment_method </th>';
echo '  <th>email </th>';
echo '  <th>username </th>';
echo '  <th>password </th>';
echo '</tr>';  
while($row = $result->fetchArray()) {   	// for reservation
	echo '<tr><td>' . $row['preferred_diner_id'] . '</td><td>' . $row['name'] . '</td>' . '<td>' . $row['mailing_address'] . '</td><td>' . $row['billing_address'] . '</td>' . '<td>' . $row['points'] . '</td><td>' . $row['payment_method'] . '</td>' . '<td>' . $row['email'] . '</td><td>' . $row['username'] . '</td>' . '<td>' . $row['password'] . '</td>';
}
echo '</table>';
echo('</p>');
 
$statement = $db->prepare("SELECT * FROM reservations");
$result = $statement->execute();

echo("RESERVATIONS TABLE: \n");
echo('<p>');
echo '<style>';
echo 'table, th, td {';
echo '  border: 1px solid black;';
echo '  border-collapse: collapse;}';
echo '</style>';
echo '<table>';
echo '<tr>';
echo '  <th>reservation_id </th>';
echo '  <th>preferred_diner_id </th>';
echo '  <th>date </th>';
echo '  <th>time </th>';
echo '  <th>name </th>';
echo '  <th>phone_num </th>';
echo '  <th>email </th>';
echo '  <th>num_of_guests </th>';
echo '  <th>tables </th>';
echo '  <th>payment_method </th>';
echo '</tr>';  
while($row = $result->fetchArray()) {   	// for reservation
	echo '<tr><td>' . $row['reservation_id'] . '</td><td>' . $row['preferred_diner_id'] . '</td><td>' . $row['date'] . '</td>' . '<td>' . $row['time'] . '</td><td>' . $row['name'] . '</td>' . '<td>' . $row['phone_num'] . '</td><td>' . $row['email'] . '</td>' . '<td>' . $row['num_of_guests'] . '</td><td>' . $row['tables'] . '</td>' . '<td>' . $row['payment_method'] . '</td>';
}
echo '</table>';
echo('</p>');

$statement = $db->prepare("SELECT * FROM tables");
$result = $statement->execute();

echo("TABLES TABLE: \n");
echo('<p>');
echo '<style>';
echo 'table, th, td {';
echo '  border: 1px solid black;';
echo '  border-collapse: collapse;}';
echo '</style>';
echo '<table>';
echo '<tr>';
echo '  <th>table_id </th>';
echo '  <th>num_of_seats </th>';
echo '</tr>';  
while($row = $result->fetchArray()) {   	// for reservation
	echo '<tr><td>' . $row['table_id'] . '</td><td>' . $row['num_of_seats'] . '</td></tr>';
}
echo '</table>';
echo('</p>');

$statement = $db->prepare("SELECT * FROM high_traffic_days");
$result = $statement->execute();

echo('<p>');
echo("HIGH TRAFFIC DAYS TABLE: \n");
echo '<style>';
echo 'table, th, td {';
echo '  border: 1px solid black;';
echo '  border-collapse: collapse;}';
echo '</style>';
echo '<table>';
echo '<tr>';
echo '  <th>date </th>';
echo '  <th>label </th>';
echo '</tr>';  
while($row = $result->fetchArray()) {   	// for reservation
	//header('Content-type: text/plain');
	echo '<tr><td>' . $row['date'] . '</td><td>' . $row['label'] . '</td></tr>';
	//echo "date = ". $row['date'] . "\n";
	//echo "label = ". $row['label'] ."\n";
}
echo '</table>';
echo('</p>');

?>