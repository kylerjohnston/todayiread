var xmlhttp = new XMLHttpRequest();
var url = "/api/sessions/" + username;

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var myArr = JSON.parse(xmlhttp.responseText);
        get_sessions(myArr);
    }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();

function get_sessions(arr) {
  lines = [];
  for (i = 0; i < arr.length; i++) {
    lines.push("<h1>Session " + i + "</h1>");
    lines.push("<dl><dt>Date</dt><dd>" + arr[i]['date'] + "</dd></dl>");
  };
  document.getElementById("all-sessions").innerHTML = lines;
};
