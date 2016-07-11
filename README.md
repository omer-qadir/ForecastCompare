ForecastCompare
===============

<p>
	<br>
	Weather prediction is well known to be a difficult task. Regardless, as a <i>consumer</i> of the weather prediction websites, it is very useful to get some measure of which websites are better at consistently getting their prediction right. There are a lot of anecdotal views in circulation, claiming the superiority of one website over another or of local website over foreign websites. The basic concept is simple: Sample the weather prediction for a future date and compare it against the measured value when that date arrives. 
Some of us have cooked up some python scripts in the <a href="https://github.com/omer-qadir/ForecastCompare" target="_blank">ForecastCompare project on GitHub</a> to evaluate the weather prediction accuracy within a very limited set of parameters. Sampling and querying data for all cities is beyond our resource capabilities, so we've set it up to gather the data for Trondheim, Norway. Although this is a somewhat arbitrary choice, the hope is that others will clone the repository and create their own mini-databases for their own cities.
The scripts currently sample the weather predictions from the following:
	<ol>
		<li> <a href="http://www.bbc.com/weather" target="_blank">BBC</a>, </li>
		<li> <a href="http://Yr.no" target="_blank">Yr.no</a>, </li>
		<li> <a href="http://openweathermap.org" target="_blank">Open Weather Map</a>, </li>
	</ol>
</p>
<p>
These predictions are compared against a local weather observation tower. The data and results can be seen at <a href="http://omer.pythonanywhere.com" target="_blank">omer.pythonanywhere.com</a>
</p>
