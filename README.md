# cwf-style

独立的文风工具仓库：把**文风蒸馏**和**文章改写**拆成两个 Skill，并通过同一个文风库交接。

本仓库与 CWF 总工程分开维护，可以单独发布、安装和升级。远程仓库：[wukongai/cwf-style](https://github.com/wukongai/cwf-style)。当前 `main` 已发布，版本为 `0.1.1`。

## 仓库内容

- `skills/cwf-style-distillation/`：从公开作品或经确认的本人材料形成完整文风档案。
- `skills/cwf-article-rewrite/`：处理已有全文，支持三档改写：保结构改写、保线索重构、取意重写。
- `library/`：共享文风卡、完整档案和版本索引。文风库不写文章，也不替任务选择改写档位。
- `shared/`：两个 Skill 共用的确定性合同和读取工具。
- `tests/`：文风库、蒸馏合同、改写合同和公共包边界测试。
- `docs/`：面向维护者和公共使用者的操作手册。

## 两个 Skill 怎样协作

```text
作品/本人材料
    ↓
cwf-style-distillation
    ↓
固定版本的文风档案
    ↓
library/ 文风库
    ├── cwf-article-rewrite 读取文风，改写已有文章
    └── 其他原创写作流程读取文风，写新文章
```

蒸馏不负责日常改稿；改写不负责重新研究作者。改写的三档只属于文章改写任务，不属于文风档案。

## 三档改写

| 档位 | 需要保留 | 允许变化 |
| --- | --- | --- |
| `preserve_structure` 保结构改写 | 篇章骨架、段落功能顺序、主线、关键材料和原意 | 句法、措辞、描写、声口和局部详略 |
| `rebuild_from_thread` 保线索重构 | 主要线索、关键人物事件、核心意思、因果和情绪方向 | 叙述起点、段落组织、详略、转折和结尾回收 |
| `rewrite_from_meaning` 取意重写 | 核心意旨、立场、情感落点及另行锁定的真实事实 | 原结构、线索、场景、意象、材料组合和语言 |

保线索重构必须在写前列出组织关系变化，写后说明开篇、推进、转折和收束怎样重新分工。只换词不算结构重构。

## 本地检查

在仓库根目录运行：

~~~bash
PYTHONPATH=. python3 -B -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=. python3 -B -m shared.cli library list --index library/index.json
git diff --check
git status --short
~~~

测试通过表示合同与包边界通过，不代表某种文风已经获得用户认可或证明能复现作者。

## 安装和发布

Codex 用户可以运行：

~~~bash
npx skills add wukongai/cwf-style
~~~

只安装文章改写 Skill 时：

~~~bash
npx skills add wukongai/cwf-style --skill cwf-article-rewrite
~~~

完整发布顺序、认证安全、白名单和回滚见 [发布与使用手册](docs/PUBLISHING.md)。

WorkBuddy 用户请按 [WorkBuddy 安装与验证](docs/WORKBUDDY.md) 操作。当前 `npx skills` 没有 WorkBuddy 适配器，因此 WorkBuddy 使用用户级 Skill 目录安装。

## 当前状态

这是 `0.1.1` 发布版本。远程克隆、11 项回归测试、两个 Skill 的 Codex 安装和 WorkBuddy 用户目录安装检查已验证通过；真实文风效果仍需按具体文风和题材继续评估。
