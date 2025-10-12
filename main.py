import subprocess
import sys
import os
import stat

def set_executable_permission(file_path):
    """设置文件为可执行权限"""
    try:
        if os.path.exists(file_path):
            # 获取当前权限
            current_permissions = os.stat(file_path).st_mode
            # 添加执行权限（用户、组、其他）
            new_permissions = current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            os.chmod(file_path, new_permissions)
            print(f"已设置 {file_path} 为可执行文件")
            return True
        else:
            print(f"错误：文件 {file_path} 不存在")
            return False
    except Exception as e:
        print(f"设置权限时出错: {e}")
        return False

def get_command_from_env():
    """从环境变量构建命令"""
    # 从环境变量获取可执行文件路径，默认为当前目录下的 komari-agent
    agent_path = os.getenv('KOMARI_AGENT_PATH', './komari-agent')
    
    base_command = [agent_path]
    
    # 必需参数
    endpoint = os.getenv('KOMARI_ENDPOINT')
    token = os.getenv('KOMARI_TOKEN')
    
    if not endpoint or not token:
        raise ValueError("必需环境变量 KOMARI_ENDPOINT 或 KOMARI_TOKEN 未设置")
    
    # 添加参数
    base_command.extend(["-e", endpoint])
    base_command.extend(["-t", token])
    
    # 可选参数
    optional_params = {
        'KOMARI_PORT': '-p',
        'KOMARI_CONFIG': '-c',
        'KOMARI_LOGLEVEL': '--log-level'
    }
    
    for env_var, flag in optional_params.items():
        value = os.getenv(env_var)
        if value:
            base_command.extend([flag, value])
    
    return base_command, agent_path

def main():
    # 证书路径从环境变量读取
    cert_path = os.getenv('SSL_CERT_PATH', '/gcp.240713.xyz.crt')

    # 设置环境变量
    env = os.environ.copy()
    env['SSL_CERT_FILE'] = cert_path
    env['REQUESTS_CA_BUNDLE'] = cert_path

    try:
        # 构建命令
        command, agent_path = get_command_from_env()
        
        # 设置 komari-agent 为可执行文件
        if not set_executable_permission(agent_path):
            print("权限设置失败，程序退出")
            return
        
        print(f"执行命令: {' '.join(command)}")
        
        # 执行命令
        result = subprocess.run(
            command,
            env=env,
            check=True,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
    except ValueError as e:
        print(f"配置错误: {e}")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误码: {e.returncode}")
    except FileNotFoundError:
        print("错误：找不到 komari-agent 文件")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    main()
