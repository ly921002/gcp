# 使用轻量级基础镜像
FROM alpine:3.18

# 安装bash（Alpine默认只有sh）
RUN apk add --no-cache bash

# 设置工作目录
WORKDIR /app

# 复制应用程序文件
COPY komari-agent .
COPY main.sh .

# 复制证书文件
RUN mkdir -p /app/certs
COPY gcp.240713.xyz.crt /app/certs/server.crt

# 调试：检查文件是否存在
RUN ls -la /app/

# 设置执行权限
RUN chmod +x komari-agent main.sh

# 检查文件内容
RUN cat main.sh || echo "无法读取main.sh"

# 设置环境变量
ENV ENDPOINT="https://gcp.240713.xyz" \
    TOKEN="rP6F8lvOgWZXViUxnmDq1I" \
    SSL_CERT_FILE="/app/certs/server.crt"

# 使用shell形式确保文件存在
CMD ["/bin/bash", "./main.sh"]
