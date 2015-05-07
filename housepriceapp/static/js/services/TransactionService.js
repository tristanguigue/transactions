/**
 * The service to access the server data
 */
housepriceApp.factory('TransactionService', ['$http', function ($http){

    var API_URL = location.protocol + "//" + location.host + "/api"
 
    var PROPERTY_TYPES = {
        'D': 'Detached',
        'S': 'Semi-Detached',
        'F': 'Flat',
        'T': 'Terraced'
    }

    /**
     * Build the filter query param
     * @param {object} filters The filters data 
     * @return {string} the query string
     */
    var makeFilters = function(filters){
        var ret = ''

        if('date' in filters){
            var from = filters.date.from.year + "-" + filters.date.from.month + "-01"
            // We extend the date range to the next month
            if(filters.date.to.month < 12){
                month_to = filters.date.to.month + 1
                year_to = filters.date.to.year
            }
            else{
                month_to = 1
                year_to = filters.date.to.year + 1            
            }

            var to = year_to + "-" + month_to + "-01"
            ret += "date_from=" + from + "&date_to=" + to  
        }
        if('locality' in filters)
            if(ret)
                ret +=  "&"
            ret += "locality=" + filters.locality

        return ret
    }

    /**
     * Build the query array of parameters
     * @param {string} name The name of the key
     * @param {array} values The list of values to be set
     * @return {string} the query string
     */
    var makeQueryParams = function(name, values){
        var ret = ""
        for(i in values){
            if(ret)
                ret += "&"
            ret += name + "=" + values[i]
        }
        return ret
    }

    return {
        getPropertyType: function(){
            return PROPERTY_TYPES
        },
        /**
         * Retrieve the aggregate data for the transactions
         * @param {object} filters The filters to be applied
         * @param {object} groupbys The field we'll use to group the data
         * @param {object} bins The optional bins to group the data
         * @return {object} the http promise
         */
        getAggregates: function(filters, groupbys, bins){
            var url = API_URL + "/transactions/aggregate/";

            var filters_query_params = makeFilters(filters)
            var groupby_query_params = makeQueryParams("groupby", groupbys)
            var bins_query_params = makeQueryParams("bins", bins)

            var query_params = ""

            if(filters_query_params)
                query_params += filters_query_params

            if(groupby_query_params)
                if(query_params)
                    query_params += "&"
                query_params += groupby_query_params

            if(bins_query_params)
                if(query_params)
                    query_params += "&"
                query_params += bins_query_params

            url += "?" + query_params

            return $http.get(url)

        }
    }
}]);