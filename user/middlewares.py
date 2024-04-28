class CheckCookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 查看發送的 Cookie
        print(request.COOKIES)

        return response