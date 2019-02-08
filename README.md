# wukong-contrib

[![wukong-project](https://img.shields.io/badge/project-wukong-informational.svg)](https://github.com/users/wzpan/projects/1)

[wukong-robot](http://github.com/wzpan/wukong-robot) 的第三方技能插件。

除了 [Weather](https://github.com/wzpan/wukong-contrib/wiki/weather) 插件之外，其余插件均为用户贡献，因此并不保证完全可用。

* [插件列表](https://github.com/wzpan/wukong-contrib/wiki)

## 安装

``` sh
cd $HOME/.wukong
git clone http://github.com/wzpan/wukong-contrib contrib
pip install -r contrib/requirements.txt
```

## 升级

``` sh
cd /home/pi/.wukong/contrib
git pull
pip install --upgrade -r requirements.txt
```

## 如何贡献

### 教程

wukong-robot 的插件机制基本和 dingdang-robot 相同，所以可参照 [手把手教你编写叮当机器人插件](http://www.hahack.com/codes/how-to-write-dingdang-plugin/) 教程编写插件。不过要注意区别：

1. 无需再定义 `WORDS` 常量，不再支持 wxBot 参数，另外 `profile` 参数改成从 `robot.config` 中获取；
2. 严格使用 Python 3 语法编写，也不再使用 `sys.setdefaultencoding('utf8')` ；
3. 和 dingdang-robot 主要面向树莓派不同，wukong-robot 的目的是能跑在尽可能多的设备上，所以一些平台特定的库（例如GPIO、wiringpi等）请在 `isValid` 方法中引用，例如：

    ``` py
    def isValid(text):
        try:
            import wiringpi
            return u"台灯" in text
        except Exception:
            return False
    ```
  
  这类库不要写入 `requirements.txt` 文件中，而是放在该插件的相应 wiki 说明中，由需要的人按需安装。

### 流程说明

1. fork 本项目；
2. 添加你的插件；
3. 如果你的插件有依赖第三方库，将依赖项添加进 requirements.txt 。如果依赖第三方工具, 则在 README 中的[安装](#安装) 一节中补充。
4. 发起 pull request ，说明该插件的用途、指令和配置信息（如果有的话）。
5. pull request 被 accept 后，在本项目 [Wiki页](https://github.com/dingdang-robot/dingdang-contrib/wiki/neteasemusic) 中添加一项，将该插件的用途、指令和配置信息也添加到此页面中。

### 插件规范

* 每个插件只能包含一个 .py 文件。依赖的其他库文件不得放进本仓库中，否则会被当成插件而解析出错。如果确实需要分成多个文件，可以将其他文件打包发布到 PyPi ，然后将依赖加进 requirements.txt 中。
