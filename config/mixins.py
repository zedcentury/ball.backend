from rest_framework.pagination import PageNumberPagination


class PaginationMixin:
    """
    Turn on or turn off pagination by query parameter 'pagination'
    """

    def list(self, request, *args, **kwargs):
        if request.query_params.get('pagination') == 'off':
            self.pagination_class = None
        else:
            self.pagination_class = PageNumberPagination
        return super().list(request, *args, **kwargs)
