import unittest
import socket

class TestEchoServer(unittest.TestCase):
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.SERVER_HOST, self.SERVER_PORT))
            s.sendall(request.encode())
            response = s.recv(4096)
        return response.decode()

    def test_simple_get_request(self):
        request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(self.SERVER_HOST)
        response = self.send_request(request)
        self.assertIn('HTTP/1.1 200 OK', response)
        self.assertIn('Request Method: GET', response)
        self.assertIn('Host: {}'.format(self.SERVER_HOST), response)

    def test_status_404(self):
        request = 'GET /?status=404 HTTP/1.1\r\nHost: {}\r\n\r\n'.format(self.SERVER_HOST)
        response = self.send_request(request)
        self.assertIn('HTTP/1.1 404 Not Found', response)
        self.assertIn('Request Method: GET', response)
        self.assertIn('Host: {}'.format(self.SERVER_HOST), response)

    def test_invalid_status(self):
        request = 'GET /?status=invalid HTTP/1.1\r\nHost: {}\r\n\r\n'.format(self.SERVER_HOST)
        response = self.send_request(request)
        self.assertIn('HTTP/1.1 200 OK', response)
        self.assertIn('Request Method: GET', response)
        self.assertIn('Host: {}'.format(self.SERVER_HOST), response)

    def test_custom_header(self):
        request = 'GET / HTTP/1.1\r\nHost: {}\r\nX-Custom-Header: test\r\n\r\n'.format(self.SERVER_HOST)
        response = self.send_request(request)
        self.assertIn('HTTP/1.1 200 OK', response)
        self.assertIn('X-Custom-Header: test', response)
        self.assertIn('Host: {}'.format(self.SERVER_HOST), response)

if __name__ == '__main__':
    unittest.main()
