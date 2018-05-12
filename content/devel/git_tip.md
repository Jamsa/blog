Title: Git Tips
Date: 2018-05-12
Modified: 2018-05-12
Category: 开发
Tags: git

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
 
 
