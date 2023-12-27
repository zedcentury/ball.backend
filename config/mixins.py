from rest_framework.settings import api_settings


class PaginationMixin:
    """
    Turn on or turn off pagination by query parameter 'pagination'
    """

    def list(self, request, *args, **kwargs):
        if request.query_params.get('pagination') == 'off':
            self.pagination_class = None
        else:
            self.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        return super().list(request, *args, **kwargs)
