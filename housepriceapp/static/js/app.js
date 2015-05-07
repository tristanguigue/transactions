
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
    // For readability we will divide all prices by 1000
    var PRICE_DIVISOR = 1000

    // We will allow charts to be drawn once google charts is loaded
    var chartsActive = false
    var drawCharts = function() {
        chartsActive = true
    }
    google.setOnLoadCallback(drawCharts);

    // Month and year dropdowns
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
    for(var i = 2010; i <= 2015; ++i)
        $scope.years.push(i)

    // We prefilled the data
    $scope.historyFilters = {
        from: {
            month : 1,
            year: 2010            
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

    $scope.locality = 'SO40'
    $scope.showHistory = true
    $scope.showSegmentation = true

    /**
     * Draw the history chart.
     * @param {object} data The data to feed the chart
     */
    var drawHistory = function(data){
        if(!chartsActive)
            return

        var options = {
            title: 'Average Price of Transactions (k£)',
            width: 800,
            height: 450,
            interpolateNulls: true     
        }; 

        var chart = new google.visualization.LineChart(document.getElementById('history_chart'));
        chart.draw(data, options);
    }

    /**
     * Update the history chart.
     */
    var updateHistory = function(){
        $scope.loadingHistory = true

        var filters = {
            date: $scope.historyFilters,
            locality: $scope.locality
        }

        // We call the transaction service to retrieve the aggregate data
        TransactionService.getAggregates(
                filters, ["year", "month", "property_type"], [])
                .success(function(results){

            var raw = results.results

            if(raw && raw.length){
                $scope.showHistory = true
            
                // We need to process the data in a year/month array
                var processed = {}
                for(i in raw){
                    var year = raw[i].year
                    var month = raw[i].month
                    if (!(year in processed))
                        processed[year] = {}
                    if (!(month in processed[year]))
                        processed[year][month] = {}
                    processed[year][month][raw[i].property_type] = 
                        raw[i].price_avg / PRICE_DIVISOR
                }

                var propertyTypes = TransactionService.getPropertyType();
                var propertyTypeNames = [];
                var propertyTypeKeys = [];

                for(var key in propertyTypes){
                    propertyTypeNames.push(propertyTypes[key]);  
                    propertyTypeKeys.push(key);              
                }

                // Building the data object for the chart
                var data = new google.visualization.DataTable();
                data.addColumn('date', 'Date');
                for(i in  propertyTypeNames)
                    data.addColumn('number', propertyTypeNames[i]);                    
                rows = []
                for(year in processed){
                    for(month in processed[year]){
                        var priceAverages = processed[year][month]
                        var currentData = [new Date(year, month, 1)]
                        for(i in propertyTypeKeys)
                            currentData.push(priceAverages[propertyTypeKeys[i]])
                        rows.push(currentData)
                    }      
                }
                data.addRows(rows)
                drawHistory(data)
            
            }else{
                $scope.showHistory = false
            }

            $scope.loadingHistory = false

        }).error(function(results){
            $scope.loadingHistory = false
            $scope.showHistory = false

            alert("An unexpected error occured")
        });
    }

    /**
     * Draw the segmentation chart
     */
    var drawSegmentation = function(data){
        if(!chartsActive)
            return

        var data = google.visualization.arrayToDataTable(data);
        var options = {
            title: 'Transactions by Price Range (k£)',
            width: 800,
            height: 450,
            legend: {position: 'none'},       
        };

        var chart = new google.visualization.BarChart(
            document.getElementById('segmentation_chart'));

        chart.draw(data, options);        
    }

    /**
     * Update the segmentation chart
     */
    var updateSegmentation = function(){
        $scope.loadingSegmentation = true

        // We want to split the prices into 8 price range
        var BINS = 8
        var filters = {
            date: {
                from: $scope.segmentationFilters,
                to: $scope.segmentationFilters
            },
            locality: $scope.locality
        }

        TransactionService.getAggregates(filters, ["price_bin"], [BINS])
                .success(function(results){
            var data = [['Price Range', 'Number of transactions']]
            var raw = results.results

            if(raw && raw.length){
                $scope.showSegmentation = true

                min_price = raw[0].price_min
                max_price = raw[raw.length - 1].price_max
                interval = (min_price + max_price) / BINS

                // For each bin add the number of transaction or 0 if we 
                // don't have any
                var i = 0
                for(bin_index = 1; bin_index <= BINS; ++bin_index){
                    var low = Math.round(
                        (min_price + (bin_index - 1) * interval) / PRICE_DIVISOR)
                    var high = Math.round(
                        (min_price + bin_index * interval) / PRICE_DIVISOR)

                    if(raw[i].price_bin == bin_index){
                        data.push([low + " - " + high, raw[i].count])
                        i++
                    }else{
                        data.push([low + " - " + high, 0])
                    }

                }
                drawSegmentation(data)
            }else{
                $scope.showSegmentation = false
            }
            $scope.loadingSegmentation = false

        }).error(function(results){
            $scope.loadingSegmentation = false
            $scope.showSegmentation = false
            alert("An unexpected error occured")
        });
    }

    /**
     * Update both charts
     */
    $scope.updateCharts = function(){
        updateHistory()
        updateSegmentation()
    }

    /**
     * Whenever the filters changes, we update the relevant chart
     */
    $scope.$watch('historyFilters', function(newValue, oldValue){
        // Making sure that we have a valid date range
        var from = $scope.historyFilters.from
        var to =  $scope.historyFilters.to

        if(from.year > to.year)
            to.year = from.year

        if (from.year == to.year && from.month > to.month)
            to.month = from .month

        updateHistory()            
    }, true) 

    $scope.$watch('segmentationFilters', function(newValue, oldValue){
        updateSegmentation()
    }, true) 
}]);