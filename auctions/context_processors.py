from .models import Listing

def add_variable_to_context(request):
    return {
        "categories": dict(sorted(Listing.CATEGORIES.items()))
    }