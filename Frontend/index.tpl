<!DOCTYPE html>
<html lang="en">
<head>
    <title>Predict Oil</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <!-- <link rel="stylesheet" type="text/css" href="/static/index.css"> -->
</head>
<body>	
	<nav class="navbar navbar-dark bg-dark">
		<div class="navbar-header">
			<a class="navbar-brand" href="/">WebSiteName</a>
		</div>
		<div class="navbar-nav ml-auto" >
			<a class="nav-link" href="/about">About Us</a>
		</div>
	</nav> <br /> <br />
	
	<div class="container h-100">
		<div class="row align-items-center h-100">
			<div class="col-3 mx-auto" align="center">

				<form action="/results" method="post" id="getinput">

					<div class="form-group">
						<input name="past" type="text" class="form-control form-control-lg" placeholder="Past Days">
					</div>

					<div class="form-group">
						<input name="future" type="text" class="form-control form-control-lg" placeholder="Future Days">
					</div>

					<small class="form-text text-muted">Enter digits from 1 to 999</small><br />
					<button type="submit" class="btn btn-success">Submit</button>

				</form>

			</div>
		</div>
	</div>


	<nav class="navbar fixed-bottom navbar-dark bg-dark">
		<div class="navbar-header">
			<a class="navbar-text" href="/">Developed by ... </a>
		</div>
		<div class="navbar-nav ml-auto" >
			<a class="nav-link" href="/faq">F.A.Q</a>
		</div>
	</nav>

</body>
</html>


