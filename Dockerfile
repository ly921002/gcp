# 使用轻量级Alpine基础镜像
FROM alpine:3.18

# 设置工作目录
WORKDIR /app

# 复制GitHub代码到容器（包括二进制文件）
COPY . .
# RUN chmod +x /app/komari-agent

# 安装基础依赖
RUN apk update && \
    apk add --no-cache \
        bash \

    chmod +x main.sh && \
    chmod +x komari-agent && \

# 设置启动命令（根据项目调整）
CMD ["./main.sh"]
