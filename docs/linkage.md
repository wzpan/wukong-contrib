# 与其他智能音箱联动

## Siri

<center>
    <iframe src="//player.bilibili.com/player.html?aid=653231978&bvid=BV1yY4y1y7oW&cid=1044940521&page=1" scrolling="no" border="0" frameborder="no" framespacing="0"  width="80%" height="360px" allowfullscreen="true"> </iframe>
</center>

通过 Siri 捷径可以实现和 wukong-robot 的联动。步骤：

1. 启动 Siri 捷径应用；
2. 点击 + 号按钮，创建一个新的捷径，名为 “传我指令” ；
3. 在搜索框中搜索 “URL” ，创建一个 “URL” 操作。地址为 `你的wukong-robot的地址/chat` ，例如：

    ![创建捷径](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/siri-step1.jpeg)

   上面这个 `URL` 其实就是我们要发给 wukong-robot 的 [`/chat`](/api?id=对话) API 的地址。

4. 接下来我们再尝试调用这个 API 。在搜索框中搜索 “获取URL内容” ，创建一个 “获取URL内容” 操作。将方法改为 “POST”，将请求体改为 “表单” ，并增加 `type`，`query`，`validate`，`uuid` 四个键值对。其中：
    - `type` 的值设为 `text` ，表示我们要让 siri 用文本指令传递给 wukong-robot 实现联动；
    - `query` 表示具体的指令文本，这个可以通过 Siri 捷径里自带的 “听写文本” 操作来进一步获取；
    - `validate` 是 wukong-robot 的后端密码的 md5，与你的配置文件中的 `validate` 项目配置一致。如果你没有改过，默认就是 `f4bde2a342c7c75aa276f78b26cfbd8a` 。（老生常谈：为了安全，强烈建议在 `config.yml` 里修改这个值！这里仅是示例。）
    - `uuid` 是为这次 query 赋予的一个 uuid。我们可以想办法赋予一个随机数。

    ![创建“获取URL内容”操作](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/siri-step1.5.jpeg)

5. 在第4步中我们还遗留 `query` 和 `uuid` 没有获取。依次搜索添加 “随机数” 和 “听写文本” 操作并将值赋给这两个键即可完成操作。最终的捷径如图所示：

    ![完成请求](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/siri-step2.jpeg)

完成上面的配置后，点击执行按钮，然后允许接下来弹出来的语音识别和网页访问权限申请弹窗。看看 wukong-robot 是否正确反应吧。如果 wukong-robot 能够正确执行指令，再试试通过下面的步骤完成更自然的交互：

1. 说 “嘿Siri” 唤醒 Siri
2. 说 “传我指令” 激活这个捷径
3. 在 Siri 问出 “文本是什么？” 后，进一步说出需要 wukong-robot 响应的指令。

## 小爱音箱

使用 [xiaoai-wukong](https://github.com/wzpan/xiaoai-wukong) 可以实现小爱音箱和 wukong-robot 的联动，将小爱音箱作为 wukong-robot 的备用唤醒装置。

详细使用方法：参考 [xiaoai-wukong](https://github.com/wzpan/xiaoai-wukong) 的 README 即可。

联动小爱音箱的原理其实很简单：逆向了小爱音箱的服务端协议，轮询抓取最近的聊天记录然后分析是否需要 wukong-robot 响应的指令，有的话就再转发给wukong-robot。缺点是响应比较慢（需要等云端有更新聊天记录，下一个轮询时机才能做出响应）。