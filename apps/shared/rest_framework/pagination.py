from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_query_param = 'page_size'
