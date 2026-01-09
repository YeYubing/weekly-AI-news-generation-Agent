#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS AI Weekly Reporter - 完全安全的AI信息播报助手
所有文件都在桌面项目文件夹中，不影响系统
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 使用Python内置库，无需安装额外依赖
import urllib.request
import urllib.error
from xml.etree import ElementTree

class DesktopAIReporter:
    """桌面版AI播报助手"""
    
    def __init__(self):
        # 获取桌面路径
        desktop = Path.home() / "Desktop"
        self.project_folder = desktop / "AI_Weekly_Reporter"
        
        # 创建子文件夹
        self.data_folder = self.project_folder / "data"
        self.reports_folder = self.project_folder / "reports"
        self.data_folder.mkdir(exist_ok=True)
        self.reports_folder.mkdir(exist_ok=True)
        
        print("=" * 60)
        print("🤖 桌面AI播报助手 v1.0")
        print("=" * 60)
        print(f"📁 项目位置: {self.project_folder}")
        print("✅ 所有文件都保存在桌面上，不影响系统")
        print("=" * 60)
    
    def get_ai_news(self):
        """获取AI相关新闻"""
        try:
            # 使用多个RSS源
            sources = [
                "https://hnrss.org/newest?q=AI",
                "https://hnrss.org/newest?q=machine+learning",
            ]
            
            all_news = []
            for source in sources:
                try:
                    response = urllib.request.urlopen(source, timeout=10)
                    data = response.read()
                    root = ElementTree.fromstring(data)
                    
                    for item in root.findall('.//item')[:3]:
                        title_elem = item.find('title')
                        link_elem = item.find('link')
                        
                        if title_elem is not None and link_elem is not None:
                            all_news.append({
                                'title': title_elem.text[:100] if title_elem.text else '',
                                'link': link_elem.text,
                                'source': 'Hacker News',
                                'time': datetime.now().strftime('%H:%M')
                            })
                            
                except Exception as e:
                    print(f"  警告: {source} 获取失败")
                    continue
            
            return all_news[:5]  # 最多返回5条
            
        except Exception as e:
            print(f"获取新闻时出错: {e}")
            return []
    
    def get_github_trending(self):
        """获取GitHub趋势项目"""
        try:
            # GitHub搜索API
            url = "https://api.github.com/search/repositories?q=artificial+intelligence&sort=stars&order=desc&per_page=3"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'macOS-AI-Reporter')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                repos = []
                for item in data.get('items', []):
                    repos.append({
                        'name': item.get('name', ''),
                        'full_name': item.get('full_name', ''),
                        'stars': item.get('stargazers_count', 0),
                        'url': item.get('html_url', ''),
                        'description': item.get('description', '')[:80] if item.get('description') else ''
                    })
                
                return repos
                
        except Exception as e:
            print(f"获取GitHub项目失败: {e}")
            return []
    
    def create_report(self):
        """创建报告"""
        print("\n📡 正在获取最新AI信息...")
        print("-" * 40)
        
        # 获取数据
        news = self.get_ai_news()
        repos = self.get_github_trending()
        
        # 构建报告内容
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append(f"🤖 AI发展周报 - {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        report_lines.append("=" * 60)
        report_lines.append("📍 数据来源: Hacker News, GitHub")
        report_lines.append("")
        
        # 新闻部分
        if news:
            report_lines.append("📰 最新AI动态:")
            for i, item in enumerate(news, 1):
                report_lines.append(f"{i}. {item['title']}")
                report_lines.append(f"   链接: {item['link']}")
            report_lines.append("")
        else:
            report_lines.append("📰 最新AI动态: (暂时无法获取)")
            report_lines.append("")
        
        # GitHub项目
        if repos:
            report_lines.append("💻 GitHub热门项目:")
            for i, repo in enumerate(repos, 1):
                report_lines.append(f"{i}. {repo['full_name']}")
                report_lines.append(f"   ⭐ {repo['stars']} stars")
                if repo['description']:
                    report_lines.append(f"   📝 {repo['description']}")
                report_lines.append(f"   🔗 {repo['url']}")
            report_lines.append("")
        else:
            report_lines.append("💻 GitHub热门项目: (暂时无法获取)")
            report_lines.append("")
        
        # 统计信息
        report_lines.append("📊 统计信息:")
        report_lines.append(f"   • 新闻数量: {len(news)} 条")
        report_lines.append(f"   • 开源项目: {len(repos)} 个")
        report_lines.append(f"   • 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("💡 提示:")
        report_lines.append("   1. 每周运行一次获取最新信息")
        report_lines.append("   2. 所有文件保存在桌面项目文件夹")
        report_lines.append("   3. 可手动删除不需要的报告")
        report_lines.append("=" * 60)
        
        report_content = "\n".join(report_lines)
        return report_content
    
    def save_report(self, content):
        """保存报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"AI_Report_{timestamp}.txt"
        filepath = self.reports_folder / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 报告已保存: {filepath}")
            
            # 同时保存一份到桌面方便查看
            desktop_file = Path.home() / "Desktop" / f"AI周报_{timestamp}.txt"
            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 桌面副本: {desktop_file}")
            
            return filepath
            
        except Exception as e:
            print(f"保存报告失败: {e}")
            return None
    
    def cleanup_old_reports(self, keep_days=30):
        """清理旧报告"""
        try:
            now = time.time()
            deleted_count = 0
            
            for report_file in self.reports_folder.glob("*.txt"):
                file_age = now - report_file.stat().st_mtime
                if file_age > keep_days * 86400:  # 超过指定天数
                    report_file.unlink()
                    deleted_count += 1
            
            if deleted_count > 0:
                print(f"🧹 已清理 {deleted_count} 个旧报告文件")
                
        except Exception as e:
            print(f"清理文件时出错: {e}")
    
    def run(self):
        """运行播报器"""
        try:
            # 清理旧报告
            self.cleanup_old_reports()
            
            # 创建报告
            report = self.create_report()
            
            # 显示报告
            print("\n" + report)
            
            # 保存报告
            save = input("\n💾 是否保存报告？(y/n): ").strip().lower()
            if save == 'y':
                self.save_report(report)
                print("\n🎉 报告生成完成！")
                print(f"📁 所有文件都保存在: {self.project_folder}")
            else:
                print("\n📝 报告已显示但未保存")
            
            # 询问是否设置定时
            self.setup_schedule_option()
            
        except KeyboardInterrupt:
            print("\n\n👋 操作已取消")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            sys.exit(1)
    
    def setup_schedule_option(self):
        """提供定时运行选项"""
        print("\n" + "=" * 60)
        print("⏰ 定时运行选项")
        print("=" * 60)
        print("您可以选择每周自动运行一次此程序")
        print("")
        print("有两种方式:")
        print("1. 使用macOS自带的日历提醒 (推荐，最安全)")
        print("2. 使用launchd (用户级别，无需管理员权限)")
        print("")
        
        choice = input("是否设置定时运行？(y/n): ").strip().lower()
        
        if choice == 'y':
            print("\n📅 设置方法:")
            print("")
            print("方法1 - 使用日历:")
            print("   1. 打开'日历'应用")
            print("   2. 创建新事件")
            print("   3. 重复: 每周")
            print("   4. 提醒: 执行脚本")
            print("   5. 脚本路径: " + str(self.project_folder / "run_weekly.command"))
            print("")
            print("方法2 - 使用终端命令:")
            print("   运行以下命令创建每周任务:")
            print(f"   cd '{self.project_folder}' && python3 create_schedule.py")
            print("")
            
            # 创建运行脚本
            self.create_run_script()

    def create_run_script(self):
        """创建运行脚本"""
        # 创建启动脚本
        script_content = '''#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 ai_reporter.py --auto
'''
        
        script_file = self.project_folder / "run_weekly.command"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 添加执行权限
        import os
        os.chmod(script_file, 0o755)
        
        print(f"📜 已创建运行脚本: {script_file}")
        print("💡 双击此文件即可运行播报器")

def main():
    """主函数"""
    print("🚀 启动桌面AI播报助手...")
    
    # 检查是否在虚拟环境中
    if sys.prefix == sys.base_prefix:
        print("⚠️  建议在虚拟环境中运行")
        print("   请执行: source venv/bin/activate")
        print("   或直接双击 run.command 文件")
    
    # 创建并运行播报器
    reporter = DesktopAIReporter()
    reporter.run()

if __name__ == "__main__":
    main()
