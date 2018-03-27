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
			
			var mySlider = document.getElementById('myslider');
			var myLabel = document.getElementById('mylabel');

			mySlider.oninput = function() {
				myLabel.innerHTML = "YEAR: " + this.value;
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


