;; batch 模式下 org mode 发布时，htmlize无效
;;(add-to-list 'load-path "/Users/zhujie/.emacs.d/elpa/color-theme-20080305.34")
(add-to-list 'load-path "/Users/zhujie/.emacs.d/elpa/htmlize-20171017.141")

;;(require 'color-theme)
;;(require 'htmlize)
;;(load-theme 'wombat t)
;;(setq org-src-fontify-natively t)
;;(setq org-html-htmlize-output-type 'inline-css)

;设置可参考：https://github.com/nhoffman/org-export/blob/master/org-export-pelican.el

(require 'ox)
;; 执行src代码块时，不需要确认
(setq org-confirm-babel-evaluate nil)

(setq org-export-htmlize-output-type 'css)
(org-babel-do-load-languages
 'org-babel-load-languages
 '((dot . t)
   (python . t)
   (emacs-lisp . t)
   (sh . t)))

;(setq org-html-htmlize-output-type nil)
;; 用highlight.js处理语法高亮
(defun rasmus/org-html-wrap-blocks-in-code (src backend info)
  "Wrap a source block in <pre><code class=\"lang\">.</code></pre>"
  (when (org-export-derived-backend-p backend 'html)
    (replace-regexp-in-string
     "\\(</pre>\\)" "</code>\n\\1"
     (replace-regexp-in-string "<pre class=\"src src-\\([^\"]*?\\)\">"
                               "<pre>\n<code class=\"\\1\">\n" src))))

(add-to-list 'org-export-filter-src-block-functions
             'rasmus/org-html-wrap-blocks-in-code)

;; 使用pygments高亮源码 'pelican-html backend
;; ;; Path for pygments or command name
;; (defvar pygments-path "pygmentize")

;; (defun pygments-org-html-code (code contents info)
;;   ;; Generating tmp file path.
;;   ;; Current date and time hash will ideally pass our needs.
;;   (setq temp-source-file (format "/tmp/pygmentize-%s.txt"(md5 (current-time-string))))
;;   ;; Writing block contents to the file.
;;   (with-temp-file temp-source-file (insert (org-element-property :value code)))
;;   ;; Exectuing the shell-command an reading an output
;;   (shell-command-to-string (format "%s -l \"%s\" -f html %s"
;;                    pygments-path
;;                    (or (org-element-property :language code)
;;                        "")
;;                    temp-source-file)))

;; (org-export-define-derived-backend 'pelican-html 'html
;;   :translate-alist '((src-block .  pygments-org-html-code)
;;              (example-block . pygments-org-html-code)))

