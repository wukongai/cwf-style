---
name: cwf-article-rewrite
display_name: 文章改写
display_name_zh: 文章改写
display_name_en: CWF Article Rewrite
description: Use when rewriting an existing article under an explicit preservation scope, structural rewrite mode, audience, length, and optional style-library profile.
description_zh: 当用户提供完整原文，并明确改写幅度、结构边界、受众、篇幅或可选文风档案时使用。
description_en: Use when rewriting a complete source article with an explicit preservation scope, structural mode, audience, length, or optional style profile.
author: wukongai
version: 0.1.1
---

# 文章改写

这个 Skill 只负责处理一篇已经存在的全文。它先理解原文，再明确改写档位和保留边界，随后从文风库读取一个固定版本（可不选），完成正文、变化说明和分项审阅。它不负责从作品建档；需要新文风时交给 `cwf-style-distillation`。

## 三档改写

### `preserve_structure`：保结构改写

保留篇章骨架、段落功能与先后、主线、关键材料和原意。改变句法、措辞、描写、声口和局部详略。段落数量不要求逐个相同，但组织关系必须能对应。

### `rebuild_from_thread`：保线索重构

保留主要线索、关键人物事件、核心意思、因果关系和情绪方向；允许重组篇章、段落、叙述起点、材料详略、转折和收束。写前必须列出至少两项组织关系变化，写后逐项说明。只换词或只挪开头不算完成重构。

### `rewrite_from_meaning`：取意重写

保留明确提取的核心意旨、立场、情感落点和另行锁定的真实事实。原结构、线索、场景、意象和材料组合都可以重做。解除原文元素继承义务，不解除事实来源和虚构边界。

## 固定流程

1. 读取完整原文和来源；主题摘要不能代替原文。
2. 提取事实、主张、因果、不确定性、原结构和材料功能。
3. 选择三档之一，列出必须保留、可以变化和允许新增内容。
4. 从文风库选择匹配体裁的固定档案版本；没有文风时可以普通改写。
5. 写前形成改写安排，特别说明第二档的组织关系变化或第三档的核心意旨。
6. 固定原文、事实、档位、安排、受众、篇幅和完整表达包，再生成候选。
7. 分别复核保留义务、事实与因果、越界新增、结构安排、文风符合度、自然度和用户可用性。

## 确定性检查

从仓库根目录运行：

~~~bash
PYTHONPATH=. python3 -B -m shared.cli rewrite validate --request path/to/request.json
~~~

请求必须使用 `cwf-article-rewrite-request/v1`，包含 `source.text` 的完整原文和三档之一。工具会拒绝只有摘要的输入、缺少第二档重组计划的输入以及缺少第三档核心意旨的输入。

## 交付

交付改写稿、原文到新稿的具体变化说明、档位验收、事实/原意保真、文风与自然度评阅及未解决项。一次改稿的偏好不会自动改写文风库；长期风格问题另建蒸馏版本。
