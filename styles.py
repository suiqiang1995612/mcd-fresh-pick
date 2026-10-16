#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
styles.py · 多种「麦当劳适配」的产品宣传风格渲染
================================================
每个风格把 MCP 返回的结构化数据绘制成一张**自包含 HTML 卡片**：
无外部依赖、无 CDN、无第三方资源、完全离线可打开。

合规约束（渲染层强制，违反即取消参赛资格）：
- 每张卡片都带固定免责声明 + 「理性消费 · 适量享用」提示
- 不做任何竞品对比 / 不出现其他品牌
- 不诱导暴饮暴食、浪费、炫富式消费；给出的数据中性呈现，不做健康或医疗承诺
- 图片**只使用 MCP 工具返回的官方 URL**；无图时用纯色占位块，
  绝不通过 AI 生成或伪造产品图（避免虚假宣传与商标风险）
- 所有文本经过 HTML 转义，杜绝注入脚本
"""

from html import escape
from datetime import date

DISCLAIMER = (
    "以上信息基于麦当劳中国官方 MCP 实时数据整理，仅供参考；"
    "餐品、价格、供应与活动以麦当劳官方渠道为准。"
)
NUDGE = "理性消费 · 适量享用"


# ---------------------------------------------------------------- 基础工具

def _e(s):
    """HTML 转义，防止脚本注入。"""
    return escape(str(s if s is not None else ""), quote=True)


def _pick(d, *keys, default=""):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return default


def _figure(d, css_class="pic"):
    """优先使用 MCP 返回的官方图片 URL；无图则用首字色块占位，绝不伪造产品图。"""
    url = _pick(d, "image", "imageUrl", "pic", "img", "picture", "imgUrl")
    if url and str(url).startswith(("http://", "https://")):
        alt = _pick(d, "name", "title", default="餐品")
        return f'<img class="{css_class} pic-img" src="{_e(url)}" alt="{_e(alt)}" />'
    initial = str(_pick(d, "name", "title", default="麦"))[:1]
    return f'<div class="{css_class} pic-ph">{_e(initial)}</div>'


def _items(data, key="meals", limit=5):
    out = data.get(key) or data.get("items") or []
    return list(out)[:limit]


def _footnote():
    return (
        f'<footer class="foot"><div class="note">{_e(DISCLAIMER)}</div>'
        f'<div class="nudge">{_e(NUDGE)}</div></footer>'
    )


# ------------------------------------------------------------ 风格 1 经典主推

_CSS_HERO = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#FFF6E5;}
.wrap{max-width:680px;margin:0 auto;padding:28px;}
.hero{background:linear-gradient(135deg,#DA291C 0%,#AF1C13 100%);color:#FFF;border-radius:20px;padding:28px 26px;position:relative;overflow:hidden;}
.hero::after{content:"";position:absolute;right:-60px;top:-60px;width:190px;height:190px;border-radius:50%;background:rgba(255,199,44,.22)}
.kicker{font-size:12px;letter-spacing:3px;color:#FFC72C;font-weight:700}
.hero h1{font-size:30px;margin:10px 0 6px;line-height:1.25}
.badge{display:inline-block;background:#FFC72C;color:#8C1D12;font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;margin-right:6px}
.price{font-size:26px;font-weight:800;color:#FFC72C;margin-top:12px}
.hero .pic{width:100%;height:200px;object-fit:cover;border-radius:14px;margin-top:16px;background:rgba(255,255,255,.14)}
.pic-ph{display:flex;align-items:center;justify-content:center;font-size:56px;color:rgba(255,255,255,.7);font-weight:800}
.panel{background:#FFF;border-radius:18px;padding:20px 22px;margin-top:16px;box-shadow:0 6px 20px rgba(140,29,18,.10)}
.panel h2{font-size:14px;color:#DA291C;letter-spacing:2px;margin-bottom:12px}
.row{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-bottom:1px dashed #F0E0C8;font-size:14px;color:#2B211E}
.row:last-child{border-bottom:none}
.chip{display:inline-block;background:#FFF0D6;color:#8C1D12;font-size:12px;padding:5px 11px;border-radius:999px;margin:4px 6px 0 0}
.foot{margin-top:16px;padding:14px 16px;background:#fffdf7;border-radius:12px;border:1px solid #F0E0C8}
.note{font-size:11.5px;color:#7A6A62;line-height:1.6}
.nudge{font-size:11px;color:#A8958A;margin-top:6px}
"""


def render_hero(data):
    meals = _items(data)
    hero_item = meals[0] if meals else {}
    campaigns = data.get("campaigns") or []
    coupons = data.get("coupons") or []

    rows = "".join(
        f'<div class="row"><span>{_e(_pick(c, "name", "title"))}</span>'
        f'<span style="color:#7A6A62">{_e(_pick(c, "period", "date"))}</span></div>'
        for c in campaigns[:4]
    ) or '<div class="row"><span>暂无进行中的活动</span></div>'

    chips = "".join(f'<span class="chip">{_e(_pick(c, "name", "title"))}</span>' for c in coupons[:6])
    price = _pick(hero_item, "price")

    body = f"""
<div class="wrap">
  <div class="hero">
    <div class="kicker">今 日 主 推</div>
    <h1>{_e(_pick(hero_item, 'name', 'title', default='暂无主推餐品'))}</h1>
    <div>{f'<span class="badge">{_e(_pick(hero_item, "tag", "label"))}</span>' if _pick(hero_item, "tag", "label") else ''}</div>
    {f'<div class="price">¥{_e(price)}</div>' if price else ''}
    {_figure(hero_item)}
  </div>
  <div class="panel"><h2>⏰ 限时活动</h2>{rows}</div>
  <div class="panel"><h2>🎟️ 顺手可用的券</h2>{chips or '<div class="row"><span>暂无可用券</span></div>'}</div>
  {_footnote()}
</div>"""
    return _page("经典主推", body, _CSS_HERO, "#FFF6E5")


# ------------------------------------------------------------ 风格 2 限定夜潮

_CSS_LIMIT = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#120C0B;color:#F5EDE4}
.wrap{max-width:680px;margin:0 auto;padding:28px}
.head{text-align:center;padding:26px 20px;border:1px solid rgba(255,199,44,.35);border-radius:18px;background:radial-gradient(circle at 50% 0%,rgba(255,199,44,.12),transparent 70%)}
.kicker{font-size:12px;letter-spacing:4px;color:#FFC72C;font-weight:700}
.head h1{font-size:28px;margin:12px 0;color:#FFC72C;letter-spacing:1px}
.sub{font-size:13px;color:#A8958A}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:18px}
.card{background:#1E1513;border:1px solid rgba(255,199,44,.18);border-radius:16px;padding:14px;transition:.2s}
.card:hover{border-color:rgba(255,199,44,.55)}
.card .pic{width:100%;height:120px;object-fit:cover;border-radius:10px;background:#2A1E1B}
.pic-ph{display:flex;align-items:center;justify-content:center;font-size:40px;color:#FFC72C;font-weight:800}
.name{font-size:14px;font-weight:700;margin-top:10px;color:#F5EDE4}
.meta{font-size:12px;color:#A8958A;margin-top:4px}
.price{color:#FFC72C;font-weight:800;margin-top:6px;font-size:15px}
.strip{margin-top:18px;padding:16px 18px;background:#1E1513;border-radius:14px;border-left:3px solid #FFC72C}
.strip h2{font-size:13px;color:#FFC72C;letter-spacing:2px;margin-bottom:10px}
.line{font-size:13px;color:#C9B8AE;padding:5px 0}
.foot{margin-top:18px;padding:14px 16px;background:#1A1211;border-radius:12px}
.note{font-size:11.5px;color:#8C7A70;line-height:1.6}
.nudge{font-size:11px;color:#6E5C54;margin-top:6px}
@media(max-width:520px){.grid{grid-template-columns:1fr}}
"""


def render_limit(data):
    meals = _items(data, limit=4)
    cards = ""
    for m in meals:
        price = _pick(m, "price")
        cards += (
            '<div class="card">'
            f'{_figure(m)}'
            f'<div class="name">{_e(_pick(m, "name", "title"))}</div>'
            f'<div class="meta">{_e(_pick(m, "tag", "label", default="限定"))}</div>'
            + (f'<div class="price">¥{_e(price)}</div>' if price else "")
            + "</div>"
        )
    lines = "".join(
        f'<div class="line">· {_e(_pick(c, "name", "title"))}'
        + (f'　<i style="color:#8C7A70">{_e(_pick(c, "period", "date"))}</i>' if _pick(c, "period", "date") else "")
        + "</div>"
        for c in (data.get("campaigns") or [])[:5]
    ) or '<div class="line">暂无限时活动</div>'

    body = f"""
<div class="wrap">
  <div class="head">
    <div class="kicker">限 定 上 线</div>
    <h1>{_e(_pick(data, "headline", "theme", default="麦麦限定 · 手慢无"))}</h1>
    <div class="sub">{_e(date.today().isoformat())}　限时供应，先到先得</div>
  </div>
  <div class="grid">{cards or '<div class="card"><div class="name">暂无餐品数据</div></div>'}</div>
  <div class="strip"><h2>⏳ 活动日历</h2>{lines}</div>
  {_footnote()}
</div>"""
    return _page("限定夜潮", body, _CSS_LIMIT, "#120C0B")


# ------------------------------------------------------------ 风格 3 晨光早餐

_CSS_MORNING = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(180deg,#FFFDF5 0%,#FFF3E0 100%);color:#4A3A2A}
.wrap{max-width:680px;margin:0 auto;padding:28px}
.toptag{display:inline-block;background:#FFE3B3;color:#B26A00;font-size:12px;font-weight:700;padding:6px 14px;border-radius:999px}
h1{font-size:27px;margin:14px 0 4px;color:#3A2C1E}
.lead{font-size:13.5px;color:#8B7355}
.list{margin-top:20px;background:#fff;border-radius:20px;padding:8px 18px;box-shadow:0 8px 24px rgba(214,170,90,.18)}
.item{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid #F6EAD8}
.item:last-child{border-bottom:none}
.pic{width:62px;height:62px;flex:0 0 62px;border-radius:16px;object-fit:cover;background:#FFE3B3}
.pic-ph{display:flex;align-items:center;justify-content:center;font-size:24px;color:#B26A00;font-weight:800}
.info{flex:1}
.nm{font-size:15px;font-weight:700}
.tg{font-size:11.5px;color:#B26A00;background:#FFF3E0;display:inline-block;padding:2px 8px;border-radius:6px;margin-top:4px}
.pr{font-size:16px;font-weight:800;color:#E07A1F}
.cpn{margin-top:16px;font-size:12.5px;color:#7A6851;background:#FFF8EC;border:1px dashed #E8CFA6;border-radius:12px;padding:12px 14px;line-height:1.8}
.foot{margin-top:18px;padding:14px 16px;background:#FFF8EC;border-radius:12px}
.note{font-size:11.5px;color:#99836A;line-height:1.6}
.nudge{font-size:11px;color:#B5A08A;margin-top:6px}
"""


def render_morning(data):
    items = ""
    for m in _items(data, limit=5):
        price = _pick(m, "price")
        items += (
            '<div class="item">'
            f'{_figure(m)}'
            '<div class="info">'
            f'<div class="nm">{_e(_pick(m, "name", "title"))}</div>'
            + (f'<div class="tg">{_e(_pick(m, "tag", "label"))}</div>' if _pick(m, "tag", "label") else "")
            + "</div>"
            + (f'<div class="pr">¥{_e(price)}</div>' if price else "")
            + "</div>"
        )
    cps = "、".join(_pick(c, "name", "title") for c in (data.get("coupons") or [])[:4])

    body = f"""
<div class="wrap">
  <span class="toptag">☀️ 晨光上新</span>
  <h1>{_e(_pick(data, "headline", "theme", default="今天，从一份热的开始"))}</h1>
  <div class="lead">{_e(date.today().isoformat())}　{_e(_pick(data, "sub", default="早段限定组合，暖胃也暖心"))}</div>
  <div class="list">{items or '<div class="item"><div class="info"><div class="nm">暂无餐品数据</div></div></div>'}</div>
  {f'<div class="cpn">🎟️ 可用：{_e(cps)}</div>' if cps else ''}
  {_footnote()}
</div>"""
    return _page("晨光早餐", body, _CSS_MORNING, "#FFFDF5")


# ------------------------------------------------------------ 风格 4 极简日报

_CSS_DIGEST = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Helvetica Neue","PingFang SC","Microsoft YaHei",sans-serif;background:#F4F4F2;color:#1D1D1F}
.wrap{max-width:640px;margin:0 auto;padding:28px;background:#fff}
.bar{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #1D1D1F;padding-bottom:12px}
.bar h1{font-size:20px;letter-spacing:1px}
.bar .dt{font-size:12px;color:#86868B}
ol{list-style:none;margin-top:18px;counter-reset:n}
li{counter-increment:n;display:flex;gap:14px;padding:13px 0;border-bottom:1px solid #EFEFEF;align-items:flex-start}
li::before{content:counter(n);flex:0 0 22px;height:22px;border:1px solid #1D1D1F;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700}
.nm{font-size:14.5px;font-weight:600}
.sub2{font-size:12px;color:#86868B;margin-top:3px}
.pr{margin-left:auto;font-size:14px;font-weight:700;color:#1D1D1F}
.sec{margin-top:22px}
.sec h2{font-size:11px;letter-spacing:3px;color:#86868B;margin-bottom:10px}
.tagline{font-size:12.5px;color:#515154;border-left:2px solid #1D1D1F;padding-left:10px;margin:6px 0}
.foot{margin-top:24px;padding-top:14px;border-top:1px solid #EFEFEF}
.note{font-size:11px;color:#86868B;line-height:1.6}
.nudge{font-size:11px;color:#AFAFAF;margin-top:6px}
"""


def render_digest(data):
    lis = ""
    for m in _items(data, limit=6):
        price = _pick(m, "price")
        tag = _pick(m, "tag", "label")
        lis += (
            "<li><div><div class='nm'>"
            f"{_e(_pick(m, 'name', 'title'))}"
            + (f" <span style='font-size:11px;color:#86868B'>{_e(tag)}</span>" if tag else "")
            + f"</div><div class='sub2'>{_e(_pick(m, 'desc', 'note'))}</div></div>"
            + (f"<div class='pr'>¥{_e(price)}</div>" if price else "")
            + "</li>"
        )
    tl = "".join(
        f"<div class='tagline'>{_e(_pick(c, 'name', 'title'))}"
        + (f"　{_e(_pick(c, 'period', 'date'))}" if _pick(c, "period", "date") else "")
        + "</div>"
        for c in (data.get("campaigns") or [])[:5]
    )
    cl = "".join(
        f"<div class='tagline'>{_e(_pick(c, 'name', 'title'))}</div>"
        for c in (data.get("coupons") or [])[:5]
    )

    body = f"""
<div class="wrap">
  <div class="bar"><h1>今日麦麦速览</h1><span class="dt">{_e(date.today().isoformat())}</span></div>
  <ol>{lis or '<li><div><div class="nm">暂无餐品数据</div></div></li>'}</ol>
  {f'<div class="sec"><h2>限时活动</h2>{tl}</div>' if tl else ''}
  {f'<div class="sec"><h2>可用券</h2>{cl}</div>' if cl else ''}
  {_footnote()}
</div>"""
    return _page("极简日报", body, _CSS_DIGEST, "#F4F4F2")


# ------------------------------------------------------------ 风格 5 国潮派对

_CSS_PARTY = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Songti SC","SimSun","PingFang SC",serif;background:#7A1610;color:#F3E2C0}
.wrap{max-width:680px;margin:0 auto;padding:26px}
.frame{border:2px solid #E8C87E;padding:6px;border-radius:6px}
.inner{border:1px solid #E8C87E;border-radius:4px;padding:26px 22px;text-align:center;background:linear-gradient(180deg,#8C1D12 0%,#6B120C 100%)}
.kicker{font-size:11px;letter-spacing:6px;color:#E8C87E}
h1{font-size:29px;margin:14px 0 10px;color:#FFE9BE;letter-spacing:3px}
.divider{width:70px;height:1px;background:#E8C87E;margin:14px auto;opacity:.6}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}
.cell{background:rgba(255,255,255,.05);border:1px solid rgba(232,200,126,.4);border-radius:8px;padding:12px 8px}
.pic{width:100%;height:78px;object-fit:cover;border-radius:6px;background:rgba(255,255,255,.10)}
.pic-ph{display:flex;align-items:center;justify-content:center;font-size:26px;color:#E8C87E;font-weight:700}
.cname{font-size:12.5px;margin-top:8px;color:#FFE9BE;line-height:1.4}
.cprice{font-size:12px;color:#E8C87E;margin-top:4px}
.ribbon{margin-top:18px;font-size:13px;color:#E8C87E;letter-spacing:1px;line-height:1.9}
.foot{margin-top:20px;padding:12px 14px;border:1px dashed rgba(232,200,126,.5);border-radius:6px}
.note{font-size:11px;color:#D9BB92;line-height:1.6}
.nudge{font-size:11px;color:#BFA07A;margin-top:5px}
@media(max-width:520px){.grid{grid-template-columns:1fr}}
"""


def render_party(data):
    cells = ""
    for m in _items(data, limit=6):
        price = _pick(m, "price")
        cells += (
            '<div class="cell">'
            f'{_figure(m)}'
            f'<div class="cname">{_e(_pick(m, "name", "title"))}</div>'
            + (f'<div class="cprice">¥{_e(price)}</div>' if price else "")
            + "</div>"
        )
    ribbon = "".join(
        f"<div>◈ {_e(_pick(c, 'name', 'title'))}"
        + (f"　{_e(_pick(c, 'period', 'date'))}" if _pick(c, "period", "date") else "")
        + "</div>"
        for c in (data.get("campaigns") or [])[:4]
    )

    body = f"""
<div class="wrap"><div class="frame"><div class="inner">
  <div class="kicker">麦 麦 派 对</div>
  <h1>{_e(_pick(data, "headline", "theme", default="限定主题 · 邀你赴约"))}</h1>
  <div class="divider"></div>
  <div class="grid">{cells or '<div class="cell"><div class="cname">暂无餐品数据</div></div>'}</div>
  <div class="ribbon">{ribbon or '<div>◈ 暂无活动安排</div>'}</div>
  {_footnote()}
</div></div></div>"""
    return _page("国潮派对", body, _CSS_PARTY, "#7A1610")


# ------------------------------------------------------------------ 风格注册表

STYLES = {
    "hero": {"name": "经典主推", "scene": "新品首发 / 爆款单品主推", "render": render_hero},
    "limit": {"name": "限定夜潮", "scene": "限时、限量、夜宵场活动", "render": render_limit},
    "morning": {"name": "晨光早餐", "scene": "早段新品 / 早餐套餐推荐", "render": render_morning},
    "digest": {"name": "极简日报", "scene": "多品 + 优惠券的当日速览清单", "render": render_digest},
    "party": {"name": "国潮派对", "scene": "主题活动 / 派对预约（query-party-*）", "render": render_party},
}

DEFAULT_STYLE = "hero"


def list_styles():
    return [(k, v["name"], v["scene"]) for k, v in STYLES.items()]


def render(style_id, data):
    """按风格 ID 渲染，未知风格回退到默认风格（不抛错，保证 Skill 健壮性）。"""
    st = STYLES.get(style_id)
    if not st:
        st = STYLES[DEFAULT_STYLE]
    return st["render"](data or {})


def _page(title, body_html, css, bg):
    return (
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{_e(title)} · 麦麦新品种草官</title>"
        f"<style>{css}</style></head>"
        f"<body style='background:{bg}'>{body_html}</body></html>"
    )
