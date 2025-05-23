from django.http import HttpResponse

def home(request):
    """
    Simple homepage view to verify the site is running.
    """
    return HttpResponse(
        "<h1>Face Value</h1><p>The site is up and running!</p>",
        content_type="text/html",
    )