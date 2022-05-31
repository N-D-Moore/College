<?php

require "connection.php";
session_start();

//if(isset($_SESSION['id']))      // we have set id and username to Session variable   //isset will check if the variable is not null
//{
//    echo '<p class="text-white bg-dark text-center">Welcome '. $_SESSION['username'] .', Create your reservation here!</p>';
//}

function between($val, $x, $y)      // function to decide the value is correct or not
{
    $val_len = strlen($val);
    return ($val_len >= $x && $val_len <= $y)?TRUE:FALSE;
}

$all_error = $name_error = $guests_error = $tele_error = $email_error = ""; 

if(isset($_POST['reserv-submit']))  //use button name = reserv-submit in html doc below
{
            // we can add user id = $session['id] but i have to check how it work
    $name = $_POST['name'];
    $date = $_POST['date'];
    $time= $_POST['time'];
    $guests= $_POST['num_guests'];
    $tele = $_POST['tele'];
    $email = $_POST['email'];
	$avaiableSeats = getRemainingSeats($date);
    
  
    if(empty($name) || empty($date) || empty($time) || empty($guests) || empty($tele) ||empty($email))
    {
        $all_error = "fields cannot be empty";
    }

    elseif(!preg_match("/^[a-zA-Z ]*$/",$name) || !between($name,2,20))          // we can try this or we can do the between function.
    {
        $name_error = "please enter valid name";
    }

    elseif(!preg_match("/^[0-9]*$/", $guests))
    {
        $guests_error = "please enter number of guest";
    }
	
	elseif(intval($guests) > intval($avaiableSeats)){
		$guests_error = "too many guests for choosen date";
	}

    elseif(!preg_match("/^[a-zA-Z0-9]*$/", $tele) || !between($tele,6,20))
    {
        $tele_error = "please enter valid number";
    }

    elseif(!preg_match("/^[a-zA-Z0-9@]*$/", $email) || !between($email,6,20))           // i tried this if error comes we can remove it
    {
        $tele_error = "please enter valid email";
    }
    
}

if(array_key_exists('date', $_POST)) 
{
  check($_POST['date']);
}
function check($date)
{
  $db = new MyDB();
        if (!$db) {
          echo $db -> lastErrorMsg();
        }

        $statement = $db->prepare("SELECT date FROM high_traffic_days WHERE date = :date");

        $statement->bindValue(":date", $date);    // values selecetd at reservation
        $result = $statement->execute();
    
        if (emptyResult($result)) {
			
			$name = $_POST['name'];
			$date = $_POST['date'];
			$time= $_POST['time'];
			$guests= $_POST['num_guests'];
			$tele = $_POST['tele'];
			$email = $_POST['email'];
			$avaiableSeats = getRemainingSeats($date);
			$id = 0;
			$payment_meth = 'Cash';
			
			if ($_SESSION["loggedin"] == true) {
				$id = $_SESSION["id"];
				$payment_meth = getUserPayment($id);
			}
			
			if (intval($guests) < intval($avaiableSeats)) {
				insertReservation($id, $date, $time, $name, $tele, $email, intval($guests), "", $payment_meth);
				header("Location:index.php");
			}

          $var = "0";       //var stores the value but how to link it still not get it
          $_SESSION["var2"] = $var;
          echo $var;                  
        } 
        else 
        {
			$_SESSION['name'] = $_POST['name'];                 // all this information is stored from previous page 
			$_SESSION['date'] = $_POST['date'];
			$_SESSION['time'] = $_POST['time'];
			$_SESSION['num_guests'] = $_POST['num_guests'];
			$_SESSION['tele'] = $_POST['tele'];
			$_SESSION['email'] = $_POST['email'];
			$avaiableSeats = getRemainingSeats($date);
			
			if (intval($guests) < intval($avaiableSeats)) {
				header("Location:hightraffic.php");
			}

          $var = "1";  //high traffic 
          $_SESSION["var2"] = $var;
          echo $var;
        }
        $db->close();
}

?>


<!DOCTYPE html>
<html lang="en">
    <head>
		<script>
		function showHint() {
			var date = document.getElementById("date");
			var strDate = date.value; <!-- options[e.selectedIndex].text -->  // pulls the value selected in text
			if (strDate.length == 0) {
				document.getElementById("txtSeat").innerHTML = "No date selected";
				return;
			} else {
				var xmlhttp = new XMLHttpRequest();
				xmlhttp.onreadystatechange = function() {
				  if (this.readyState == 4 && this.status == 200) {
					document.getElementById("txtSeat").innerHTML = this.responseText;   // echo will store in txtseat
				  }
				};
				var time = document.getElementById("time");
				var strTime = time.options[time.selectedIndex].text;
				let temp = strTime.split(" ")
				var numGuests = document.getElementById("num_guests");
				var strTemp = strDate + " " + numGuests;
				var strNum = numGuests.value;
				var strTemp = 13
				xmlhttp.open("GET", "table.php?q=" + strDate, true); // this is q send to table.php 
				xmlhttp.send();
			}
		}
		</script>

        <meta charset="utf-8">
	    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	    <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Untitled Document</title>
        <!-- Bootstrap -->
	    <link href="css/bootstrap-4.4.1.css" rel="stylesheet">
	    <link href="style.css" rel="stylesheet" type="text/css">
	 
    </head> 
    
    <body>
    <script src="js/jquery-3.4.1.min.js"></script>

<!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="js/popper.min.js"></script> 
<div class="container-fluid">
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light"> <a class="navbar-brand" href="#"><img src="images/logo.jpg" width="250" height="150" alt=""/></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent1" aria-controls="navbarSupportedContent1" aria-expanded="false" aria-label="Toggle navigation"> <span class="navbar-toggler-icon"></span> </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent1">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active"> <a class="nav-link" href="index.php">Home <span class="sr-only">(current)</span></a> </li>
          <li class="nav-item active"> <a class="nav-link" href="menu.php">Menu <span class="sr-only">(current)</span></a></li>
          <li class="nav-item active"> <a class="nav-link" href="reservation.php">Book A Table <span class="sr-only">(current)</span></a></li>
          <li class="nav-item active"> <a class="nav-link" href="catering.php">Private Events <span class="sr-only">(current)</span></a></li>
            <li class="nav-item active"> <a class="nav-link" href="signup.php">Sign up <span class="sr-only">(current)</span></a></li>
            <li class="nav-item active"> <a class="nav-link" href="login.php">Log In<span class="sr-only">(current)</span></a></li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
        </form>
      </div>
    </nav>
    <div id="carouselExampleIndicators1" class="carousel slide" data-ride="carousel" style="background-color: grey">
      <ol class="carousel-indicators">
        <li data-target="#carouselExampleIndicators1" data-slide-to="0" class="active"></li>
        <li data-target="#carouselExampleIndicators1" data-slide-to="1"></li>
        <li data-target="#carouselExampleIndicators1" data-slide-to="2"></li>
      </ol>
      <div class="carousel-inner" role="listbox">
        <div class="carousel-item active"> <img src="images/1.jpg" alt="First slide" class="d-block mx-auto">
          <div class="carousel-caption">
          </div>
        </div>
        <div class="carousel-item"> <img class="d-block mx-auto" src="images/2.jpg" alt="Second slide">
          <div class="carousel-caption">
          </div>
        </div>
        <div class="carousel-item"> <img class="d-block mx-auto" src="images/3.jpg" alt="Third slide">
          <div class="carousel-caption">
          </div>
        </div>
          <div class="carousel-item"> <img class="d-block mx-auto" src="images/4.jpg" alt="Second slide">
          <div class="carousel-caption">
          </div>
        </div>
      </div>
      <a class="carousel-control-prev" href="#carouselExampleIndicators1" role="button" data-slide="prev"> <span class="carousel-control-prev-icon" aria-hidden="true"></span> <span class="sr-only">Previous</span> </a> <a class="carousel-control-next" href="#carouselExampleIndicators1" role="button" data-slide="next"> <span class="carousel-control-next-icon" aria-hidden="true"></span> <span class="sr-only">Next</span> </a> </div>
    <h1 class="text-center">&nbsp;</h1>
    <h1 class="text-center">Reserve Your Table</h1>
    <p class="text-center">&nbsp;</p>

          <center>

        <form action="" method="POST">
        
        <div class="form-group">
            <label>First Name</label>
            <input type="text" class="form-control" name="name" placeholder="Name" id="name" required="required">
            <small class="form-text text-muted">Name must be 2-20 characters long</small>
        </div> 
        
        <div class="form-group">
    
            <label>Enter Date</label>
            <input type="date" class="form-control" name="date" id ="date" placeholder="Date" required="required" onchange="showHint()">
        </div>

        <div class="form-group">
            <label>Enter Time Zone</label>
            <select class="form-control" name="time" id="time">
            <option>16:00 - 17:00</option>
            <option>17:00 - 18:00</option>
            <option>18:00 - 19:00</option>
            <option>19:00 - 20:00</option>
            <option>20:00 - 21:00</option>
            <option>21:00 - 22:00</option>
            </select>
        </div>
		
		<div> 
			Available Seats: <span id="txtSeat"></span>
		</div>
    
        <div class="form-group">
            <label>Enter number of Guests</label>
            <input type="number" class="form-control" min="1" name="num_guests" id ="num_guests" placeholder="Guests" required="required" onchange="showHint()">
            <small class="form-text text-muted">Minimum value is 1</small>
        </div>
        
        

    
        <div class="form-group">
            <label for="guests">Enter your Telephone Number</label>
            <input type="telephone" class="form-control" name="tele" placeholder="Telephone" id = "tele" required="required">
            <small class="form-text text-muted">Telephone must be 6-20 characters long</small>
        </div>
    
        <div class="form-group">
            <label for="email">Enter your Email</label>
            <input type="email" class="form-control" name="email" placeholder="email" id ="email" required="required">
            <small class="form-text text-muted">Email should have @.com </small>
        </div> 	

        <div class="form-group">
            <label class="checkbox-inline"><input type="checkbox" required="required"> I accept the <a href="#">Terms of Use</a> &amp; <a href="#">Privacy Policy</a></label>
        </div>
        
        <div class="form-group">
             
        <input type="submit" name="reserv-submit" class="btn btn-dark btn-lg btn-block" class="form-control">Submit Reservation</button>
    
        </div>
        
       
      
        </form>
        <br><br>
    </div>

    </center>




    
</div>
      <br>
      <br>
      <br>
<footer>
<div class="row">
<div class="col-xl-6">"This is where the logo goes"</div>
<div class="col-xl-6">Copyright © 2021  All Rights Reserved.</div>
</div>
</footer>
  </div>
</div>
<script src="js/bootstrap-4.4.1.js"></script>
</body>
</html>
