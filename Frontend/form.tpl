<div class="container" align="center">
	<div class="jumbotron">
		<h1 style="font-size: 400%;">WTI CRUDE OIL FORECASTING TOOL</h1>
	</div>
</div>



<div class="container">
	<form action="/" method="post" id="getinput" >
		<div class="row">
			<div class="col-sm-4">
				<h5>
					<label for="slideryear" id="labelyear"> YEAR: 2007</label>
				</h5>
			</div>
			<div class="col-sm-8">
				<div class="slider">
				    <input type="range" class="slider" id="slideryear" min="2007" max="2015" value="2007" name="year" />
				</div>
			</div>
		</div>

		<br >
		<div class="row">
			<div class="col-sm-4">
				<h5> 
					<label for="sliderfuture" id="labelfuture"> FUTURE DAY: 1</label>
				</h5>
			</div>
			<div class="col-sm-8">
				<div class="slider">
				    <input type="range" class="slider" id="sliderfuture" value="1" min="1" max="6" step="1" name="future" />
				</div>
			</div>
		</div>

		<br >
		<div class="row">
			<div class="col-sm-4">
				<h5>
					<label for="sliderpast" id="labelpast"> PAST DAYS: 5</label>
				</h5>
			</div>
			<div class="col-sm-8">
				<div class="slider">
				    <input type="range" class="slider" id="sliderpast" value="1" min="1" max="5" step="1" name="past"  />
				</div>			
			</div>
		</div>

		<br ><br >
		<div class="col text-center"> 
			<button type="submit" class="btn btn-success" align="center">Submit</button>
		</div>
	</form>
</div>



<!-- _________________________________ Previous form _________________________________________________________ -->
<!-- _________________________________________________________________________________________________________ -->
<!-- _________________________________________________________________________________________________________ -->

<!-- For year -->
<!-- 				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year07" value="2007">
				  <label class="form-check-label" for="year07">2007</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year08" value="2008">
				  <label class="form-check-label" for="year08">2008</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year09" value="2009">
				  <label class="form-check-label" for="year09">2009</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year10" value="2010">
				  <label class="form-check-label" for="year10">2010</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year11" value="2011">
				  <label class="form-check-label" for="year11">2011</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year12" value="2012">
				  <label class="form-check-label" for="year12">2012</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year13" value="2013">
				  <label class="form-check-label" for="year13">2013</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year14" value="2014">
				  <label class="form-check-label" for="year14">2014</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="year" id="year15" value="2015">
				  <label class="form-check-label" for="year15">2015</label>
				</div> -->



<!-- For Future -->
				<!-- 				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="future" id="future1" value="1">
				  <label class="form-check-label" for="future1">1</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="future" id="future7" value="7">
				  <label class="form-check-label" for="future7">7</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="future" id="future14" value="14">
				  <label class="form-check-label" for="future14">14</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="future" id="future30" value="30">
				  <label class="form-check-label" for="future30">30</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="future" id="future60" value="60">
				  <label class="form-check-label" for="future60">60</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="future" id="future90" value="90">
				  <label class="form-check-label" for="future90">90</label>
				</div> -->

<!-- For Past -->
<!-- 				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="past" id="past5" value="5">
				  <label class="form-check-label" for="past5">5</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="past" id="past7" value="7">
				  <label class="form-check-label" for="past7">7</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="past" id="past14" value="14">
				  <label class="form-check-label" for="past14">14</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="past" id="past30" value="30">
				  <label class="form-check-label" for="past30">30</label>
				</div>
				<div class="form-check form-check-inline">
				  <input class="form-check-input" type="radio" name="past" id="past60" value="60">
				  <label class="form-check-label" for="past60">60</label>
				</div> -->