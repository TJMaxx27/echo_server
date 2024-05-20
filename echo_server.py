import socket
import urllib.parse
from http.server import BaseHTTPRequestHandler


def get_status_message(status_code):
    class HTTPStatusHelper(BaseHTTPRequestHandler):
        def __init__(self):
            self.requestline = ''
            self.request_version = 'HTTP/1.1'
            self.command = None
            self.status_code = status_code

        def send_response(self, code, message=None):
            if message is None:
                message = self.responses[code][0]
            self.send_response_only(code, message)

    helper = HTTPStatusHelper()
    return f"{status_code} {helper.responses[status_code][0]}"


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    request_lines = request_data.splitlines()

    if len(request_lines) > 0:
        request_line = request_lines[0]
        method, path, version = request_line.split()
        parsed_path = urllib.parse.urlparse(path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        status_code = 200
        status_message = "200 OK"
        if 'status' in query_params:
            try:
                status_code = int(query_params['status'][0])
                status_message = get_status_message(status_code)
            except (ValueError, KeyError):
                status_code = 200
                status_message = "200 OK"

        response_lines = [
            f"HTTP/1.1 {status_message}",
            f"Content-Type: text/plain; charset=utf-8",
            "",
            f"Request Method: {method}",
            f"Request Source: {client_socket.getpeername()}",
            f"Response Status: {status_message}",
        ]

        headers = {}
        for header_line in request_lines[1:]:
            if header_line.strip():
                key, value = header_line.split(":", 1)
                headers[key.strip()] = value.strip()

        for key, value in headers.items():
            response_lines.append(f"{key}: {value}")

        response_body = "\n".join(response_lines)
        response = f"{response_body}\n"

        client_socket.sendall(response.encode('utf-8'))
    client_socket.close()


def run_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        handle_request(client_socket)


if __name__ == "__main__":
    run_server()
