# -*- coding: UTF-8 -*-
"""
LLM 漏洞验证服务器（调试版）
功能：通过监听指定端口接收请求，检测SSRF/命令注入/XSS等漏洞，并将漏洞信息记录到文件中
"""

import os
import re
import socket
import argparse
from datetime import datetime

# 定义待检测的漏洞类型列表
RequestVulnerabilityList = ["ssrf", "command_injection", "xss"]

def create_verification_server(server_ip="127.0.0.1", server_port=4444):
    """
    创建验证服务端Socket
    :param server_ip: 绑定IP地址，默认127.0.0.1
    :param server_port: 监听端口号，默认4444
    :return: 配置好的socket对象
    """
    verification_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    verification_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口复用
    try:
        verification_server.bind((server_ip, server_port))
        verification_server.listen(4)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Server started on {server_ip}:{server_port}")
        return verification_server
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to start server: {e}")
        raise

def vul_verification(verification_server, vul_dir):
    """
    漏洞验证主逻辑（调试增强版）
    :param verification_server: 已创建的socket服务器对象
    :param vul_dir: 漏洞信息存储目录
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Waiting for connections...")
    while True:
        socket_conn = None
        try:
            # 接受客户端连接
            socket_conn, client_addr = verification_server.accept()
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New connection from {client_addr}")
            
            # 设置接收超时（5秒）
            socket_conn.settimeout(5.0)
            
            # 接收请求数据
            socket_data = socket_conn.recv(1024).decode('utf-8', errors='ignore')
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received {len(socket_data)} bytes:")
            print("="*40)
            print(socket_data)
            print("="*40)
            
            if not socket_data:
                print("[DEBUG] Received empty data, closing connection")
                continue
                
            # 调试输出原始数据
            with open(os.path.join(vul_dir, "raw_requests.log"), "a+") as log:
                log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {client_addr}\n")
                log.write(socket_data + "\n" + "="*40 + "\n")
            
            # 遍历漏洞类型进行检测
            detected = False
            for RequestVulnerability in RequestVulnerabilityList:
                print(f"[DEBUG] Checking for {RequestVulnerability}...")
                if RequestVulnerability in socket_data.lower():  # 改为小写匹配更灵活
                    print(f"\n[!] VULNERABILITY DETECTED: {RequestVulnerability.upper()}")
                    
                    # 提取漏洞信息
                    try:
                        http_pos = socket_data.find(" HTTP/")
                        vul_start = socket_data.find(RequestVulnerability)
                        
                        if http_pos > 0 and vul_start > 0:
                            vul_filename = socket_data[vul_start+len(RequestVulnerability):http_pos].strip()
                            print(f"[DEBUG] Extracted vulnerability data: {vul_filename}")
                            
                            # 创建漏洞目录
                            vul_output_dir = os.path.join(vul_dir, RequestVulnerability) + "/"
                            os.makedirs(vul_output_dir, exist_ok=True)
                            
                            # 构造报告内容
                            vul_api_content = f"""-------- LLM Vul API --------
Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Client Address: {client_addr}
API Vul Type: {RequestVulnerability}
Vul API Url: {vul_filename[:vul_filename.find("LLM")] if "LLM" in vul_filename else vul_filename}
API Vul Param: {vul_filename[vul_filename.find("LLM")+3:] if "LLM" in vul_filename else "N/A"}
Full Request:
{socket_data}
"""
                            print(f"[DEBUG] Report content:\n{vul_api_content}")
                            
                            # 处理文件名
                            safe_filename = re.sub(r'[<>:"/\\|?*]', '@', 
                                                 vul_filename.replace("/", "!")[:50])  # 限制文件名长度
                            
                            # 写入文件
                            report_path = os.path.join(vul_output_dir, f"{safe_filename}.txt")
                            with open(report_path, "a+") as f:
                                f.write(vul_api_content)
                            print(f"[+] Report saved to {report_path}")
                            
                            detected = True
                            break
                    except Exception as e:
                        print(f"[!] Error processing vulnerability: {e}")
                        continue
            
            if not detected:
                print("[DEBUG] No vulnerabilities detected in this request")
                
        except socket.timeout:
            print("[DEBUG] Socket timeout, closing connection")
        except Exception as e:
            print(f"[!] Error: {type(e).__name__}: {e}")
        finally:
            if socket_conn:
                socket_conn.close()
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connection closed")

if __name__ == '__main__':
    # 命令行参数解析配置
    parser = argparse.ArgumentParser(description="LLM Vulnerability Verification Server (Debug Mode)")
    parser.add_argument('--verification_server_ip', 
                       help='验证服务器监听IP（默认：127.0.0.1）', 
                       type=str, 
                       default="127.0.0.1")
    parser.add_argument('--verification_server_port', 
                       help='验证服务器监听端口（默认：4444）', 
                       type=int, 
                       default=4444)
    parser.add_argument('--output', 
                       help='漏洞报告存储绝对路径（默认当前目录）', 
                       type=str, 
                       default="./")
    args = parser.parse_args()
    
    # 处理输出目录
    output_dir = os.path.abspath(args.output)
    if not output_dir.endswith(os.sep):
        output_dir += os.sep
    
    # 创建漏洞存储目录
    vul_dir = os.path.join(output_dir, "vul")
    os.makedirs(vul_dir, exist_ok=True)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Output directory: {vul_dir}")
    
    # 启动验证服务
    try:
        verification_server = create_verification_server(
            args.verification_server_ip, 
            args.verification_server_port
        )
        vul_verification(verification_server, vul_dir)
    except KeyboardInterrupt:
        print("\n[!] Server stopped by user")
    except Exception as e:
        print(f"[!] Fatal error: {e}")
    finally:
        if 'verification_server' in locals():
            verification_server.close()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Server shutdown")