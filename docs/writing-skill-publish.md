# 发布技能

技能开发完后，可以申请发布你的技能，让别人也能用上你的杰作。但在开始之前，请先阅读以下这份发布前的 checklist ，确保符合规范：

## 技能插件发布前 checklist ##

1. 你的插件应该能够完成预期的功能，没有明显的bug；
2. 你的插件没有跟其他插件有命名冲突，甚至最好不要有 `isValid()` 判断规则的交叉。比如如果你正在写一个“豆瓣电台”插件，而已经有一个“百度电台”插件，那么技能的关键词就应该用“豆瓣电台”，而不是“电台”，以免影响后者的使用；
3. 严格使用 Python 3 语法编写，也不再使用 `sys.setdefaultencoding('utf8')` ；
4. 在 Merge Request 中备注这个的技能的 UNIT 分享码。如果这个技能有相应的自定义 UNIT 技能，记得也要到百度 UNIT 先分享这个技能得到一个分享码。

  ![自定义技能需要提供一个分享码](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/share-skill.png)

5. 如果依赖第三方库，则务必将其写进 `requirements.txt` 。但有一个例外：wukong-robot 的目的是能跑在尽可能多的设备上，所以一些平台特定的库（例如GPIO、wiringpi等）请先在 `isValid` 方法中使用 `importlib.util.find_spec()` 方法确认该库是否可用，例如：

    ``` python
    import importlib  # 用来判断模块是否存在

    ...

    def isValid(text):
        return importlib.util.find_spec('wiringpi') and \
              "台灯" in text
    ```

然后在 `handle()` 或者其他真正需要使用到这些库的的地方再 `import` 。

同时这类库不要写入 `requirements.txt` 文件中，而是放在该插件的相应 wiki 说明中，由其他用户按需安装。

### 技能插件发布流程

插件正常工作后，可以将该插件发布到 [wukong-contrib](https://github.com/wzpan/wukong-contrib) ，让更多人用上您的插件。

首先先对你的插件过一下 [checklist](writing-skill-publish?id=%e6%8a%80%e8%83%bd%e6%8f%92%e4%bb%b6%e5%8f%91%e5%b8%83%e5%89%8d-checklist) ，确认符合发布规范。

然后，将这个插件挪至 `$HOME/.wukong/contrib` 目录中，并且编辑 `$HOME/.wukong/contrib/docs/contrib.md` ，参考其他技能的编写范例，在后面添加一个新条目介绍你的技能。

接下来，访问 [wukong-contrib 的 Github 主页](https://github.com/wzpan/wukong-contrib) ，点击右上角的 【fork】 按钮，将仓库 fork 到自己的账户。如果之前已经 fork 过，这一步可以跳过。

fork 完仓库后，在您的账户下也会有一个 wukong-contrib 项目，点击绿色的 【Clone or download】 按钮，记下新的仓库的地址。

![复制新的仓库地址](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/wukong-contrib-forks.png)

之后在你装有 wukong-robot 的设备中执行如下命令，添加新的仓库地址：

``` bash
cd ~/.wukong/contrib
git remote add mine 新的仓库地址
```

将新建的插件提交推送到您的 wukong-contrib 仓库中：

``` bash
git add Weather.py
git commit -m "feat(plugins): 新增天气查询插件"
git push -u mine master
```

完成后访问您的 wukong-contrib 仓库主页，可以看到一个创建 pull request 的提示：

![创建pull request的提示](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/pull-request-hint.png)

点击 【compare and pull request】 按钮，进入 pull request 创建页面，申请将您的改动合并到 wukong-contrib 项目中：

![创建一个 pull request](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/new-pull-request.png)

在里头认真填写插件的相关信息。模板如下：

<pre class="lang-yaml">
* 用于查询天气情况。数据来自 [心知天气API](https://www.seniverse.com/doc)。

### 交互示例

- 用户：天气
- 悟空：深圳天气。今天：晴。最高气温：25～30摄氏度；明天：晴。26～31摄氏度；
后天：小雨。最高气温：23～29摄氏度。

### 配置

``` yaml
# 天气
# 使用心知天气的接口
# https://www.seniverse.com/
weather:
    key: '心知天气 API Key'
```

### UNIT技能

* 分享码 -- 8zsro1  # 技能分享码。如果只用了预置技能或者没使用UNIT，不用填
* 预置技能ID -- 无  # 如果只用了自定义技能或者没使用UNIT，不用填
</pre>

不难发现就是你刚刚插进 `contrib.md` 里的内容再加上一段 UNIT 技能的相关说明。

完成后点击 【Create pull requset】 ，完成创建，等待 [wukong-robot](https://github.com/wukong-robot) 项目管理员的审核。如果你的插件包含自定义 UNIT 技能，在这段期间，管理员还会对你的 UNIT 技能进行测试，确认没问题后也会添加进 wukong-robot 的 UNIT 机器人中。

![创建一个 pull request](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/pull-request-created.png)

一旦审核通过，您的插件就发布成功了。

