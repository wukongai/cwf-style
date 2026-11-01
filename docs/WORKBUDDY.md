# WorkBuddy 安装与验证

本仓库可以作为 WorkBuddy 的用户级 Skill 使用。WorkBuddy 当前没有被 `npx skills` 支持的安装器参数，因此采用 WorkBuddy 的用户 Skill 目录安装方式。

## 普通用户安装

先下载仓库 ZIP，解压后在终端执行：

```bash
mkdir -p "$HOME/.workbuddy/skills/cwf-style-distillation" "$HOME/.workbuddy/skills/cwf-article-rewrite"
cp -R cwf-style/skills/cwf-style-distillation/. "$HOME/.workbuddy/skills/cwf-style-distillation/"
cp -R cwf-style/skills/cwf-article-rewrite/. "$HOME/.workbuddy/skills/cwf-article-rewrite/"
```

`mkdir -p` 创建 WorkBuddy 用户级 Skill 目录；`cp -R` 将两个 Skill 的 `SKILL.md`、`references.md` 和 `skill.contract.yaml` 一起复制进去。把 `cwf-style` 换成你解压后的仓库目录名。

安装后完全退出并重新打开 WorkBuddy。新建任务后可以直接说：

```text
请使用 cwf-style-distillation，从我提供的两组公开作品中整理一张文风档案。
```

或：

```text
请使用 cwf-article-rewrite，保留主要线索并重组这篇文章，调用文风库中的汪曾祺生活散文档案。
```

## 检查是否被发现

重启 WorkBuddy 后，运行：

```bash
test -f "$HOME/.workbuddy/skills/cwf-style-distillation/SKILL.md"
test -f "$HOME/.workbuddy/skills/cwf-article-rewrite/SKILL.md"
```

两个命令都没有输出且退出码为 0，表示文件已经落在 WorkBuddy 的用户 Skill 目录。是否被当前版本加载，还要在 WorkBuddy 新会话中用上面的最小任务确认。

## 当前边界

- WorkBuddy 的 `skill.contract.yaml` 提供入口、版本、输入输出、停止条件和审批边界。
- 本 Skill 不含脚本、网络请求或凭证读取。
- WorkBuddy 的真实任务效果仍需按具体文风和题材单独复核；安装通过不等于文风效果已经得到用户认可。
