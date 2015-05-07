
google.load("visualization", "1", {packages:["corechart"]});

/**
 * The demo application  
 */
var housepriceApp = angular.module('housepriceApp', []);

/**
 * The main controller
 */
housepriceApp.controller('mainController',
  ['$scope', 'TransactionService', function ($scope, TransactionService) {
    var chartsActive = false
    var drawCharts = function() {
        chartsActive = true
    }
    google.setOnLoadCallback(drawCharts);


    $scope.months = [
      {value: 1, label: "January"},
      {value: 2, label: "February"},
      {value: 3, label: "March"},
      {value: 4, label: "April"},
      {value: 5, label: "May"},
      {value: 6, label: "June"},
      {value: 7, label: "July"},
      {value: 8, label: "August"},
      {value: 9, label: "September"},
      {value: 10, label: "October"},
      {value: 11, label: "November"},
      {value: 12, label: "December"},
    ];

    $scope.years = []
    for(var i = 2013; i <= 2015; ++i)
        $scope.years.push(i)

    $scope.historyFilters = {
        from: {
            month : 1,
            year: 2013            
        },
        to: {
            month : 5,
            year: 2015           
        }
    }
    $scope.segmentationFilters = {
        month : 6,
        year: 2013            
    }

    var drawHistory = function(data){
        if(!chartsActive)
            return

        var data = google.visualization.arrayToDataTable(data);
        var options = {
            title: 'Transactions',
            width: 800,
            height: 600,        
        };    
        var chart = new google.visualization.LineChart(document.getElementById('history_chart'));
        chart.draw(data, options);
    }

    var updateHistory = function(){
        var filters = {
            date: $scope.historyFilters,
            locality: $scope.locality
        }

        TransactionService.getHistory(filters).success(function(results){
            var raw = results.results
            var processed = {}
            for(i in raw){
                var year = raw[i].year
                var month = raw[i].month
                if (!(year in processed))
                    processed[year] = {}
                if (!(month in processed[year]))
                    processed[year][month] = {}
                processed[year][month][raw[i].property_type] = raw[i].price_avg
            }
            var propertyTypes = TransactionService.getPropertyType();
            var propertyTypeNames = [];
            var propertyTypeKeys = [];
            for(var key in propertyTypes){
                propertyTypeNames.push(propertyTypes[key]);  
                propertyTypeKeys.push(key);              
            }
            var data = [["Month"].concat(propertyTypeNames)]
            for(year in processed){
                for(month in processed[year]){
                    var priceAverages = processed[year][month]
                    var currentData = [year + "/" + month]
                    for(i in propertyTypeKeys)
                        currentData.push(priceAverages[propertyTypeKeys[i]])
                    data.push(currentData)
                }      
            }
            drawHistory(data)
        });    
    }

    var drawSegmentation = function(data){
        if(!chartsActive)
            return

        var data = google.visualization.arrayToDataTable(data);
        var options = {
            title: 'Transactions',
            width: 800,
            height: 600,            
        };    
        var chart = new google.visualization.BarChart(document.getElementById('segmentation_chart'));
        chart.draw(data, options);        
    }

    var updateSegmentation = function(){
        var BINS = 8
        var filters = {
            date: {
                from: $scope.segmentationFilters,
                to: $scope.segmentationFilters
            },
            locality: $scope.locality
        }
        TransactionService.getSegmentation(filters, BINS)
                .success(function(results){
            var data = [['Price Bin', 'Number of transactions']]
            var raw = results.results

            if(raw.length){
                min_price = raw[0].price_min
                max_price = raw[raw.length - 1].price_max
                interval = (min_price + max_price) / BINS

                var i = 0
                for(bin_index = 1; bin_index <= BINS; ++bin_index){
                    var low = min_price + (bin_index - 1)* interval
                    var high = min_price + bin_index * interval

                    if(raw[i].price_bin == bin_index){
                        data.push([low + " - " + high, raw[i].count])
                        i++
                    }else{
                        data.push([low + " - " + high, 0])
                    }

                }
            }
            drawSegmentation(data)
        });
    }


    $scope.updateCharts = function(){
        updateHistory()
        updateSegmentation()
    }

    $scope.$watch('historyFilters', function(newValue, oldValue){
        if(newValue != oldValue)
            updateHistory()
    }, true) 

    $scope.$watch('segmentationFilters', function(newValue, oldValue){
        if(newValue != oldValue)
            updateSegmentation()
    }, true) 
}]);