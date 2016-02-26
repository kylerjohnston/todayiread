var url = "/api/sessions/" + user_id;

function get_sessions(arr) {
  var session_count = arr['session'].length;
  $("span#session-count").html(session_count);
};

function user_dates(date) {
//  var registration = new Date(date.slice(0,10));
  var today = new Date();
  $("span#registration-length").html(date_diff(today, date));
};

function date_diff(date_one, date_two) {
  var one_day = 24*60*60*1000;
  return Math.round(Math.abs((date_one.getTime() - date_two.getTime())/one_day));
};

function arrayify_sessions(sessions) {
  var array = [];
  for (i = 0; i < sessions.length; i++) {
    var row = [];
    row.push(sessions[i]['date']);
    row.push(sessions[i]['title']);
    row.push(sessions[i]['author']);
    row.push(sessions[i]['genre']);
    row.push(sessions[i]['pages']);
    array.push(row);
  };
  return array;
};

function generate_session_table(dataSet) {
  var transformed = arrayify_sessions(dataSet['session']);
  $("table#session-table").DataTable( {
    data: transformed,
    columns: [
    { title: "date" },
    { title: "title" },
    { title: "author" },
    { title: "genre" },
    { title: "pages" }
    ]
  });
};

function get_pages(data) {
  var page_total = 0;
  for (i = 0; i < data.length; i++) {
    page_total += data[i]['pages'];
  };
  $("span#total-pages").html(page_total);
};

function gen_pages_per_day_timeseries(dataSet) {
  var	margin = {top: 30, right: 30, bottom: 30, left: 50},
	  width = 750 - margin.left - margin.right,
	  height = 270 - margin.top - margin.bottom;
  var	parseDate = d3.time.format("%Y %m %d").parse;
  var	x = d3.time.scale().range([0, width]);
  var	y = d3.scale.linear().range([height, 0]);
  var	xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);
  var	yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);
  var area = d3.svg.area()
    .x(function(d) { return x(d.date) })
    .y0(height)
    .y1(function(d) { return y(d.pages) });
  var	valueline = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.pages); });
  var	svg = d3.select("#pages-per-day-timeseries")
    .append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
    .append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  data = date_and_pages_table(dataSet.session);
  x.domain(d3.extent(data, function(d) { return d.date; }));
	y.domain([0, d3.max(data, function(d) { return d.pages; })]);
  svg.append("path")
    .datum(data)
    .attr("class", "area")
    .attr("d", area);
  svg.append("path")	
		.attr("class", "line")
		.attr("d", valueline(data));
  svg.append("g")		
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);
  svg.append("g")		
		.attr("class", "y axis")
		.call(yAxis);
  svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", -50)
    .attr("dy", ".75em")
    .attr("transform", "rotate(-90)")
    .text("pages");
};

function date_and_pages_table(sessions) {
  var parseDate = d3.time.format("%Y %m %d").parse;
  var stringDate = d3.time.format("%Y %m %d");
	var data = [];
  sessions.forEach(function(s) {
  	var matched = false;
  	data.forEach(function(d) {
    	if(s.date === d.date) {
      	matched = true;
      	d.pages += +s.pages;
      }
    });
    if (!matched) {
    	data.push({"date": s.date, "pages": +s.pages});
    }
  });
  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });
  data.sort(function(a, b) {
    return a.date - b.date;
  });
  var mindate = data[0].date;
//  var maxdate = data[data.length - 1].date;
  var maxdate = new Date();
  var daterange = d3.time.days(mindate, maxdate);
  new_data = [];
  daterange.forEach(function(d) {
    new_data.push({"date": d, "pages": 0});
  });
  data.forEach(function(d) {
    new_data.forEach(function(n) {
      if(stringDate(d.date) == stringDate(n.date)) {
        n.pages += d.pages;
      }
    });
  });
  user_dates(new_data[0].date);
  return new_data;
};

// user_dates(registration_date);

$.getJSON(url, function(data) {
  get_pages(data['session']);
  get_sessions(data);
  generate_session_table(data);
  gen_pages_per_day_timeseries(data);
});
