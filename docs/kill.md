# 退出

要退出 wukong-robot ，根据当前情况的不同有不同的方式：

## 如果 wukong-robot 正在前台工作

可以直接按组合键 `Ctrl+4` 即可。在 Mac 系统下可能会弹出诸如 “Python 已停止工作” 的警告，仅仅只是系统的提示，不必理会。

## 如果 wukong-robot 正在后台工作

可以执行如下命令：

``` bash
ps auwx | grep wukong  # 查看wukong的PID号
kill -9 PID号
```
