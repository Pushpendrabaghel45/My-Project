from django.shortcuts import redirect

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        print("inside __init__")
        self.get_response = get_response

    def __call__(self, request):
        print("inside __call__",request.path)
        if request.path.startswith('/dashboard/'):
            if not request.session.get('user_logged_in'):
                return redirect('/login/')


        # protected_paths = ['/dashboard/']

        # if request.path in protected_paths:
        #     print("inside if",request.session.get('user_logged_in'))
        #     if not request.session.get('user_logged_in'):
        #         return redirect('/login/')
        
        print("outside if")

        response = self.get_response(request)
        return response