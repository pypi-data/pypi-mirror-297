import platform
import socket
import fileinput
import sys
from rich.console import Console
from rich.panel import Panel

# 创建一个 Console 对象
console = Console()


def get_hosts_file_path():
    system = platform.system()

    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system in ["Linux", "Darwin"]:  # macOS 和 Linux 使用相同的路径
        return "/etc/hosts"
    else:
        print("不支持的操作系统")
        sys.exit(1)


def get_ip_from_socket(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"查询失败: {e}")
        sys.exit(1)


def check_host_entry(hosts_file_path, txt):
    try:
        found = False
        with fileinput.input(hosts_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if '001.gov' in line:
                    print(txt)  # 替换整行
                    found = True
                else:
                    print(line, end='')  # 保持原行不变

        if not found:
            with open(hosts_file_path, 'a') as file:
                file.write(f"{txt}\n")
    except PermissionError:
        print("\n无权限，请使用管理员用户进行操作！Mac: `sudo updns` Win: `在具有管理员权限的终端下执行`")
        sys.exit(1)
    except Exception as e:
        print(f"\n读取 hosts 文件时出错: {e}")
        sys.exit(1)


def main():
    domain_to_lookup = "home.w0rk.top"
    hosts_file_path = get_hosts_file_path()
    ip = get_ip_from_socket(domain_to_lookup)
    txt = f"{ip}	001.gov"
    check_host_entry(hosts_file_path, txt)
    # 创建一个面板，将输出放入框中
    panel_content = f"hosts文件位置为: [cyan]{hosts_file_path}[/cyan]\n记录值  --> [yellow]{txt}[/yellow]"
    panel = Panel(panel_content, title="更新成功", title_align="center", border_style="green", width=50)
    # 输出面板
    console.print(panel)


if __name__ == '__main__':
    main()
