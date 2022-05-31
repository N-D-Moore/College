<?php 
    session_start();
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
	    <h1 class="text-center">Welcome To Casa Nostra</h1>
		  <p class="text-center"><center><h2>Buona sera!</h2></center></p>
        <p class="text-center">&nbsp;</p>
<div class="row">
      <div class="col-xl-4">
        <div class="card col-md-4 col-xl-12"> <img src="images/istockphoto-182062973-612x612.jpg" alt="Card image cap" width="318" height="180" class="card-img-top">
              <div class="card-body">
                <h5 class="card-title">Wine&nbsp;</h5>
                <p class="card-text">"Between each wine and each dish one should drink a mouthful of pure fresh water, preferably not (or only slightly) aerated." Paul Ramain
				  <br>
				  <br></p>
                <a href="menu.html" class="btn btn-primary">Check our Wine menu</a> </div>
        </div>
      </div>
          <div class="col-xl-4">
            <div class="card col-md-4 col-xl-12"> <img src="images/istockphoto-502872140-612x612.jpg" alt="Card image cap" width="318" height="180" class="card-img-top">
              <div class="card-body">
                <h5 class="card-title">Private Events&nbsp;</h5>
                <p class="card-text">Create a truly memorable event by letting us host your next private event. The restaurant empahizes in special event from rehearsal dinners to business meetings and corporate events.&nbsp; &nbsp;&nbsp;</p>
                <a href="catering.html" class="btn btn-primary">Catering/Private Events</a> </div>
            </div>
      </div>
          <div class="col-xl-4">
            <div class="card col-md-4 col-xl-12"> <img src="images/loyalty.jpg" alt="Card image cap" width="318" height="180" class="card-img-top">
              <div class="card-body">
                <h5 class="card-title">Rewards&nbsp;</h5>
                <p class="card-text">Join our loyalty program. Members receive different perks based on status level and sometimes get surprise, personalized perks.
					<br>
				<br>
			    </p>
                <a href="signup.html" class="btn btn-primary">Join our eClub</a> </div>
            </div>
      </div>
        </div>
		  <br>
		  <br>
		  <br>
<footer>
  <div class="row">
    <div class="col-xl-6"><img src="images/logo.jpg" width="125" height="75" alt=""/></div>
    <div class="col-xl-6">Copyright © 2021  All Rights Reserved.</div>
  </div>
</footer>
      </div>
	</div>
	<script src="js/bootstrap-4.4.1.js"></script>
  </body>
</html>