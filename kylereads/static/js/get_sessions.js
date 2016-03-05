if(typeof jQuery === 'undefined') {
  document.write(unescape("%3Cscript src='/static/js/jquery-2.2.1.min.js' type='text/javascript'%3E%3C/script%3E"));
};

if(typeof d3 === 'undefined') {
  document.write(unescape("%3Cscript src='/static/js/d3.min.js' type='text/javascript'%3E%3C/script%3E"));
};

function count_sessions(arr) {
  var session_count = arr['session'].length;
  $("span#session-count").html(session_count);
};

function user_dates(date) {
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
  if(data === 0) {
    $("#pages-per-day-timeseries").html("You haven't added any reading sessions yet.");
  }
  else {
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
      .attr("y", 6)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .text("Pages");
  }
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
  if(data.length === 0) {
    return 0;
  }
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

function day_bar_graph(data) {
  var margin = {top: 40, right: 20, bottom: 30, left: 40},
  width = 750 - margin.left - margin.right,
  height = 270 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

  var y = d3.scale.linear()
    .range([height, 0]);

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

  var svg = d3.select("#pages-bar").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data = transform_day_counts(data.session);

  x.domain(data.map(function(d) { return d.day; }));
  y.domain([0, d3.max(data, function(d) { return d.total; })]);

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Pages");

  svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) { return x(d.day); })
    .attr("width", x.rangeBand())
    .attr("y", function(d) { return y(d.total); })
    .attr("height", function(d) { return height - y(d.total); })
};

function transform_day_counts(data) {
  var parseDate = d3.time.format("%Y %m %d").parse;
  bars = [
    {"day": "Sun", "total": 0, "count": 0},
    {"day": "Mon", "total": 0, "count": 0},
    {"day": "Tues", "total": 0, "count": 0},
    {"day": "Wed", "total": 0, "count": 0},
    {"day": "Thurs", "total": 0, "count": 0},
    {"day": "Fri", "total": 0, "count": 0},
    {"day": "Sat", "total": 0, "count": 0}
  ];
  data.forEach(function(d) {
    d.date = parseDate(d.date);
    day = d.date.getDay();
    bars[day].total += +d.pages;
  });
  return bars;
};

function author_bubbles(data) {
	var diameter = 750;

	var svg = d3.select('#author-bubbles').append('svg')
					.attr('width', diameter)
					.attr('height', diameter);

	var bubble = d3.layout.pack()
				.size([diameter, diameter])
				.value(function(d) {return d.size;})
         // .sort(function(a, b) {
				// 	return -(a.value - b.value)
				// }) 
				.padding(3);
  
  // generate data with calculated layout values
  var nodes = bubble.nodes(transform_author_data(data.session))
						.filter(function(d) { return !d.children; }); // filter out the outer bubble
 
  var vis = svg.selectAll('circle')
					.data(nodes);
  vis.enter().append('g')
    .attr("class", "node")
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  vis.append('circle')
			.attr('r', function(d) { return d.r; })
			.attr('class', function(d) { return d.className; });

  vis.append("text")
      .attr("dy", ".3em")
      .attr("class", "circle")
      .style("text-anchor", "middle")
      .text(function(d) { return d.name.substring(0, d.r / 3); });
};

function transform_author_data(data) {
  var author_data = [];
  data.forEach(function(d) {
    var matched = false;
    author_data.forEach(function (a) {
      if(a.name === d.author) {
        a.size += +d.pages;
        matched = true;
      }
    });
    if(!matched) {
      author_data.push({"name": d.author,
        "className": "author-circle",
        "size": +d.pages});
    }
  });
  return {"children": author_data};
};

function genre_bars(data) {
  var margin = {top: 40, right: 20, bottom: 30, left: 40},
  width = 750 - margin.left - margin.right,
  height = 270 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

  var y = d3.scale.linear()
    .range([height, 0]);

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

  var svg = d3.select("#genre-bars").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data = transform_genre_counts(data.session);

  x.domain(data.map(function(d) { return d.genre; }));
  y.domain([0, d3.max(data, function(d) { return d.count; })]);

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Pages");

  svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) { return x(d.genre); })
    .attr("width", x.rangeBand())
    .attr("y", function(d) { return y(d.count); })
    .attr("height", function(d) { return height - y(d.count); })
};

function transform_genre_counts(data) {
  var bars = [];
  data.forEach(function(d) {
    matched = false;
    bars.forEach(function(b) {
      if(b.genre === d.genre) {
        b.count += +d.pages;
        matched = true;
      }
    });
    if(!matched) {
      bars.push({"genre": d.genre, "count": +d.pages});
    }
  });
  return bars;
}

if(typeof user_id !== 'undefined') {
  var url = "/api/sessions/" + user_id;
  $.getJSON(url, function(data) {
    get_pages(data['session']);
    count_sessions(data);
    generate_session_table(data);
    gen_pages_per_day_timeseries(data);
    day_bar_graph(data);
    author_bubbles(data);
    genre_bars(data);
  });
}

var sessionDateField = document.getElementById("new-session-date");
if(sessionDateField !== null) {
  var today = new Date();
  var parseDate = d3.time.format("%Y-%m-%d");
  var dateField = parseDate(today);
  sessionDateField.setAttribute("value", dateField);
}
