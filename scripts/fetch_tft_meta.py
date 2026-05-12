"""
DataTFT API 数据抓取脚本
从 datatft.com 获取云顶之弈阵容梯队数据

用法:
  python fetch_tft_meta.py                    # 获取阵容梯队列表
  python fetch_tft_meta.py --detail ID        # 获取指定阵容详情
  python fetch_tft_meta.py --all              # 获取所有S/A级阵容详情
  python fetch_tft_meta.py --output file.md   # 输出到文件
"""

import hashlib
import random
import string
import time
import json
import urllib.request
import sys
import os
import argparse

SECRET = "koTefnFEdaYDuLFmXyzt"
API_BASE = "https://api.datatft.com"


def generate_nonce(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_signature(t, nonce, did):
    raw = f"{t}{nonce}{did}{SECRET}"
    return hashlib.md5(raw.encode()).hexdigest()


def call_api(path, body=None):
    """调用 datatft API，自动处理签名"""
    t = str(int(time.time() * 1000))
    nonce = generate_nonce()
    did = "datatft_skill_agent"
    signature = generate_signature(t, nonce, did)

    url = f"{API_BASE}{path}"
    headers = {
        "Content-Type": "application/json",
        "Browser-Language": "ZH-CN",
        "Accept-Language": "CN",
        "t": t,
        "did": did,
        "nonce": nonce,
        "signature": signature,
    }

    data = json.dumps(body or {}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
        return json.loads(raw.decode('utf-8'))


def get_comp_list(season=None):
    """获取阵容梯队列表"""
    body = {}
    if season:
        body["season"] = season
    result = call_api("/team/comps", body)
    if result.get("success"):
        return result["data"]["list"]
    return []


def get_comp_rank(season=None):
    """获取阵容排名（简略版）"""
    body = {}
    if season:
        body["season"] = season
    result = call_api("/team/rank", body)
    if result.get("success"):
        return result["data"]
    return {}


def get_comp_detail(comp_id):
    """获取阵容详情（运营思路、装备推荐等）"""
    result = call_api("/team/strategy", {"id": comp_id})
    if result.get("success"):
        return result["data"]
    return {}


def format_tier_list(comps):
    """格式化阵容梯队列表为 Markdown"""
    tiers = {"S": [], "A": [], "B": [], "C": [], "D": []}
    for comp in comps:
        tier = comp.get("tier", "")
        if tier in tiers:
            tiers[tier].append(comp)

    tier_labels = {
        "S": "T0 阵容（强烈推荐）",
        "A": "T1 阵容（推荐）",
        "B": "T2 阵容（可用）",
        "C": "T3 阵容（较弱）",
        "D": "T4 阵容（不推荐）"
    }

    lines = ["## 当前版本阵容梯队 (数据来源: datatft.com)\n"]

    for tier_name in ["S", "A", "B", "C", "D"]:
        items = tiers[tier_name]
        if items:
            lines.append(f"\n### {tier_labels[tier_name]}")
            for item in items:
                title = item.get("title", "Unknown")
                comp_id = item.get("id")
                ext = item.get("ext", "")

                tasks_str = ""
                if ext:
                    try:
                        ext_data = json.loads(ext)
                        tasks = [e.get("name", "") for e in ext_data if e.get("type") == "task"]
                        if tasks:
                            tasks_str = f" | 任务: {', '.join(tasks)}"
                    except:
                        pass

                lines.append(f"- **{title}** (ID:{comp_id}){tasks_str}")

    return "\n".join(lines)


def format_comp_detail(detail):
    """格式化阵容详情为 Markdown"""
    lines = []
    lines.append(f"## {detail.get('title', '未知阵容')}\n")

    if detail.get("core"):
        lines.append(f"**核心思路**: {detail['core']}\n")
    if detail.get("open"):
        lines.append(f"**开局**: {detail['open']}\n")
    if detail.get("earlyDesc"):
        lines.append(f"**前期运营**: {detail['earlyDesc']}\n")
    if detail.get("midDesc"):
        lines.append(f"**中期运营**: {detail['midDesc']}\n")
    if detail.get("finalDesc"):
        lines.append(f"**后期运营**: {detail['finalDesc']}\n")

    if detail.get("difficulty"):
        diff_map = {1: "简单", 2: "中等", 3: "困难"}
        lines.append(f"**难度**: {diff_map.get(detail['difficulty'], '未知')}\n")

    if detail.get("tags"):
        lines.append(f"**标签**: {', '.join(detail['tags'])}\n")

    if detail.get("teamUrl"):
        lines.append(f"**阵容模拟器**: {detail['teamUrl']}\n")

    return "\n".join(lines)


def output_result(text, output_file=None):
    """输出结果到文件或标准输出"""
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        # Windows 终端兼容
        if sys.platform == "win32":
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        print(text)


def main():
    parser = argparse.ArgumentParser(description="DataTFT 阵容数据抓取")
    parser.add_argument("--detail", type=int, help="获取指定阵容ID的详情")
    parser.add_argument("--all", action="store_true", help="获取所有S/A级阵容详情")
    parser.add_argument("--season", type=str, default=None, help="赛季号，如 17")
    parser.add_argument("--json", action="store_true", help="输出原始JSON")
    parser.add_argument("--output", "-o", type=str, help="输出到文件路径")
    args = parser.parse_args()

    result_text = ""

    if args.detail:
        detail = get_comp_detail(args.detail)
        if args.json:
            result_text = json.dumps(detail, ensure_ascii=False, indent=2)
        else:
            result_text = format_comp_detail(detail)
    elif args.all:
        comps = get_comp_list(args.season)
        parts = [format_tier_list(comps), "\n\n---\n"]
        for comp in comps:
            if comp.get("tier") in ["S", "A"]:
                detail = get_comp_detail(comp["id"])
                if detail:
                    parts.append(format_comp_detail(detail))
                    parts.append("\n---\n")
                time.sleep(0.3)
        result_text = "\n".join(parts)
    else:
        comps = get_comp_list(args.season)
        if args.json:
            result_text = json.dumps(comps, ensure_ascii=False, indent=2)
        else:
            result_text = format_tier_list(comps)

    output_result(result_text, args.output)


if __name__ == "__main__":
    main()
