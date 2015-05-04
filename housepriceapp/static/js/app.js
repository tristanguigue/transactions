
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Name', 'Number'],
        ['Name 1', 1],
        ['Name 2', 2],
        ['Name 3', 3],
    ]);
    var options = {
      title: 'Transactions',
    };    
    var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
        chart.draw(data, options);
    }


/**
 * The demo application  
 */
var housepriceApp = angular.module('housepriceApp', []);


/**
 * The login controller
 */
housepriceApp.controller('mainController',
  ['$scope', function ($scope) {
    

}]);