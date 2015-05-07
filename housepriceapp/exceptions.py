from rest_framework import exceptions


class GroupByFieldError(exceptions.APIException):
    """
    This exception is raise when an attempt is made to group by an
    invalid field
    """
    status_code = 400
    default_detail = 'Group by field not allowed'
