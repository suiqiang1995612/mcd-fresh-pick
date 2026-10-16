#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦麦新品种草官 · 宣传渲染引擎 (promo.py)
-------------------------------------------------
输入：MCD MCP 工具返回的结构化数据（JSON 文件 / 管道 stdin）
输出：① Markdown 速览卡片　② 多种「麦当劳适配」风格的 HTML 宣传视觉卡

内置风格见 styles.py（可用 --list-styles 查看）。

设计原则：
- 仅依赖 Python 标准库，零第三方依赖，可直接运行。
- 数据来源只能是 MCP 工具返回；本引擎不做任何数据编造。
- 两种输出都固定带免责声明；HTML 额外带「理性消费 · 适量享用」提示。
- 不做竞品对比、不诱导浪费；**不伪造产品图**，
  图片仅使用 MCP 工具返回的官方 URL，无图时用纯色占位块。

用法：
    python promo.py --list-styles
    python promo.py data.json --style hero --format md
    python promo.py data.json --style limit --format html > card.html
    cat data.json | python promo.py
    python promo.py                    # 无输入时使用内置示例数据
"""

import sys
import json
import argparse
import datetime

import styles

DISCLAIMER = (
    "> 以上信息基于麦当劳中国官方 MCP 实时数据整理，仅供参考；"
    "餐品、价格、供应与活动以麦当劳官方渠道为准。"
)


def _pick(d, *keys, default=""):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return default


# ------------------------------------------------------------ Markdown 输出

def build_card(data):
    lines = []
    today = datetime.date.today().isoformat()
    lines.append(f"# 🍔 麦麦新品种草 · {today}")
    lines.append("")

    campaigns = data.get("campaigns") or []
    if campaigns:
        lines.append("## ⏰ 限时活动（进行中 / 即将开始）")
        for c in campaigns[:5]:
            name = _pick(c, "name", "title", default="活动")
            period = _pick(c, "period", "date", "time")
            suffix = f" · {period}" if period else ""
            lines.append(f"- **{name}**{suffix}")
        lines.append("")

    meals = data.get("meals") or data.get("items") or []
    if meals:
        lines.append("## 🆕 值得尝的新品 / 特色")
        for m in meals[:5]:
            name = _pick(m, "name", "title", default="餐品")
            tag = _pick(m, "tag", "label")
            price = _pick(m, "price")
            line = f"- **{name}**"
            if tag:
                line += f"  _{tag}_"
            if price:
                line += f"  ¥{price}"
            lines.append(line)
        lines.append("")

    coupons = data.get("coupons") or []
    if coupons:
        lines.append("## 🎟️ 顺手可用的券")
        for cp in coupons[:5]:
            lines.append(f"- {_pick(cp, 'name', 'title', default='优惠券')}")
        lines.append("")

    stores = data.get("stores") or []
    if stores:
        lines.append("## 📍 附近可参与门店")
        for s in stores[:3]:
            lines.append(f"- {_pick(s, 'name', 'storeName', default='门店')}")
        lines.append("")

    lines.append(DISCLAIMER)
    return "\n".join(lines)


def _demo_data():
    """内置示例数据（仅用于演示渲染效果，均为「示例：」前缀，非真实商品）。"""
    return {
        "headline": "示例：麦麦秋日限定",
        "theme": "示例：限定主题 · 邀你赴约",
        "campaigns": [
            {"name": "示例：买一送一狂欢", "period": "本周末"},
            {"name": "示例：限定周边回归", "period": "即日—本月底"},
        ],
        "meals": [
            {"name": "示例：芝士安格斯厚牛堡", "tag": "新品", "price": "29.5",
             "desc": "示例描述：厚牛饼配双层芝士"},
            {"name": "示例：杨枝甘露麦旋风", "tag": "限定", "price": "18.0",
             "desc": "示例描述：芒果西柚风味"},
            {"name": "示例：双层吉士蛋麦满分", "tag": "早餐", "price": "15.5",
             "desc": "示例描述：现烤英式松饼"},
            {"name": "示例：麦辣鸡腿堡", "tag": "经典", "price": "21.0",
             "desc": "示例描述：深夜也想吃"},
        ],
        "coupons": [
            {"name": "示例：满30减8 麦麦省券"},
            {"name": "示例：早餐组合立减5元"},
        ],
        "stores": [{"name": "示例：三亚XX路餐厅"}],
    }


# ------------------------------------------------------------------ 数据装载

def _load(args):
    raw = None
    if args.json_file:
        with open(args.json_file, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        # 非阻塞探测管道输入：0.1s 无数据则走示例，避免在非交互 shell 下卡死
        try:
            import select
            if not sys.stdin.isatty():
                r, _, _ = select.select([sys.stdin], [], [], 0.1)
                if r:
                    raw = sys.stdin.read()
        except (ImportError, OSError):
            pass

    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[promo.py] JSON 解析失败：{e}", file=sys.stderr)
            sys.exit(1)
    return _demo_data()


# --------------------------------------------------------------------- 入口

def main():
    parser = argparse.ArgumentParser(description="麦麦新品种草官 · 宣传渲染引擎")
    parser.add_argument("json_file", nargs="?",
                        help="MCP 返回的 JSON 数据文件；省略则读管道或使用内置示例")
    parser.add_argument("--style", default=styles.DEFAULT_STYLE,
                        help=f"宣传风格 id（见 --list-styles），默认 {styles.DEFAULT_STYLE}")
    parser.add_argument("--format", dest="fmt", choices=["md", "html"], default="md",
                        help="输出格式：md=Markdown 卡片，html=HTML 宣传视觉卡")
    parser.add_argument("--list-styles", action="store_true", help="列出内置宣传风格")
    args = parser.parse_args()

    if args.list_styles:
        print("内置「麦当劳适配」宣传风格：")
        for sid, name, scene in styles.list_styles():
            mark = "*" if sid == styles.DEFAULT_STYLE else " "
            print(f"{mark} {sid:<9}{name:<8}—— {scene}")
        print("\n（* 表示默认风格）")
        return

    if args.style not in styles.STYLES:
        print(f"[promo.py] 未知风格 '{args.style}'，回退到默认 '{styles.DEFAULT_STYLE}' "
              f"（可用 --list-styles 查看）", file=sys.stderr)

    data = _load(args)
    if args.fmt == "html":
        print(styles.render(args.style, data))
    else:
        print(build_card(data))


if __name__ == "__main__":
    main()
