# TFT Meta Advisor

云顶之弈版本强度分析工具——从 datatft.com 抓取实时阵容胜率、登场率数据，生成版本梯队推荐与阵容运营攻略。

## 功能

- 获取当前版本阵容梯队列表（T0~T4）
- 查询指定阵容的详细运营思路（核心思路、开局选择、前/中/后期运营、装备推荐、难度评级）
- 批量导出所有 S/A 级阵容攻略
- 支持 Markdown 和 JSON 两种输出格式
- 支持指定赛季

## 快速开始

```bash
# Python 3.6+ 环境，无需第三方依赖（仅用标准库）

# 获取阵容梯队列表
python scripts/fetch_tft_meta.py

# 获取指定阵容详情（阵容ID从梯队列表中获取）
python scripts/fetch_tft_meta.py --detail <阵容ID>

# 获取所有 S/A 级阵容详细攻略
python scripts/fetch_tft_meta.py --all

# 输出原始 JSON
python scripts/fetch_tft_meta.py --json

# 指定赛季并输出到文件
python scripts/fetch_tft_meta.py --season 17 --output meta.md
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--detail ID` | 获取指定阵容ID的详细运营攻略 |
| `--all` | 获取所有 S/A 级阵容的详细攻略 |
| `--season S` | 指定赛季号（如 `17`），不指定则获取当前赛季 |
| `--json` | 输出原始 JSON 格式（适用于程序化处理） |
| `--output` / `-o` | 将结果写入文件而非标准输出 |

## 输出示例

### 梯队列表

```
## 当前版本阵容梯队 (数据来源: datatft.com)

### T0 阵容（强烈推荐）
- **阵容名称** (ID:123) | 任务: 任务A, 任务B

### T1 阵容（推荐）
- **阵容名称** (ID:456)
```

### 阵容详情

- 核心思路
- 开局选择
- 前期/中期/后期运营
- 难度评级（简单/中等/困难）
- 阵容标签
- 阵容模拟器链接

## API 说明

数据来源: `https://api.datatft.com`

所有请求需要签名（`/team/rank` 除外），签名算法见 `scripts/fetch_tft_meta.py`。

| 接口 | 方法 | 说明 |
|------|------|------|
| `/team/rank` | POST `{}` | 阵容排名（简略，含梯队） |
| `/team/comps` | POST `{"season":"17"}` | 阵容列表（含标题、梯队、任务） |
| `/team/strategy` | POST `{"id": 阵容ID}` | 阵容详情（运营攻略） |

## 注意事项

- 数据具有时效性，每次使用都应重新运行脚本获取最新数据
- 如果脚本执行失败（网络问题），可直接访问 https://www.datatft.com
- 胜率数据仅供参考，实际游戏中还需考虑对手阵容、经济运营等因素
- 如需在 AI/Copilot 中使用此工具，详见 [SKILL.md](./SKILL.md)

## 许可证

[MIT](./LICENSE)
