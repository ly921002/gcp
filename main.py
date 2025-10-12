import subprocess
import sys
import os
import stat

def debug_file_info(file_path):
    """详细调试文件信息"""
    print("=== 文件调试信息 ===")
    print(f"文件路径: {file_path}")
    print(f"文件存在: {os.path.exists(file_path)}")
    print(f"绝对路径: {os.path.abspath(file_path)}")
    
    if os.path.exists(file_path):
        st = os.stat(file_path)
        print(f"文件权限: {oct(st.st_mode)}")
        print(f"文件大小: {st.st_size} 字节")
        print(f"文件所有者: {st.st_uid}:{st.st_gid}")
        
        # 检查是否可执行
        print(f"当前用户可执行: {os.access(file_path, os.X_OK)}")
        print(f"当前用户可读: {os.access(file_path, os.R_OK)}")
        print(f"当前用户可写: {os.access(file_path, os.W_OK)}")
    
    print(f"当前工作目录: {os.getcwd()}")
    print(f"目录内容: {os.listdir('.')}")
    print("===================")

def main():
    # 使用绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agent_path = os.path.join(base_dir, "komari-agent")
    
    # 调试信息
    debug_file_info(agent_path)
    
    # 如果文件不存在，尝试其他可能的位置
    if not os.path.exists(agent_path):
        print("尝试在其他位置查找 komari-agent...")
        possible_paths = [
            "/app/komari-agent",
            "/usr/local/bin/komari-agent", 
            "./komari-agent",
            "komari-agent"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                agent_path = path
                print(f"找到文件: {agent_path}")
                break
    
    if not os.path.exists(agent_path):
        print("错误：找不到 komari-agent 文件")
        sys.exit(1)
    
    # 尝试设置权限
    try:
        os.chmod(agent_path, 0o777)
        print(f"已设置权限: {oct(os.stat(agent_path).st_mode)}")
    except Exception as e:
        print(f"设置权限失败: {e}")
    
    # 证书路径
    cert_path = os.getenv('SSL_CERT_PATH', '/gcp.240713.xyz.crt')
    
    # 设置环境变量
    env = os.environ.copy()
    env['SSL_CERT_FILE'] = cert_path
    env['REQUESTS_CA_BUNDLE'] = cert_path
    
    # 构建命令
    endpoint = os.getenv('KOMARI_ENDPOINT', 'https://gcp.240713.xyz')
    token = os.getenv('KOMARI_TOKEN', 'alorV4SEQjwJyCKEEYPuUO')
    
    command = [agent_path, "-e", endpoint, "-t", token]
    
    print(f"执行命令: {' '.join(command)}")
    
    try:
        # 方法1：直接执行
        result = subprocess.run(
            command,
            env=env,
            check=True,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    except PermissionError:
        print("直接执行失败，尝试方法2...")
        try:
            # 方法2：使用shell执行
            shell_command = f"'{agent_path}' -e '{endpoint}' -t '{token}'"
            result = subprocess.run(
                shell_command,
                env=env,
                check=True,
                text=True,
                stdout=sys.stdout,
                stderr=sys.stderr,
                shell=True
            )
        except Exception as e:
            print(f"方法2失败: {e}")
            # 方法3：尝试使用bash直接执行
            try:
                result = subprocess.run(
                    ["bash", "-c", f"'{agent_path}' -e '{endpoint}' -t '{token}'"],
                    env=env,
                    check=True,
                    text=True,
                    stdout=sys.stdout,
                    stderr=sys.stderr
                )
            except Exception as e:
                print(f"所有方法都失败: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()
