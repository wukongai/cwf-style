# 共用文风库

`index.json` 是唯一入口。每个可调用条目都指向一个固定版本的完整文风档案和一个可读预览。

- `status` 表示证据与验证阶段：`draft`、`research_trial`、`scenario_validated`、`user_confirmed`、`archived`。
- `availability` 表示能否被消费者读取：只有 `callable` 才能被文章改写或原创写作调用。
- 文风卡不复制规则；规则只在档案中维护。
- 作者名、研究状态和用户认可度分开记录；公开研究不伪装成作者确认。
- 私有档案不因放入共享库而扩大访问权限。

从仓库根目录读取：

~~~bash
PYTHONPATH=. python3 -B -m shared.cli library list --index library/index.json
PYTHONPATH=. python3 -B -m shared.cli library show --index library/index.json --style-id cwf-wang-life-prose-personality --genre 生活散文
~~~
