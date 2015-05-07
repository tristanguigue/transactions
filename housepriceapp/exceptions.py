from rest_framework import exceptions


class GroupByFieldError(exceptions.APIException):
    """
    This exception is raise when an attempt is made to group by an
    invalid field
    """
    status_code = 400
    default_detail = 'Group by field not allowed'


class NoDataError(exceptions.APIException):
    """
    This exception is raise when an attempt is made to group by bins but
    there are is no data available
    """
    status_code = 204
    default_detail = 'No data to perform group by bin'
