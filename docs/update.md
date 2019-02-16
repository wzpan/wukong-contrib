# 升级

## 提示升级 ##

当有新的更新时，wukong-robot 的后台会提示升级，询问你是否需要更新：

![](http://hahack-1253537070.file.myqcloud.com/images/update.jpg)

点击更新即可自动进入更新。

## 手动升级 ##

如果提示升级失败，可以尝试在 wukong-robot 的根目录手动执行以下命令，看看问题出在哪。

``` sh
python3 wukong.py update
```

如果 wukong-robot 出现了 bug 导致无法升级，还可以用最原始的升级命令：

``` sh
cd wukong-robot的目录
git checkout master
git pull
cd wukong-contrib的目录
git checkout master
git pull
```