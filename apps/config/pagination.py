from django.core.paginator import Paginator, Page

class CustomPage(Page):
    def page_range_to_show(self, visible=5):
        total_pages = self.paginator.num_pages
        current_page = self.number
        half = visible // 2
        if total_pages <= visible:
            return list(self.paginator.page_range)
        start = max(current_page - half, 1)
        end = start + visible - 1
        if end > total_pages:
            end = total_pages
            start = max(end - visible + 1, 1)
        return list(range(start, end + 1))

class CustomPaginator(Paginator):
    def _get_page(self, *args, **kwargs):
        return CustomPage(*args, **kwargs)
