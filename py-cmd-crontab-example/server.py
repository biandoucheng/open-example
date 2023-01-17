from http.server import HTTPServer,BaseHTTPRequestHandler

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        健康检测接口
        """
        self.send_response(200)
        self.send_header('Content_type','text/plain;charset=utf-8')
        self.end_headers()
        self.wfile.write('ok\n'.encode())

def run():
    """
    启动服务占据窗口
    """
    port = 8000
    address = ('',port)
    httpd = HTTPServer(address, HealthCheck)
    httpd.serve_forever()
    print("Continuous task server started .")

#启动
run()