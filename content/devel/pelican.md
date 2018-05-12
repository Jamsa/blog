Title: Pelican 静态博客
Date: 2018-05-12
Modified: 2018-05-12
Category: 开发
Tags: python

## 重新整理博客

## 草稿
```
Status: draft
```

## 静态文件发布
`直接使用 make github 会把生成的内容发布至 github 仓库`，如果你希望在 github 上保存 blog 源码就会被覆盖。

我是直接在 output 目录下新建仓库，发布至 github pages。
```
cd output
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/xxx/xxx.github.io.git
git push -u origin master
```
