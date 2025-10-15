# 使用轻量级基础镜像
FROM alpine:3.18

# 设置工作目录
WORKDIR /app

# 复制应用程序文件
COPY komari-agent .
COPY main.sh .
# 复制证书文件 - 使用英文文件名
RUN mkdir -p /app/certs
COPY gcp.240713.xyz.crt /app/certs/server.crt
ENV SSL_CERT_FILE="/app/certs/server.crt"

# 创建日志目录
RUN mkdir -p /var/log

# 设置执行权限
RUN chmod +x komari-agent main.sh

# 设置默认环境变量（可在运行时覆盖）
ENV ENDPOINT="https://gcp.240713.xyz" \
    TOKEN="rP6F8lvOgWZXViUxnmDq1I" \
    SSL_CERT_FILE="/app/certs/server.crt"

# 指定容器启动命令
CMD ["./main.sh"]
