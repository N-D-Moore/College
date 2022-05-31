<?php
//include the databse file below
require_once "connection.php";

$username = $password = $confirm_password = $mailing_address = $billing_address = $email = $payment = ""; // we intialize variable
$username_err = $password_err = $confirm_password_err = $mailing_address_err = $billing_address_err = $email_err = "";

if($_SERVER["REQUEST_METHOD"] == "POST")
{

	// this will be for username
	if(empty(trim($_POST["username"])))
	{
        $username_err = "Please enter a username.";
    }

	elseif(!preg_match('/^[a-zA-Z0-9_]+$/', trim($_POST["username"])))
	{
        $username_err = "Username can only contain letters, numbers, and underscores.";		// restricted username
	}

	else
	{
		if (doesUserExist(trim($_POST["username"]))) {
			$username_err = "This username is already taken.";
		} else {
			$username = trim($_POST["username"]);
		}
		
    }

	// this will be for password
	if(empty(trim($_POST["password"])))
	{
        $password_err = "Please enter a password.";     
    } 
	
	elseif(strlen(trim($_POST["password"])) < 6)
	{
        $password_err = "Password must have atleast 6 characters.";
    } 
	
	else
	{
        $password = trim($_POST["password"]);
    }

	//this will confirm password
	if(empty(trim($_POST["confirm_password"])))
	{
        $confirm_password_err = "Please confirm password.";     
    } 
	
	else
	{
        $confirm_password = trim($_POST["confirm_password"]);
        
		if(empty($password_err) && ($password != $confirm_password))
		{
            $confirm_password_err = "Password did not match.";
        }
    }

	//this will enter the email address
	if(empty(trim($_POST["mailing_address"])))
	{
        $mailing_address_err = "Please enter a valid mailing address.";     
    } 

	else
	{
        $mailing_address = trim($_POST["mailing_address"]);
    }

	// this will enter billing address
	if(empty(trim($_POST["billing_address"])))
	{
        $billing_address_err = "Please enter a valid billing address.";     
    } 

	else
	{
        $billing_address = trim($_POST["billing_address"]);
    }

	// this will take email
	if(empty(trim($_POST["email"])))
	{
        $email_err = "Please enter a valid email.";     
    } 

	else
	{
        $email = trim($_POST["email"]);
    }

	// eneter data in database is remaining
	if (empty($username_err) && empty($password_err) && empty($confirm_password_err) && empty($mailing_address_err) && empty($billing_address_err) && empty($email_err)) {
		$hash = password_hash($password, PASSWORD_DEFAULT);
		insertUser($username, $mailing_address, $billing_address, 0, trim($_POST["payment"]), $email, $username, $hash);
		header("Location:index.php");
	}
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
  	<!-- body code goes here -->


	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) --> 
	<script src="js/jquery-3.4.1.min.js"></script>

	<!-- Include all compiled plugins (below), or include individual files as needed -->
	<script src="js/popper.min.js"></script> 
	<div class="container-fluid">
	  <div class="container">
	    <nav class="navbar navbar-expand-lg navbar-light bg-light"> <a class="navbar-brand" href="#"><img src="images/logo.jpg" width="250" height="150" alt=""/></a>
	      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent1" aria-controls="navbarSupportedContent1" aria-expanded="false" aria-label="Toggle navigation"> <span class="navbar-toggler-icon"></span> </button>
	      <div class="collapse navbar-collapse" id="navbarSupportedContent1">
	        <ul class="navbar-nav ml-auto">
	          <li class="nav-item active"> <a class="nav-link" href="index.php ">Home <span class="sr-only">(current)</span></a> </li>
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
	    <h1 class="text-center">eClub SIGN UP FORM</h1>
        <h2 class="text-center" >Join the Casa Notra eClub for the latest news, events and promotions.</h2>
		 <form action="" method="post">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" class="form-control <?php echo (!empty($username_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                <span class="invalid-feedback"><?php echo $username_err; ?></span>
            </div>    
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $password; ?>">
                <span class="invalid-feedback"><?php echo $password_err; ?></span>
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" name="confirm_password" class="form-control <?php echo (!empty($confirm_password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $confirm_password; ?>">
                <span class="invalid-feedback"><?php echo $confirm_password_err; ?></span>
            </div>
            <div class="form-group">
                <label>Mailing address</label>
                <input type="text" name="mailing_address" class="form-control <?php echo (!empty($mailing_address_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $mailing_address; ?>">
                <span class="invalid-feedback"><?php echo $mailing_address_err; ?></span>
            </div>
            <div class="form-group">
                <label>Billing address</label>
                <input type="text" name="billing_address" class="form-control <?php echo (!empty($billing_address_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $billing_address; ?>">
                <span class="invalid-feedback"><?php echo $billing_address_err; ?></span>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="text" name="email" class="form-control <?php echo (!empty($email_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $email; ?>">
                <span class="invalid-feedback"><?php echo $email_err; ?></span>
            </div>
			<div class="form-group">
				<label>Prefered Payment Method</label>
				<select class="form-control" name="payment" id="payment">
				<option>Credit</option>
				<option>Check</option>
				<option>Cash</option>
				</select>
			</div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Submit">
                <input type="reset" class="btn btn-secondary ml-2" value="Reset">
            </div>
            <p>Already have an account? <a href="login.php">Login here</a>.</p>
        </form>
		 
        <p class="text-center">&nbsp;</p>
        <div class="row">
      
          <div class="col-xl-4"> </div>
          <div class="col-xl-4"></div>
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