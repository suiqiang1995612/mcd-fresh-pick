# WorkBuddy 开发上下文（workbuddy.md）

> 本文件用于核验本项目是否真实使用腾讯 WorkBuddy 智能体开发，符合麦当劳程序员创意开发大赛「WorkBuddy 专项奖励」的联动条件。

## 项目信息

- **项目名称**：麦麦新品种草官（MCD Fresh Pick）
- **类型**：WorkBuddy Skill（AI 编排类，调用麦当劳中国官方 MCP）
- **主题**：新品 & 限时活动种草推荐
- **创建时间**：2026-10-16
- **开发工具**：腾讯 WorkBuddy（Agent 模式，直接对话生成项目骨架与源码）

## 开发过程（与 WorkBuddy 的对话脉络）

1. **需求确认**：用户提出「登录 GitHub 搜索 McDonald's China(M-China) 查看赛事规则」。
   - WorkBuddy 通过 GitHub 连接器检索到官方组织 `M-China` 与活动仓库 `M-China/mcd-developer-innovation-challenge`，拉取 `README.md` / `activityGuidelines.md` / `CONTEST_DECLARATION.md`，整理出赛事规则摘要（时间线、报名文件清单、排名规则、奖励、合规红线）。

2. **方向对齐**：用户确认「从零搭一个参赛 Skill」。
   - WorkBuddy 就「产品宣传」主题做合规研判：结论为合规，但须真实调用 MCP、不对比竞品、不诱导浪费、基于实时数据 + 免责声明。
   - 用户选定角度：**新品 & 限时活动种草**。

3. **MCP 能力调研**：WorkBuddy 拉取官方 `M-China/mcd-mcp-server` 的 `README.md` 工具列表，确认可用 Tool：`campaign-calendar`、`query-meals`、`query-meal-detail`、`list-nutrition-foods`、`available-coupons`、`query-store-coupons`、`query-nearby-stores`、`now-time-info` 等，据此设计调用流程。

4. **产出项目骨架**（本仓库）：
   - `README.md`、`CONTEST_DECLARATION.md`（官方原文未改）、`MCP_INTEGRATION.md`、`mcp-config.example.json`（仅 `${MCD_MCP_TOKEN}` 环境变量占位符）——满足活动「必须文件」要求。
   - `SKILL.md`：Skill 触发与 MCP 编排指令（主体源码）。
   - `promo.py`：宣传渲染引擎（md 卡片 + `--style` 多风格分发 + `--format md|html`）。
   - `styles.py`：5 套「麦当劳适配」宣传视觉风格的 HTML 绘制实现。
   - `workbuddy.md`：本文件。

5. **多风格宣传渲染**：用户追加需求「内置多种适配于麦当劳的产品宣传风格绘制」。
   - WorkBuddy 新增 `styles.py`，实现 `hero` / `limit` / `morning` / `digest` / `party` 五套风格（各自配色与版式），
     并把 `promo.py` 改造为渲染引擎，追加 `--style` / `--format md|html` / `--list-styles`。
   - 合规取舍：产品图**只使用 MCP 返回的官方 URL**，无图用纯色占位块，**拒绝 AI 伪造产品图**；
     每套风格强制注入免责声明与「理性消费 · 适量享用」提示；输出无 `<script>`、无外部资源。

6. **上线提交**：WorkBuddy 通过 GitHub 连接器将全部文件推送至公开仓库 `suiqiang1995612/mcd-fresh-pick`，
   并向官方活动仓库 `M-China-Official/mcd-developer-innovation-challenge` 提交报名 Issue。
   （注：官方组织已从 `M-China` 改名重定向至 `M-China-Official`，两者为同一仓库。）

## 真实使用 WorkBuddy 智能体的证据点

- 通过 WorkBuddy 内置 GitHub 连接器完成官方仓库检索与文件读取，而非手动复制。
- 在 WorkBuddy 对话中以 Agent 模式逐轮迭代生成全部 8 个交付文件（含源码与合规声明）。
- 项目设计严格遵循 WorkBuddy 官方文档的 MCP 连接器配置方式（`streamablehttp` + Bearer Token）。

## 合规自检

- ✅ 真实使用麦当劳中国 MCP（`mcd-mcp`）能力。
- ✅ 真实使用腾讯 WorkBuddy 智能体开发。
- ✅ 配置文件仅含环境变量占位符，无真实 Token / 密钥。
- ✅ 输出基于官方实时数据、加免责声明、不对比竞品、不诱导浪费。
- ✅ 不 AI 伪造产品图（仅用 MCP 官方图片 URL，否则占位块），规避虚假宣传与商标风险。
- ✅ 仓库为 Public，创建时间在活动窗口（2025-12-25 ~ 2026-10-25）内。
