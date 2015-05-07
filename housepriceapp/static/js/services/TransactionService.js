housepriceApp.factory('TransactionService', ['$http', function ($http){

    var API_URL = location.protocol + "//" + location.host + "/api"
 
    var PROPERTY_TYPES = {
        'D': 'Detached',
        'S': 'Semi-Detached',
        'F': 'Flat',
        'T': 'Terraced'
    }

    var makeFilters = function(filters){
        var from = filters.date.from.year + "-" + filters.date.from.month + "-01"
        var to = filters.date.to.year + "-" + (filters.date.to.month + 1) + "-01"
        var date_query_params = "date_from=" + from + "&date_to=" + to
        var locality_query_params = "locality=" + filters.locality

        return locality_query_params + "&" + date_query_params
    }

    return {
        getPropertyType: function(){
            return PROPERTY_TYPES
        },
        getHistory: function(filters){

            var url = API_URL + "/transactions/aggregate/";
            var filters_query_params = makeFilters(filters)
            var groupby_query_params = "groupby=year"
                                       + "&groupby=month"
                                       + "&groupby=property_type"

            var query_params = "?" + groupby_query_params + "&" 
                                   + filters_query_params
            url += query_params
            return $http.get(url)
        },
        getSegmentation: function(filters, bins){
            var url = API_URL + "/transactions/aggregate/";
            var filters_query_params = makeFilters(filters)
            var groupby_query_params = "groupby=price_bin&bins=" + bins
            var query_params = "?" + groupby_query_params + "&" 
                                   + filters_query_params
            url += query_params
            return $http.get(url)

        }
    }
}]);