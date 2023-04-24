setInterval(function() {
  $.getJSON('/t', function(data) {
      CreateHtmlTable(data);
  });
  return false;
}, 3000);

function CreateHtmlTable(data) {
$("#ResultArea").html("");  
var table = $("<table class='table table-striped table-light table-bordered table-hover table-sm table-responsive' id='DynamicTable'></table>").appendTo("#ResultArea");
var rowHeader = $("<tr></tr>").appendTo(table);
$("<td></td>").text("Name").appendTo(rowHeader);
$("<td></td>").text("Album").appendTo(rowHeader);
$("<td></td>").text("Artist").appendTo(rowHeader);
$.each(data, function (i, value) {
    var row = $("<tr></tr>").appendTo(table);
    $("<td></td>").text(value.Name).appendTo(row);
    $("<td></td>").text(value.Album).appendTo(row);
    $("<td></td>").text(value.Artist).appendTo(row);
});
}
