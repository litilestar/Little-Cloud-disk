import socket

def service(client_socket):

    recv_data = client_socket.recv(1024).decode("utf-8")



    # 读取HTML页面信息,返回给浏览器
    f = open("../day9-HTTP协议、http服务器的实现-1/html/index.html", "rb")
    response_body = f.read()
    f.close()

    response_header = "HTTP/1.1 200 OK\r\n" + "\r\n"
    client_socket.send(response_header.encode("utf-8") + response_body)


    client_socket.close()


def main():
    # 1. 创建
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 2. bind
    tcp_socket.bind(("", 7890))
    # 3. lisetn
    tcp_socket.listen(128)
    # 4. accept
    while True:
        client_socket, client_addr = tcp_socket.accept()
        # 5. 服务
        service(client_socket)

    # 6. 关闭套接字
    tcp_socket.close()


if __name__ == '__main__':
    main()