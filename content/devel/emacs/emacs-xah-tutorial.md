Title: Xah的Emacs Lisp 教程学习笔记
Date: 2008-03-10
Modified: 2008-03-10
Category: emacs
Tags: emacs

# 例子
```emacs-lisp
(defun zj-open-directory-with-explorer ()
  "在windows中用explorer浏览当前目录"
  (interactive)
  (shell-command "explorer.exe .")
  (browse-url "www.google.cn")
  )

(defun zj-display-directory-files ()
  "执行shell命令并处理它的输出。这里为显示当前目录下的文件"
  (interactive)
  (message (shell-command-to-string "ls -l"))
  )

(defun zj-display-current-major-mode ()
  "如果当前为emacs-lisp-mode则显示当前主模式"
  (interactive)
  (if (eq 'emacs-lisp-mode major-mode)
      (message "emacs-lisp-mode"))
  )

(defun zj-regexp-match ()
  "正则表达式匹配"
  (interactive)
  (let ((test-string "aaaaaaaaaaaa123sfdsfs456")
        (regexp-string "\\([0-9]+\\)[a-z]+\\([0-9]+\\)"))
    (string-match regexp-string test-string)
    (message (concat (match-string 1 test-string) "--" (match-string 2 test-string) ))
    )
  )

(defun dos2unix (file-path)
  "dos换行转unix换行"
  (let (mybuffer)
    (setq mybuffer (find-file file-path))
    (replace-string "\r\n" "\n" nil 1 (1+ (buffer-size)))
    (save-buffer)
    (kill-buffer mybuffer)
    )
  )

(defun zj-insert-p ()
  "在光标位置插入<p></p>"
  (interactive)
  (insert "<p></p>")
  (backward-char 4))

(defun zj-wrap-paragraph (start end)
  "在区域前后加<p></p>"
  (interactive "r")
  (goto-char end) (insert "</p>")
  (goto-char start) (inster "<p>")
  )

(defun zj-replace-html-chars-in-region (start end)
  "将特殊字符转成html中的符号"
  (interactive "r")
  (save-restriction
    (narrow-to-region start end)
    (goto-char (point-min))
    (while (search-forward "&" nil t)(replace-match "&amp;" nil t))
    (goto-char (point-min))
    (while (search-forward "&" nil t)(replace-match "&amp;" nil t))
    (goto-char (point-min))
    (while (search-forward "&" nil t)(replace-match "&amp;" nil t))
    )
  )

(defun zj-hash-test ()
  "hash table 测试"
  (interactive)
  (let (myhash val)
    ;; 创建hash table并告诉elips用equal来测试key是否存在
    (setq myhash (make-hash-table :test 'equal))

    ;; 添加数据
    (puthash "mary" "19" myhash)
    (puthash "jane" "19" myhash)
    (puthash "liz" "19" myhash)
    (puthash "zj" "19" myhash)


    ;; 修改数据
    (puthash "zj" "27" myhash)

    ;; 删除数据
    (remhash "liz" myhash)

    ;; 获取数据
    (setq val (gethash "zj" myhash))
    (message val)
    )
  )

```
