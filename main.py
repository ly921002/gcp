import subprocess
import sys
import os

# 设置证书路径（根据你实际存放证书的位置修改）
cert_path = "/gcp.240713.xyz.crt"  # 替换为实际路径

# 设置环境变量来指定证书
env = os.environ.copy()
env['SSL_CERT_FILE'] = cert_path
env['REQUESTS_CA_BUNDLE'] = cert_path
    
# 定义命令参数
command = [
    "./komari-agent",  # 可执行文件路径（确保在相同目录或提供完整路径）
    "-e", "https://gcp.240713.xyz",
    "-t", "alorV4SEQjwJyCKEEYPuUO"
]

try:
    # 执行命令并实时打印输出
    result = subprocess.run(
        command,
        env=env,  # 使用自定义环境变量
        check=True,  # 检查命令是否成功
        text=True,   # 以文本形式捕获输出
        stdout=sys.stdout,  # 标准输出重定向到控制台
        stderr=sys.stderr   # 错误输出重定向到控制台
    )
except subprocess.CalledProcessError as e:
    print(f"命令执行失败，错误码: {e.returncode}")
except FileNotFoundError:
    print("错误：找不到 komari-agent 文件")
