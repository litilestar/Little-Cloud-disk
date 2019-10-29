import socket
import re

def service(client_socket):

    # 7. TODO 请求行  GET /login.html HTTP/1.1
    recv_data = client_socket.recv(1024).decode("utf-8")
    request_list = recv_data.splitlines()
    print("---------请求列表-------")
    print( request_list)
    print()

    # 8. TODO 正则匹配目录名,第一个字母不是/,从/最后一个不是空格,匹配第一次出现的
    match_ret = re.match(r"[^/]+([^ ]*)", request_list[0])
    print("-----目录名-------", match_ret.group(1))
    file_name = match_ret.group(1)
    # 10. 如果输入 127.0.0.1:7890,设置默认页面/index.html
    if match_ret:
        if file_name == "/":
            file_name = "/index.html"

    # 9. 读取HTML页面信息,返回给浏览器
    # 11. 如果输入页面不存在,提示404  NOT FOUND
    try:
        f = open("../day9-HTTP协议、http服务器的实现-1/html" + file_name, "rb")
    except:
        # TODO 响应行 HTTP/1.1 404 NOT FOUND
        response_header = "HTTP/1.1 404 NOT FOUND\r\n" + "\r\n"
        response_body = "--------------not found ------------"
        client_socket.send(response_header.encode("utf-8") + response_body.encode("utf-8"))
        client_socket.close()
    else:
        response_body = f.read()
        f.close()
        # TODO 12. 使用长连接,连接一次,请求响应多次,客户端自动关闭
        # TODO 响应行 HTTP/1.1 200 OK
        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"
        client_socket.send(response_header.encode("utf-8") + response_body)

        # TODO ??用了长连接,有时候网页一直打转,有的加载很快
        # client_socket.close()


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