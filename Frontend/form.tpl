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