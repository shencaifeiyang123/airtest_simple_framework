# 安装airtest脚本
import sys
import subprocess

print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

# 尝试安装airtest
print("\n尝试安装airtest...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "airtest==1.3.5"],
        capture_output=True,
        text=True
    )
    print("安装输出:")
    print(result.stdout)
    if result.stderr:
        print("错误信息:")
        print(result.stderr)
    print(f"安装返回码: {result.returncode}")
except Exception as e:
    print(f"安装失败: {str(e)}")

# 检查是否安装成功
print("\n检查airtest是否安装成功...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True,
        text=True
    )
    if "airtest" in result.stdout:
        print("✅ airtest安装成功！")
    else:
        print("❌ airtest未安装成功！")
except Exception as e:
    print(f"检查失败: {str(e)}")
