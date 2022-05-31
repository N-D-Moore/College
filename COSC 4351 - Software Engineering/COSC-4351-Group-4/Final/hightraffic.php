<?php
  
// Initialize the session
require "connection.php";
session_start();
       
// Store the submitted data sent
// via POST method, stored 
if(isset($_SESSION['id']))      // we have set id and username to Session variable   //isset will check if the variable is not null
{
    echo '<p class="text-white bg-dark text-center">Welcome '. $_SESSION['name'] .', Enter the card details here!</p>';
}

if(isset($_SESSION['var']))      // we have set id and username to Session variable   //isset will check if the variable is not null
{
    echo '<p class="text-white bg-dark text-center">Welcome '. $_SESSION['var'] .', Enter details</p>';
}
  
// Temporarily in $_POST structure.
/*$_SESSION['name'] = $_POST['name'];                 // all this information is stored from previous page 
$_SESSION['date'] = $_POST['date'];
$_SESSION['time'] = $_POST['time'];
$_SESSION['num_guests'] = $_POST['num_guests'];
$_SESSION['tele'] = $_POST['tele'];
$_SESSION['email'] = $_POST['email'];*/


$all_error = $cardtype_error = $cardno_error = $cvv_error = $expdate_error = ""; 
$cardtype = $cardno = $cvv = $expdate = ""; 

if(isset($_POST['final-submit']))  //use button name = reserv-submit in html doc below
{
            // we can add user id = $session['id] but i have to check how it work
    $cardtype = $_POST['cardtype'];
    $cardno = $_POST['cardno'];
    $cvv = $_POST['cvv'];
    $expdate = $_POST['expdate'];
}

    if(empty($cardtype) || empty($cardno) || empty($cvv) || empty($expdate))
    {
        $all_error = "fields cannot be empty";
    }
    
    elseif(!preg_match("/^[a-zA-Z0-9]*$/", $cardno) || !between($cardno,6,20))
    {
        $cardno_error = "please enter valid card no number";
    }
    elseif(!preg_match("/^[a-zA-Z0-9]*$/", $cvv) || !between($cvv,2,4))
    {
        $cvv_error = "please enter valid Cvv number";
    }
    elseif(!preg_match("/^[a-zA-Z0-9]*$/", $expdate) || !between($expdate,0,3))
    {
        $expdate_error = "please enter valid expiration date";
    }
	
	if(empty($cardno_error) && empty($cvv_error) && empty($expdate_error) && !empty($cardtype) && !empty($cardno) && !empty($cvv) && !empty($expdate)) {		
		insertReservation(0, $_SESSION['date'], $_SESSION['time'], $_SESSION['name'], $_SESSION['tele'], $_SESSION['email'], intval($_SESSION['num_guests']), "", "Credit");
		header("Location:index.php");
	}

?>

<!DOCTYPE html>
<html lang="en">
    <head>
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
          <li class="nav-item active"> <a class="nav-link" href="reservations.php">Book A Table <span class="sr-only">(current)</span></a></li>
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

        <form method="POST" action="hightraffic.php"> <!-- change this to any php file for connecting databse-->
        
        <div class="form-group">
            <label>Card Type</label>
            <select class="form-control" name="cardtype" id="cardtype" required ="required">
            <option>Credit Card</option>
            <option>Debit Card</option>
            </select>
        </div> 

        <div class="form-group">
            <label>Card Number</label>
            <input type="cardno" class="form-control" min="10" name="cardno" id ="cardno" placeholder="Card no" required="required">
            <small class="form-text text-muted">Card no must be 16 digits</small>
        </div>
        
        <div class="form-group">
            <label for="cvv">Enter Cvv</label>
            <input type="cvv" class="form-control" name="cvv" placeholder="cvv" id = "cvv" required="required">
            <small class="form-text text-muted">Cvv must be 3 or 4 digits</small>
        </div>
    
        <div class="form-group">
            <label for="expdate">Enter expiration Date</label>
            <input type="expdate" class="form-control" name="expdate" placeholder="expdate" id ="expdate" required="required">
            <small class="form-text text-muted">Enter expiration date with "/"</small>
        </div>   

        <div class="form-group">
            <label class="checkbox-inline"><input type="checkbox" required="required"> I accept the <a href="#">Terms of Use</a> &amp; <a href="#">Privacy Policy</a></label>
        </div>
        
        <div class="form-group">
             
        <input type="submit" name="final-submit" class="btn btn-dark btn-lg btn-block" class="form-control">Submit Reservation</a></button>
    
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
