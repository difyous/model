class RemoveServerHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Server'] = ' '
        return response
      
class XContentTypeOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        return response
class DisableHttpTraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'TRACE':
            return HttpResponseNotAllowed(['GET'])
        return self.get_response(request)

class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response should have Cache-Control header
        if self.should_set_cache_control(request):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

        return response

    def should_set_cache_control(self, request):
        # Define your criteria to determine if Cache-Control header should be set
        # For example, check the URL or some other condition
        if request.path.startswith('/assets/'):
            return True
        return False
class PermissionsPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Permissions-Policy'] = "geolocation 'none'; microphone 'none'; camera 'none'"
        return response
