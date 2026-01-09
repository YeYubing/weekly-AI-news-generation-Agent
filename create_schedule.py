#!/usr/bin/env python3
"""
创建每周自动运行的任务（用户级别，无需管理员权限）
"""

import os
from pathlib import Path
import plistlib

def create_launchd_plist():
    """为当前用户创建launchd任务"""
    
    # 获取当前用户和项目路径
    home = str(Path.home())
    project_path = home + "/Desktop/AI_Weekly_Reporter"
    script_path = project_path + "/run_weekly.command"
    
    # launchd plist内容
    plist_content = {
        'Label': 'com.user.aiweeklyreporter',
        'ProgramArguments': ['/bin/bash', script_path],
        'StartCalendarInterval': {
            'Weekday': 1,    # 周一 (0=周日, 1=周一, ..., 6=周六)
            'Hour': 9,       # 9点
            'Minute': 0      # 0分
        },
        'StandardOutPath': '/tmp/ai_reporter.log',
        'StandardErrorPath': '/tmp/ai_reporter_err.log',
        'RunAtLoad': False,
    }
    
    # 确保launch agents目录存在
    launch_agents_dir = home + "/Library/LaunchAgents"
    os.makedirs(launch_agents_dir, exist_ok=True)
    
    # 写入plist文件
    plist_file = launch_agents_dir + "/com.user.aiweeklyreporter.plist"
    
    with open(plist_file, 'wb') as f:
        plistlib.dump(plist_content, f)
    
    print(f"✅ 已创建计划任务配置文件: {plist_file}")
    print("\n📋 下一步操作:")
    print(f"1. 加载任务: launchctl load {plist_file}")
    print(f"2. 立即测试: launchctl start com.user.aiweeklyreporter")
    print(f"3. 查看日志: tail -f /tmp/ai_reporter.log")
    print(f"4. 卸载任务: launchctl unload {plist_file}")
    
    return plist_file

def main():
    print("📅 AI播报助手定时任务设置")
    print("=" * 50)
    
    # 确保脚本文件存在
    project_path = Path.home() / "Desktop/AI_Weekly_Reporter"
    run_script = project_path / "run_weekly.command"
    
    if not run_script.exists():
        # 创建自动运行脚本
        with open(run_script, 'w') as f:
            f.write('''#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 ai_reporter.py --quiet
''')
        
        # 添加执行权限
        os.chmod(run_script, 0o755)
        print(f"✅ 已创建运行脚本: {run_script}")
    
    # 创建launchd配置
    plist_file = create_launchd_plist()
    
    print("\n💡 重要提示:")
    print("• 此任务只在您登录时运行")
    print("• 不会在后台常驻")
    print("• 可以随时通过launchctl命令管理")
    print("• 所有文件都在您的用户目录，完全安全")
    
    # 询问是否立即加载
    choice = input("\n是否立即加载并启用定时任务？(y/n): ").strip().lower()
    
    if choice == 'y':
        os.system(f"launchctl load {plist_file}")
        print("✅ 定时任务已启用！每周一上午9点自动运行")
        print("💡 首次运行可能需要重启或重新登录")

if __name__ == "__main__":
    main()

