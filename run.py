# 简化版Airtest测试框架执行入口
import os
import sys
import argparse
import subprocess
import time
import shutil
import html

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 目录配置
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
REPORT_DIR = os.path.join(PROJECT_ROOT, "report")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")


# ----------------------------- 环境检查 -----------------------------
def check_environment():
    """启动前检查 airtest 与 adb 是否可用，给出友好提示。"""
    issues = []

    # 检查 airtest 是否安装
    try:
        result = subprocess.run(
            [sys.executable, "-m", "airtest", "--help"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            issues.append("❌ airtest 模块不可用，请执行: pip install -r requirements.txt")
    except Exception as e:
        issues.append(f"❌ airtest 检查失败: {e}")

    # 检查 adb 是否可用（仅 Android 用例需要，缺失时只是警告）
    if shutil.which("adb") is None:
        print("⚠️  未在 PATH 中找到 adb，若要跑 Android 用例请先安装 Android Platform Tools。")
    else:
        try:
            result = subprocess.run(
                ["adb", "devices"], capture_output=True, text=True, timeout=10
            )
            lines = [l for l in result.stdout.strip().splitlines()[1:] if l.strip()]
            connected = [l for l in lines if "device" in l and "offline" not in l]
            if not connected:
                print("⚠️  adb 未检测到已连接的设备，请检查 USB 调试是否开启。")
            else:
                print(f"✅ 已检测到 {len(connected)} 台 Android 设备：")
                for l in connected:
                    print(f"   - {l}")
        except Exception as e:
            print(f"⚠️  执行 adb devices 失败: {e}")

    if issues:
        for msg in issues:
            print(msg)
        return False
    return True


# ----------------------------- 用例执行 -----------------------------
def run_test(script_path, report_name, device="Android:///"):
    """运行单个测试脚本，返回 (returncode, report_path) 元组。"""
    print(f"▶️  运行测试脚本: {script_path}")

    # 改进 #1：每个用例独立的日志子目录，避免批量执行时相互覆盖
    log_dir = os.path.join(LOGS_DIR, report_name)
    os.makedirs(log_dir, exist_ok=True)

    # 构建命令（使用Python运行airtest模块）
    cmd = [
        sys.executable, "-m", "airtest", "run", script_path,
        "--device", device,
        "--log", log_dir,
    ]

    try:
        # 实时打印输出，长用例不再"假死"
        process = subprocess.Popen(
            cmd, cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace"
        )
        for line in process.stdout:
            print(line, end="")
        returncode = process.wait()
        print(f"测试执行完成，返回码: {returncode}")

        # 生成报告（基于该用例独立日志目录）
        report_path = generate_report(script_path, report_name, log_dir)

        return returncode, report_path
    except Exception as e:
        print(f"执行测试失败: {str(e)}")
        return 1, None


def generate_report(script_path, report_name, log_dir):
    """生成测试报告，返回报告文件路径。"""
    report_path = os.path.join(REPORT_DIR, f"{report_name}.html")
    print(f"📝 生成测试报告: {report_path}")

    cmd = [
        sys.executable, "-m", "airtest", "report", script_path,
        "--log_root", log_dir,
        "--outfile", report_path,
        "--lang", "zh",
    ]

    try:
        result = subprocess.run(
            cmd, cwd=PROJECT_ROOT,
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  报告生成失败: {result.stderr}")
            return None

        print(f"✅ 测试报告已生成: {report_path}")
        return report_path
    except Exception as e:
        print(f"生成报告失败: {str(e)}")
        return None


# ----------------------------- 用例发现 -----------------------------
def discover_scripts():
    """
    改进 #3：扫描 scripts/ 目录，优先收录 .air 工程包，
    避免 .air/ 目录与其内部 .py 同时被收录导致的重复执行。
    """
    scripts = []
    if not os.path.isdir(SCRIPTS_DIR):
        return scripts

    for entry in sorted(os.listdir(SCRIPTS_DIR)):
        full = os.path.join(SCRIPTS_DIR, entry)
        if os.path.isdir(full) and entry.endswith(".air"):
            scripts.append(full)
        elif os.path.isfile(full) and entry.endswith(".py"):
            # 仅当不是某个 .air 包内文件时收录
            scripts.append(full)
    return scripts


# ----------------------------- 汇总报告 -----------------------------
def generate_summary(results, summary_path):
    """
    改进 #5：生成一个总览 index.html，列出所有用例的结果与报告链接。
    results: List[dict(name, status, report, duration)]
    """
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    rows = []
    for r in results:
        status_color = "#28a745" if r["status"] == "PASS" else "#dc3545"
        report_link = (
            f'<a href="{html.escape(os.path.basename(r["report"]))}" target="_blank">查看</a>'
            if r.get("report") else "—"
        )
        rows.append(f"""
        <tr>
            <td>{html.escape(r["name"])}</td>
            <td style="color:{status_color};font-weight:bold;">{r["status"]}</td>
            <td>{r["duration"]:.1f}s</td>
            <td>{report_link}</td>
        </tr>""")

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Airtest 测试汇总报告</title>
<style>
  body {{ font-family: -apple-system,Segoe UI,Helvetica,Arial,sans-serif; margin: 32px; color:#333; }}
  h1 {{ margin: 0 0 16px; }}
  .stats {{ display:flex; gap:16px; margin-bottom: 24px; }}
  .card {{ flex:1; padding:16px; border-radius:8px; background:#f6f8fa; border:1px solid #e1e4e8; }}
  .card .num {{ font-size:28px; font-weight:bold; }}
  .pass {{ color:#28a745; }} .fail {{ color:#dc3545; }}
  table {{ width:100%; border-collapse: collapse; }}
  th, td {{ padding: 10px 12px; border-bottom:1px solid #eee; text-align:left; }}
  th {{ background:#f6f8fa; }}
  tr:hover {{ background:#fafbfc; }}
</style>
</head>
<body>
<h1>📊 Airtest 测试汇总报告</h1>
<p>生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
<div class="stats">
  <div class="card"><div>总用例</div><div class="num">{total}</div></div>
  <div class="card"><div>通过</div><div class="num pass">{passed}</div></div>
  <div class="card"><div>失败</div><div class="num fail">{failed}</div></div>
  <div class="card"><div>通过率</div><div class="num">{(passed/total*100 if total else 0):.1f}%</div></div>
</div>
<table>
  <thead><tr><th>用例</th><th>结果</th><th>耗时</th><th>详细报告</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
</table>
</body></html>"""

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📈 汇总报告已生成: {summary_path}")


# ----------------------------- 批量执行 -----------------------------
def run_all_tests(device="Android:///"):
    """运行所有测试脚本"""
    print("🚀 运行所有测试脚本...")

    scripts = discover_scripts()
    if not scripts:
        print("未找到测试脚本！请将 .air/.py 放入 scripts/ 目录。")
        return 1

    print(f"共发现 {len(scripts)} 个用例：")
    for s in scripts:
        print(f"   - {os.path.basename(s)}")
    print("-" * 60)

    results = []
    exit_codes = []
    batch_ts = time.strftime("%Y%m%d_%H%M%S")

    for script in scripts:
        case_name = os.path.splitext(os.path.basename(script))[0]
        report_name = f"report_{case_name}_{batch_ts}"

        start = time.time()
        exit_code, report_path = run_test(script, report_name, device=device)
        duration = time.time() - start

        results.append({
            "name": case_name,
            "status": "PASS" if exit_code == 0 else "FAIL",
            "report": report_path,
            "duration": duration,
        })
        exit_codes.append(exit_code)
        print("-" * 60)

    # 汇总报告
    summary_path = os.path.join(REPORT_DIR, f"summary_{batch_ts}.html")
    generate_summary(results, summary_path)

    # 打印简要统计
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n执行完毕：{passed}/{len(results)} 通过")

    return max(exit_codes) if exit_codes else 0


# ----------------------------- 入口 -----------------------------
def main():
    parser = argparse.ArgumentParser(description="简化版Airtest测试框架")
    parser.add_argument("-s", "--script", help="指定测试脚本路径（相对或绝对）")
    parser.add_argument("-r", "--report", default=None,
                        help="测试报告名称（不带扩展名），默认自动加时间戳")
    parser.add_argument("-a", "--all", action="store_true", help="运行所有测试脚本")
    parser.add_argument("-d", "--device", default="Android:///",
                        help="设备 URI，默认 Android:/// （可选）")
    parser.add_argument("--skip-check", action="store_true",
                        help="跳过 airtest/adb 环境检查")
    args = parser.parse_args()

    # 确保目录存在
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    # 改进 #4：环境预检
    if not args.skip_check:
        if not check_environment():
            print("\n环境检查未通过，已退出。可加 --skip-check 跳过此检查。")
            sys.exit(2)

    if args.all:
        exit_code = run_all_tests(device=args.device)
    elif args.script:
        script_path = args.script
        if not os.path.exists(script_path):
            script_path = os.path.join(SCRIPTS_DIR, args.script)
            if not os.path.exists(script_path):
                print(f"测试脚本不存在: {args.script}")
                sys.exit(1)

        # 改进 #2：单脚本默认报告名也加时间戳，避免覆盖历史
        case_name = os.path.splitext(os.path.basename(script_path))[0]
        ts = time.strftime("%Y%m%d_%H%M%S")
        report_name = args.report if args.report else f"report_{case_name}_{ts}"

        exit_code, _ = run_test(script_path, report_name, device=args.device)
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(exit_code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  已被用户中断")
        sys.exit(130)
