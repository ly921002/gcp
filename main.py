import subprocess
import sys
import os

def main():
    # 设置证书环境变量
    cert_path = os.getenv('SSL_CERT_PATH', '/gcp.240713.xyz.crt')
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    
    # 设置 komari-agent 为 777 权限
    agent_path = './komari-agent'
    try:
        os.chmod(agent_path, 0o777)
        print(f"已设置 {agent_path} 为可执行文件")
    except Exception as e:
        print(f"权限设置警告: {e}")
    
    # 构建命令
    command = [
        agent_path,
        "-e", os.getenv('KOMARI_ENDPOINT', 'https://gcp.240713.xyz'),
        "-t", os.getenv('KOMARI_TOKEN', 'QlVjtgwxsl3ZwwX0CugyH4')
    ]
    
    # 执行命令
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误码: {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("错误：找不到 komari-agent 文件")
        sys.exit(1)

if __name__ == "__main__":
    main()
