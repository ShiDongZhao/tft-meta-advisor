---
name: tft-meta-advisor
description: 从 datatft.com 抓取云顶之弈(TFT)当前版本阵容胜率、登场率数据，分析版本强度并给出阵容推荐。当用户询问云顶之弈阵容推荐、TFT meta、版本强势阵容、吃鸡阵容、上分阵容、当前版本什么阵容强、datatft 数据分析时使用此 skill。
---

# 云顶之弈版本阵容推荐

从 datatft.com 获取实时阵容梯队数据，为用户提供当前版本的阵容推荐和运营建议。

## 触发场景

- 用户询问当前版本强势阵容、meta 阵容
- 用户想知道什么阵容胜率高、登场率高
- 用户提到 datatft、云顶之弈阵容推荐、TFT 上分
- 用户想了解当前版本阵容梯队（T0/T1/T2）
- 用户问某个阵容怎么玩、怎么运营

## 不适用场景

- 用户只是问云顶之弈的基础规则或玩法教程
- 用户在讨论其他游戏
- 用户需要的是具体对局中的实时决策（转职、凑利息等）

## 工作流程

### 第一步：运行脚本获取数据

使用 `scripts/fetch_tft_meta.py` 脚本获取数据。脚本位于本 skill 目录下。

**获取阵容梯队列表（最常用）：**
```bash
python <skill-path>/scripts/fetch_tft_meta.py
```

**获取指定阵容的详细运营攻略：**
```bash
python <skill-path>/scripts/fetch_tft_meta.py --detail <阵容ID>
```

**获取所有 S/A 级阵容的详细攻略：**
```bash
python <skill-path>/scripts/fetch_tft_meta.py --all
```

**输出原始 JSON（用于程序化处理）：**
```bash
python <skill-path>/scripts/fetch_tft_meta.py --json
```

其中 `<skill-path>` 是本 skill 的安装路径（通常为 `~/.roo/skills/tft-meta-advisor`）。

### 第二步：分析数据并回复用户

根据脚本输出的数据：

1. **如果用户问"什么阵容强"** → 展示 T0/T1 阵容列表
2. **如果用户问某个具体阵容** → 用 `--detail ID` 获取运营攻略
3. **如果用户想要全面了解** → 用 `--all` 获取完整数据

### 第三步：格式化输出

使用以下格式呈现推荐结果：

```markdown
## 当前版本阵容梯队 (数据来源: datatft.com)

### T0 阵容（强烈推荐）
- **阵容名称** | 任务: XX, XX
  - 核心思路: ...
  - 简要运营: ...

### T1 阵容（推荐）
- ...

### T2 阵容（可用）
- ...
```

如果用户询问具体阵容详情，展示：
- 核心思路
- 开局选择
- 前/中/后期运营
- 装备推荐
- 难度评级
- 阵容模拟器链接

## API 说明（备用，脚本不可用时手动调用）

数据源: `https://api.datatft.com`

### 签名机制

所有请求需要以下 headers：
- `t`: 当前时间戳（毫秒）
- `did`: 设备ID（任意字符串）
- `nonce`: 16位随机字符串（大小写字母+数字）
- `signature`: MD5(`{t}{nonce}{did}koTefnFEdaYDuLFmXyzt`)
- `Content-Type`: application/json
- `Accept-Language`: CN
- `Browser-Language`: ZH-CN

### 可用接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/team/rank` | POST `{}` | 阵容排名（简略，含梯队） |
| `/team/comps` | POST `{"season":"17"}` | 阵容列表（含标题、梯队、任务） |
| `/team/strategy` | POST `{"id": 阵容ID}` | 阵容详情（运营攻略） |

注意：`/team/rank` 不需要签名也能调用，其他接口需要完整签名。

## 注意事项

- 数据具有时效性，每次都应运行脚本获取最新数据
- 如果脚本执行失败（网络问题），告知用户并建议直接访问 https://www.datatft.com
- 胜率数据仅供参考，实际游戏中还需考虑对手阵容、经济运营等因素
- 回复使用中文，除非用户使用其他语言提问
- 阵容的"任务"字段表示该阵容适合选择的英雄传送门任务
