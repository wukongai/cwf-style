# 发布验收清单

- [x] 双 Skill 目录和触发边界独立存在
- [x] 文章改写三档合同通过正反例
- [x] 文风库能列出、读取和拒绝不可调用条目
- [x] 文风档案没有私有原文、内部路径或凭证
- [x] `PYTHONPATH=. python3 -B -m unittest discover -s tests -p 'test_*.py'` 通过
- [x] `git diff --check` 通过
- [x] `git ls-files` 与白名单逐项一致
- [x] MIT 许可证已加入仓库
- [x] `gh auth status --hostname github.com` 成功
- [x] `git ls-remote --heads origin` 成功
- [x] 推送后读取远程提交并记录真实 URL
- [ ] 真实任务效果、用户阅读和跨模型结果单独记录，不由静态测试代替
