# 简化版Airtest测试框架

## 框架介绍

这是一个简化版的Airtest测试框架，支持直接使用Airtest客户端录制的测试脚本，无需或只需少量修改即可在此框架下运行，并保留生成测试报告等功能。

### 功能特性

- ✅ 支持 Airtest 客户端录制的脚本（`.air` / `.py`）直接运行
- ✅ 支持批量执行测试脚本，每个用例独立日志目录，互不干扰
- ✅ 自动生成 HTML 测试报告，并附带**汇总总览页**（pass/fail 统计）
- ✅ 单脚本报告名默认带时间戳，历史报告不会被覆盖
- ✅ 启动时自动检查 `airtest` 与 `adb` 环境，提前发现配置问题
- ✅ 支持自定义设备 URI（Android、iOS、Windows 等）
- ✅ 用例输出实时打印，长用例不再"假死"

## 目录结构

```
airtest_simple_framework/
├── scripts/           # 测试脚本目录（存放Airtest录制的脚本）
├── report/            # 测试报告目录
├── logs/              # 日志目录
├── run.py             # 主执行入口
└── requirements.txt   # 依赖包
```

## 环境安装

1. **安装Python 3.8+**
   - 下载并安装Python 3.8或更高版本
   - 确保添加到环境变量

2. **安装依赖包**
   ```bash
   cd airtest_simple_framework
   pip install -r requirements.txt
   ```

3. **安装Airtest IDE（可选）**
   - 下载并安装Airtest IDE，用于录制和编辑测试用例
   - 下载地址：https://airtest.netease.com/

4. **配置设备**
   - Android设备：启用USB调试模式，通过`adb devices`查看设备ID
   - iOS设备：需要安装Xcode和相关依赖

## 使用方法

### 1. 准备测试脚本

- **方法1：使用Airtest IDE录制**
  1. 打开Airtest IDE
  2. 连接设备
  3. 点击"录制"按钮开始录制
  4. 完成操作后，点击"停止录制"
  5. 将生成的.py或.air文件保存到`scripts/`目录

- **方法2：手动编写脚本**
  在`scripts/`目录创建.py文件，使用Airtest API编写测试脚本

### 2. 运行测试

#### 运行单个测试脚本

```bash
# 方法1：指定脚本路径
python run.py -s scripts/test_example.py

# 方法2：直接指定脚本名称（会在scripts目录中查找）
python run.py -s test_example.py

# 自定义报告名称（不指定时会自动加时间戳，避免覆盖）
python run.py -s test_example.py -r my_report

# 指定设备（如 iOS、Windows、特定 Android 序列号）
python run.py -s test_example.py -d "Android://127.0.0.1:5037/emulator-5554"

# 跳过环境检查（如已知 airtest/adb 已就绪）
python run.py -s test_example.py --skip-check
```

#### 运行所有测试脚本

```bash
python run.py -a
```

批量执行后，除了每个用例的独立报告外，还会在 `report/` 目录下生成 `summary_<时间戳>.html`，
点开即可看到所有用例的通过/失败统计与跳转链接。

### 3. 查看报告

测试完成后，报告将生成在 `report/` 目录下：

- `report_<用例名>_<时间戳>.html` —— 单个用例的详细报告
- `summary_<时间戳>.html` —— 批量执行的汇总总览（仅 `-a` 时生成）

每个用例的运行日志位于 `logs/report_<用例名>_<时间戳>/`，互不干扰。

### 4. 命令行参数一览

| 参数 | 说明 |
|---|---|
| `-s, --script` | 指定要运行的脚本（路径或名称） |
| `-a, --all` | 运行 `scripts/` 下所有用例 |
| `-r, --report` | 自定义报告名（默认带时间戳） |
| `-d, --device` | 设备 URI，默认 `Android:///` |
| `--skip-check` | 跳过 airtest/adb 环境检查 |

## 脚本规范

Airtest客户端录制的脚本通常包含以下内容：

```python
from airtest.core.api import *
from airtest.cli.parser import cli_setup

# 自动初始化
if not cli_setup():
    auto_setup(__file__, devices=["Android:///"])

# 测试步骤
# ...
```

这种格式的脚本可以直接放入`scripts/`目录，无需修改即可运行。

## 注意事项

1. **设备连接**：确保设备已正确连接，且开启了USB调试模式
2. **脚本路径**：测试脚本应放在`scripts/`目录下
3. **图片资源**：如果脚本中使用了图片模板，确保图片文件与脚本在同一目录或正确引用
4. **权限处理**：首次运行时，手机可能会弹出权限请求，需要手动允许
5. **网络环境**：确保测试环境网络稳定

## 故障排查

1. **设备未识别**：检查设备是否已连接，ADB是否正常
2. **脚本执行失败**：检查脚本中的元素定位是否正确
3. **报告生成失败**：检查报告目录是否存在，权限是否正确
4. **依赖包安装失败**：尝试使用管理员权限安装依赖包

---

**框架版本**：v1.0.0
**维护者**：MLP
