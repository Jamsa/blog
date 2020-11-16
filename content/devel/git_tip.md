---
title: "Git Tips"
date: 2018-05-12
modified: 2018-05-12
categories: ["开发"]
tags: ["git"]
---

 - 强制本地回退至指定版本
 
 ```
 git reflog
 git reset --hard oxfb
 ```
 
 - 强制远程回退至指定版本
 
 先强制本地回退，然后强制推送。
 
 ```
 git push -f
 ```
 
 
