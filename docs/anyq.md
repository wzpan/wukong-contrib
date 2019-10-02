# AnyQ #

[AnyQ](https://github.com/baidu/AnyQ) 是百度开源的面向FAQ集合的问答系统框架。wukong-robot 支持使用 AnyQ 作为问答机器人，并支持在没命中的情况下再使用其他机器人进行兜底（可选）。

## 安装 AnyQ ##

详见 [AnyQ 安装](/install?id=anyq-%e5%ae%89%e8%a3%85) 。

## 配置 AnyQ ##

在配置文件中，与 AnyQ 相关的配置如下：

``` yaml
# 聊天机器人
# 可选值：
# anyq      - anyq
# tuling    - 图灵机器人
# emotibot  - 小影机器人
robot: anyq

# AnyQ 机器人
anyq:
    host: 0.0.0.0
    port: 8999
    solr_port: 8900  # solr 的端口号
    # 置信度（confidence）需达到的阈值，
    # 达不到就认为不命中
    threshold: 0.6
    # 如果没有命中，使用其他兜底的机器人
    # 如果不想使用兜底，可以设为 null
    secondary: tuling
```

- 在第 6 行中，我们可以设置聊天机器人为 `anyq` 。
- 在第 10~12 行中，我们需要设置 AnyQ 服务的 ip 地址、端口号以及 solr 引擎的端口号（如果你没改过的话，AnyQ 和 solr 的端口号默认分别是 8999 和 8900 ）。
- 在第 15 行中，我们设置只有达到 0.6 以上的置信度的才认为命中该问题，并给出该问题的相应答案。
- 在第 18 行中，我们可以指定没有命中任何问题时，使用另一个聊天机器人作为兜底。如果设置为 `null` 的话，就直接返回类似 “抱歉，我不会这个呢” 的回答。

?> 将 `secondary` 设为 `null` 可以有效提升对话的响应速度，适用于那些核心诉求并不是闲聊的用户。

## QA 集配置 ##

wukong-robot 的后台管理端提供了 QA 集的编辑界面：

![](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/qa.png)
每个 QA 对使用`问题	答案`的形式（注意中间是使用 `TAB` 键敲出的制表符）。

如果有多个相似问题，可以起多行来记录，例如：

``` csv
你喜欢做什么？	我喜欢听音乐，你呢？
你的兴趣是什么？	我喜欢听音乐，你呢？
```

如果同类问题有多个候选回答，则答案可以使用列表的形式 `["答案1", "答案2", "答案3"]` 。注意 `[`, `"`，`,`, `]` 都要求为半角字符。

✅正确的写法：

``` csv
你是谁	["我是孙悟空！", "我是花果山水帘洞美猴王齐天大圣孙悟空！"]
```

❌错误的写法：

``` csv
你是谁	[“我是孙悟空！”, “我是花果山水帘洞美猴王齐天大圣孙悟空！”]
你是谁	["我是孙悟空！"，"我是花果山水帘洞美猴王齐天大圣孙悟空！"]
你是谁	【"我是孙悟空！", "我是花果山水帘洞美猴王齐天大圣孙悟空！"】
```

完成后需要点击下方的 【提交】 按钮提交 QA 集，等 solr 的索引重建完成后（大概 10 秒的时间）即会生效。

!> **如果使用 docker 安装 AnyQ ，每次重启 docker 后镜像内的数据会被重置**。需要在 QA 集页面里点击 【提交】 按钮触发重建一次索引才会恢复原来的聊天能力。

## 贡献 QA 集 ##

如果你添加了一些不错的 QA 集，欢迎提交 Pull Request ，帮助 wukong-robot 变得更加智能。

但在提交 PR 前请注意 QA 集里的内容：

- 不得包含反动、色情、暴力的信息；
- 不得存在讽刺、暗示、煽动等恶意内容；
- 不得包含实事政治等敏感内容，例如 “现任美国总统是谁” 这种存在维护成本的问题；
- 不得包含容易引起圣战的内容，例如 “PHP是最好的语言”、“Emacs 是最好的编辑器”、“周杰伦最牛逼”、“蔡徐坤最牛逼” 等；
- 不得包含过于私人的信息。例如 “你爸爸是谁” —— “张三”；“告诉我世界上最美的女孩是谁” —— “李四” 。

如果你的问答集中有若干条可能触碰了以上的几种禁忌，请在提交 PR 前删除这些条目。

### QA 集贡献流程 ###

接下来，访问 [wukong-robot 的 Github 主页](https://github.com/wzpan/wukong-robot) ，点击右上角的 【fork】 按钮，将仓库 fork 到自己的账户。如果之前已经 fork 过，这一步可以跳过。

fork 完仓库后，在您的账户下也会有一个 wukong-contrib 项目，点击绿色的 【Clone or download】 按钮，记下新的仓库的地址。

之后在你装有 wukong-robot 的设备中执行如下命令，添加新的仓库地址：

``` bash
cd wukong-robot的目录
git remote add mine 新的仓库地址
```

将你的 QA 集拷贝回 wukong-robot 仓库里并提交：

``` bash
cp ~/.wukong/qa.csv static/qa.csv
git add static/qa.csv
git commit -m "feat(QA): 新增QA数据集"
git push -u mine master
```

完成后访问您的 wukong-robot 仓库主页，可以看到一个创建 pull request 的提示。点击 【compare and pull request】 按钮，进入 pull request 创建页面，申请将您的改动合并到 wukong-robot 项目中。在里头简单填写下新增的内容即可。

一旦审核通过，你贡献的 QA 集就发布成功了。
