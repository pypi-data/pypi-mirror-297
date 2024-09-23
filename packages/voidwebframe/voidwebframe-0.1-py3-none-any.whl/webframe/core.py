class VoidWebFrame:
    def __init__(self):
        self.routes = {}
    
    def route(self, path):
        def wrapper(func):
            self.routes[path] = func
            return func
        return wrapper
    
    def handle_request(self, path):
        if path in self.routes:
            response = self.routes[path]()
            return self.create_response(response)
        else:
            return self.create_response("404 Not Found", 404)
        
    def create_response(self, body, status=200):
        return f"HTTP/1.1 {status} OK\N\N{body}"