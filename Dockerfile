# 使用官方Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制GitHub代码到容器（包括二进制文件）
COPY . .

# 安装依赖（可选：编译二进制依赖）
RUN apt-get update && apt-get install -y build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential && apt-get autoremove -y

# 设置启动命令（根据项目调整）
CMD ["python", "main.py"]
