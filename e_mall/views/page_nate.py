from django.core.paginator import Paginator

def pagey(results_item, request_item):
    paginator = Paginator(results_item, per_page=54, orphans=5)
    page = request_item.GET.get('page')
    results_item = paginator.get_page(page)
    return results_item

def intpagey(results_item, request_item):
    paginator = Paginator(results_item, per_page=50, orphans=0)
    page = request_item.GET.get('page')
    results_item = paginator.get_page(page)
    return results_item