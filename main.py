import subprocess
import sys
import os

def main():
    # 从环境变量 SSL_CERT_FILE 读取证书路径
    cert_path = os.getenv('SSL_CERT_FILE', 'gcp.240713.xyz.crt')
    
    # 设置环境变量
    env = os.environ.copy()
    env['SSL_CERT_FILE'] = cert_path
    env['REQUESTS_CA_BUNDLE'] = cert_path
    
    # 设置 komari-agent 为 755 权限
    agent_path = 'komari-agent'
    try:
        os.chmod(agent_path, 0o755)
        print(f"已设置 {agent_path} 为可执行文件")
    except Exception as e:
        print(f"权限设置警告: {e}")
    
    # 构建命令
    command = [
        agent_path,
        "-e", os.getenv('KOMARI_ENDPOINT', 'https://gcp.240713.xyz'),
        "-t", os.getenv('KOMARI_TOKEN', 'rP6F8lvOgWZXViUxnmDq1I')
    ]
    
    # 执行命令
    try:
        result = subprocess.run(
            command,
            env=env,  # 传递自定义环境变量
            check=True,
            text=True,
            capture_output=True,  # 关键：捕获完整输出
            encoding='utf-8'      # 明确指定编码
        )
    except subprocess.CalledProcessError as e:
        # 增强错误诊断
        print(f"\n❌ 命令执行失败 (错误码: {e.returncode})")
        print(f"► 执行的命令: {' '.join(e.cmd)}")
        
        if e.stdout:
            print("\n[标准输出]:")
            print(e.stdout.strip())
        
        if e.stderr:
            print("\n[错误输出]:")
            print(e.stderr.strip())
        
        sys.exit(e.returncode)
    else:
        # 成功时处理输出
        print(result.stdout)

if __name__ == "__main__":
    main()
