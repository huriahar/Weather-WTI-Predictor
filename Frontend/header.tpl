<!DOCTYPE html>
<html lang="en">
<head>
    <title>Predict Oil</title>

	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/js/bootstrap.min.js" integrity="sha384-a5N7Y/aK3qNeh15eJKGWxsqtnX/wWdSZSKp+81YjTmS15nvnvxKHuzaWwXHDli+4" crossorigin="anonymous"></script>
	<link rel="stylesheet" type="text/css" href="/static/frontend.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>


	<script type="text/javascript">
		window.onload=function(){
			
			var SliderYear = document.getElementById('slideryear');
			var LabelYear = document.getElementById('labelyear');

			SliderYear.oninput = function() {
				LabelYear.innerHTML = "YEAR: " + this.value;
			}

			var SliderFuture = document.getElementById('sliderfuture');
			var LabelFuture = document.getElementById('labelfuture');

			SliderFuture.oninput = function() {
				if (this.value == "1"){value = "1"}
				else if (this.value == "2"){value="7"}
				else if (this.value == "3"){value="14"}
				else if (this.value == "4"){value="30"}
				else if (this.value == "5"){value="60"}
				else{value="90"}
				LabelFuture.innerHTML = "FUTURE DAY: " + value;
			}

			var SliderPast = document.getElementById('sliderpast');
			var LabelPast = document.getElementById('labelpast');

			SliderPast.oninput = function() {
				if (this.value == "1"){value = "5"}
				else if (this.value == "2"){value="7"}
				else if (this.value == "3"){value="14"}
				else if (this.value == "4"){value="30"}
				else{value="60"}
				LabelPast.innerHTML = "PAST DAYS: " + value;
			}


		}
	</script>




</head>
<body>	
	<nav class="navbar navbar-dark bg-dark">
		<div class="navbar-header">
			<a class="navbar-brand" href="/">WTI Forecast</a>
		</div>
		<ul class="nav navbar-nav navbar-right">
			<li class="nav-item">
				<a class="nav-link" href="/faq">F.A.Q</a>
			</li>
		</ul>  
	</nav> <br /> <br />
</body>
</html>


