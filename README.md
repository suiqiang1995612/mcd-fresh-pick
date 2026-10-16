# 麦麦新品种草官 · MCD Fresh Pick

> 麦当劳中国程序员创意开发大赛参赛作品 · 基于麦当劳中国官方 MCP（mcd-mcp）

一个基于**麦当劳中国官方 MCP** 的 WorkBuddy Skill：实时拉取当月营销活动、在售餐品与可用优惠券，生成「今天值得尝 / 值得冲」的**新品 & 限时活动种草推荐**。

## 它能做什么

- 🆕 **新品种草**：基于 `query-meals` 实时菜单，按标签/分类挑出近期新品与特色餐品，附详情与营养亮点。
- ⏰ **限时活动提醒**：基于 `campaign-calendar` 拉取当月营销活动日历，告诉你正在进行 / 即将开始的限时活动。
- 🎟️ **省钱卖点**：自动关联 `available-coupons` / `query-store-coupons`，把可用券贴到推荐上。
- 📍 **落地到店**：用 `query-nearby-stores` 给出附近可参与门店。
- ✅ 全部基于官方实时数据，输出仅作参考；**绝不下单、绝不对比竞品、绝不诱导浪费**。

## 安装方法

### 1. 配置麦当劳 MCP 连接器

在 WorkBuddy 左侧【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】，填入：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": { "Authorization": "Bearer 你的MCP_TOKEN" }
    }
  }
}
```

Token 申请见 https://open.mcd.cn/mcp 。启用连接器后即可使用。完整脱敏配置见 `mcp-config.example.json`。

### 2. 安装本 Skill

将本仓库 `SKILL.md` 复制到 WorkBuddy 的 skills 目录：

- 用户级：`~/.workbuddy/skills/mcd-fresh-pick/`
- 项目级：`.workbuddy/skills/mcd-fresh-pick/`

刷新/重启 WorkBuddy 后，在对话中提及「新品 / 限时活动 / 种草 / 值得买」等即可触发。

## 使用示例

> 用户：麦当劳最近有什么新品和限时活动？给我种草一下
> 助手：调用 `now-time-info` → `campaign-calendar` + `query-meals` + `available-coupons` … 生成种草卡片

> 用户：附近哪家店能参加这个活动？
> 助手：调用 `query-nearby-stores` … 给出附近门店

## 目标用户

- 想第一时间知道麦当劳新品 / 限时活动的「麦门」爱好者
- 希望顺手看到可用优惠、理性种草的消费者
- 想用 AI + 官方实时数据做轻量内容推荐的创作者

## 项目结构

| 文件 | 说明 | 是否必须 |
|---|---|---|
| `README.md` | 项目介绍、安装、使用示例、目标用户 | 必须 |
| `CONTEST_DECLARATION.md` | 参赛声明（官方规定，内容不可改） | 必须 |
| `MCP_INTEGRATION.md` | 实际使用的 MCP Server / Tool / 调用流程 / 业务价值 | 必须 |
| `mcp-config.example.json` | 脱敏 MCP 配置示例（仅环境变量占位符） | 必须 |
| `workbuddy.md` | WorkBuddy 开发对话上下文（专项奖励核验用） | WorkBuddy 奖励必交 |
| `SKILL.md` | Skill 主体：触发逻辑与 MCP 编排指令 | 源代码 |
| `promo.py` | 宣传渲染引擎：md 卡片 + 多风格分发（`--style` / `--format`） | 源代码 |
| `styles.py` | 5 套「麦当劳适配」宣传视觉风格的 HTML 绘制实现 | 源代码 |

## 多种宣传风格（内置）

同一份 MCP 数据，可渲染成 5 套**适配麦当劳场景**的宣传视觉卡（`--list-styles` 查看）：

| style | 名称 | 适用场景 | 视觉基调 |
|---|---|---|---|
| `hero` | 经典主推 | 新品首发 / 爆款单品主推 | 红黄撞色、大而醒目 |
| `limit` | 限定夜潮 | 限时、限量、夜宵场活动 | 暗夜黑金、稀缺感 |
| `morning` | 晨光早餐 | 早段新品 / 早餐套餐推荐 | 奶油暖橙、清新柔和 |
| `digest` | 极简日报 | 多品 + 优惠券的当日速览 | 极简黑白、信息密度高 |
| `party` | 国潮派对 | 主题活动 / 派对预约（`query-party-*`） | 国风红金、宋体标题 |

```bash
python promo.py --list-styles
python promo.py data.json --style hero    --format html > card.html
python promo.py data.json --style limit   --format html > card.html
python promo.py data.json --style digest  --format md
```

`promo.py` 内置演示数据（均带「示例：」前缀），无需 Token 即可本地一键生成样张：

```bash
python promo.py --style hero    --format html > hero.html
python promo.py --style limit   --format html > limit.html
python promo.py --style morning --format html > morning.html
python promo.py --list-styles                      # 查看全部风格
```

生成的 HTML 直接用浏览器打开即可预览（`samples/` 预览产物不入库）。

> **合规要点**：每套风格渲染都强制带免责声明 + 「理性消费 · 适量享用」提示；产品图**只使用 MCP 工具返回的官方 URL**，无图时用纯色占位块，**绝不用 AI 生成或伪造产品图**（避免虚假宣传与商标风险）；输出无外部脚本、无第三方资源，纯离线可用。

## 合规说明

本项目为大赛参赛作品，非麦当劳官方产品。输出基于官方实时数据仅供参考，餐品 / 价格 / 供应以麦当劳官方渠道为准。详见 `CONTEST_DECLARATION.md`。
