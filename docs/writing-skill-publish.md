# 发布技能

技能开发完后，可以申请发布你的技能，让别人也能用上你的杰作。但在开始之前，请先阅读以下这份发布前的 checklist ，确保符合规范：

## 技能插件发布前 checklist ##

1. 你的插件没有跟其他插件有命名冲突，甚至最好不要有 `isValid()` 判断规则的交叉。比如如果你正在写一个“豆瓣电台”插件，而已经有一个“百度电台”插件，那么技能的关键词就应该用“豆瓣电台”，而不是“电台”，以免影响后者的使用。
2. 严格使用 Python 3 语法编写，也不再使用 `sys.setdefaultencoding('utf8')` ；
3. 如果依赖第三方库，则务必将其写进 `requirements.txt` 。但有一个例外：wukong-robot 的目的是能跑在尽可能多的设备上，所以一些平台特定的库（例如GPIO、wiringpi等）请先在 `isValid` 方法中引用以确认可用，例如：

    ``` python
    def isValid(text):
        try:
            import wiringpi
            return u"台灯" in text
        except Exception:
            return False
    ```

这类库不要写入 `requirements.txt` 文件中，而是放在该插件的相应 wiki 说明中，由需要的人按需安装。
4. 技能插件发布阶段，插件中如果包含 `utils.getUnit()` 的调试代码，则必须删除。并在 Merge Request 中备注这个的技能的 UNIT 分享码。

### 技能插件发布流程

1. fork 本项目；
2. 添加你的插件；
3. 如果你的插件有依赖第三方库，将依赖项添加进 requirements.txt 。如果依赖第三方工具, 则在 README 中的[安装](#安装) 一节中补充。
4. 在 docs/contrib.md 中，参考其他插件的说明，写好你的插件的说明文档。
5. 发起 pull request ，说明该插件的用途、指令和配置信息（如果有的话）。
