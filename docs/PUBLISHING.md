# cwf-style 发布与使用命令手册

> 当前仓库：[`wukongai/cwf-style`](https://github.com/wukongai/cwf-style)。`main` 已发布，最新验证提交为 `92ec766`。

## 普通用户安装

发布后，在终端运行：

~~~bash
npx skills add wukongai/cwf-style
~~~

这会从公开仓库读取可安装 Skill，并让你选择宿主和安装范围。只装文章改写 Skill 时：

~~~bash
npx skills add wukongai/cwf-style --skill cwf-article-rewrite
~~~

如果命令参数与本机版本不同，先运行 `npx skills --help`。不要把示例命令里的占位符、作者名或旧截图当作当前参数。

## 开发者检查

~~~bash
git clone https://github.com/wukongai/cwf-style.git
cd cwf-style
PYTHONPATH=. python3 -B -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=. python3 -B -m shared.cli library list --index library/index.json
git diff --check
git status --short
~~~

`git clone` 下载源码；`cd` 进入目录；`python3 -B` 运行测试且不写字节码缓存；`library list` 检查文风库是否能读取；`git diff --check` 检查空白错误；`git status --short` 查看是否有未保存改动。

## 维护者发布前

只发布以下内容：

- `skills/` 下两个 Skill 的说明和必要参考；
- `library/` 下已授权公开的档案、文风卡和合成预览；
- `shared/` 的确定性合同工具；
- `tests/`、`README.md`、版本说明和许可证。

不要发布真实文章、私有样本、用户资料、`.env*`、Token、Cookie、私钥、`.backups/`、`.skill-engineering/` 或内部绝对路径。发布前逐条检查：

~~~bash
git status --short
git diff --check
git ls-files
gh auth status --hostname github.com
git remote -v
git ls-remote --heads origin
~~~

`gh auth status` 只检查登录状态；不读取或打印 Token。不要执行 `gh auth logout`，不要删除 GitHub hosts 文件、Keychain 凭证或全局 credential helper。

## 首次推送

只有在许可证、所有者、仓库名、公开性、认证和网络都已确认后，才执行：

~~~bash
git add README.md VERSION skill.contract.yaml skills library shared tests docs .gitignore
git commit -m "feat: publish standalone cwf style skills"
git push -u origin main
~~~

`git add` 只加入发布白名单；`git commit` 保存候选版本；`git push -u origin main` 推送到已核对的独立远程。不要在当前 CWF 总工程里执行 `git add .`，也不要把未知远程当作目标。

## 更新与回滚

更新前：

~~~bash
git status --short
git pull --ff-only
~~~

普通用户回滚优先重新安装已确认的版本标签或提交。维护者回滚优先使用新的 `git revert` 提交，避免用 `git reset --hard` 丢失本地内容。

## 当前验证结果

- 远程仓库：`https://github.com/wukongai/cwf-style`
- 远程 `main`：`92ec766ab2e4018482a15d45eb527e8c8e617e70`
- 从远程全新克隆后，11 项回归测试全部通过。
- `npx skills add wukongai/cwf-style --skill cwf-style-distillation --skill cwf-article-rewrite -a codex -y` 在临时项目中成功安装两个 Skill。
- 许可证仍需单独决定；公开仓库可访问不等于已经授予特定开源许可。
