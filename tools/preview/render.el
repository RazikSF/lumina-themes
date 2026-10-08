;;; render.el --- dump themed buffers as HTML fragments  -*- lexical-binding: t; -*-
(require 'cl-lib)
(require 'json)
(defvar r-theme (intern (getenv "R_THEME")))
(defvar r-out (getenv "R_OUT"))
(dolist (d (split-string (or (getenv "R_PATH") "") ":" t))
  (add-to-list 'load-path d)
  (add-to-list 'custom-theme-load-path d))
(when (getenv "R_DOOM") (require 'doom-themes))
(setq custom-safe-themes t)
(advice-add 'display-color-cells :override (lambda (&rest _) 16777216))
(advice-add 'tty-display-color-cells :override (lambda (&rest _) 16777216))
(modify-frame-parameters nil '((display-type . color)))
(dolist (f '(hl-line vertico-current solaire-default-face doom-modeline-bar doom-modeline-buffer-file
             doom-modeline-buffer-modified doom-modeline-project-dir orderless-match-face-0
             completions-common-part))
  (unless (facep f) (make-empty-face f)))
(modify-frame-parameters nil (list (cons 'background-mode (if (getenv "R_LIGHT") 'light 'dark))))
(modify-frame-parameters nil '((display-type . color)))
(load-theme r-theme t)
(mapc #'custom-theme-recalc-face (face-list))
(require 'org) (require 'diff-mode) (require 'python)

(defun r-hex (c)
  (when (and (stringp c) (not (string-prefix-p "unspecified" c)))
    c))

(defvar r-bg (if (getenv "R_LIGHT") 'light 'dark))
(defun r-ok (disp)
  (or (eq disp t)
      (and (consp disp)
           (cl-every (lambda (c)
                       (pcase (car c)
                         ('class (memq 'color (cdr c)))
                         ('background (memq r-bg (cdr c)))
                         (_ t)))
                     disp))))

(defun r-choose (spec)
  (let ((hit (cl-find-if (lambda (cl) (r-ok (car cl))) spec)))
    (when hit
      (let ((pl (cdr hit))) (if (and (consp pl) (consp (car pl)) (null (cdr pl))) (car pl) pl)))))

(defun r-spec (f)
  (let ((th (cadr (assq r-theme (get f 'theme-face)))))
    (cond (th (r-choose th))
          ((get f 'face-defface-spec) (r-choose (get f 'face-defface-spec))))))

(defun r-get (f attr &optional depth)
  (when (and (symbolp f) (< (or depth 0) 8))
    (let* ((pl (r-spec f)) (v (plist-get pl attr)))
      (if (and v (not (eq v 'unspecified)))
          v
        (let ((inh (plist-get pl :inherit)))
          (cl-some (lambda (i) (r-get i attr (1+ (or depth 0)))) (if (listp inh) inh (list inh))))))))

(defun r-attr (faces attr)
  (let ((faces (if (listp faces) faces (list faces))))
    (cl-some (lambda (f) (and (symbolp f) (r-get f attr))) faces)))

(defun r-attr-old (faces attr)
  (let ((faces (if (listp faces) faces (list faces))) res)
    (cl-loop for f in faces
             when (and (symbolp f) (facep f))
             do (let ((v (face-attribute f attr nil t)))
                  (unless (or (eq v 'unspecified) (null v))
                    (setq res v) (cl-return))))
    res))

(defun r-style (faces)
  (let* ((fg (r-hex (r-attr faces :foreground)))
         (bg (r-hex (r-attr faces :background)))
         (w (r-attr faces :weight)) (sl (r-attr faces :slant))
         (h (r-attr faces :height)) (ul (r-attr faces :underline))
         (ov (r-attr faces :overline)) (inv (r-attr faces :inverse-video)))
    (when inv (cl-rotatef fg bg)
          (setq fg (or fg (r-hex (face-background 'default))) bg (or bg (r-hex (face-foreground 'default)))))
    (concat (if fg (format "color:%s;" fg) "")
            (if bg (format "background:%s;" bg) "")
            (pcase w ('bold "font-weight:700;") ('semi-bold "font-weight:600;") ('extra-bold "font-weight:800;") ('light "font-weight:300;") (_ ""))
            (if (memq sl '(italic oblique)) "font-style:italic;" "")
            (if (floatp h) (format "font-size:%.2fem;" h) "")
            (cond ((eq ul t) "text-decoration:underline;")
                  ((consp ul) (format "text-decoration:underline %s %s;"
                                      (if (eq (plist-get ul :style) 'wave) "wavy" "solid")
                                      (or (r-hex (plist-get ul :color)) "currentColor")))
                  (t ""))
            (if (stringp ov) (format "box-shadow:inset 0 2px 0 %s;" (r-hex ov)) ""))))

(defun r-esc (s) (replace-regexp-in-string "[<>&]" (lambda (m) (pcase m ("<" "&lt;") (">" "&gt;") ("&" "&amp;"))) s))

(defun r-faces-at (pos)
  (let ((f (or (get-char-property pos 'face) (get-char-property pos 'font-lock-face))))
    (if (and (consp f) (keywordp (car f))) nil f)))

(defun r-line-bg (pos)
  "Background of an :extend face at POS, to paint full line width."
  (let ((faces (r-faces-at pos)) res)
    (dolist (f (if (listp faces) faces (list faces)))
      (when (and (not res) (symbolp f) (eq (r-get f :extend) t))
        (setq res (r-hex (r-get f :background)))))
    res))

(defun r-buffer (file mode)
  (with-temp-buffer
    (insert-file-contents file)
    (funcall mode)
    (when (eq mode 'org-mode) (org-toggle-link-display) (org-toggle-link-display))
    (font-lock-ensure)
    (when (eq mode 'diff-mode) (diff-refine-hunk))
    (goto-char (point-min))
    (let (lines)
      (while (not (eobp))
        (let* ((bol (point)) (eol (line-end-position)) (pos bol) (html "")
               (lbg (and (< bol eol) (r-line-bg (max bol (1- eol))))))
          (while (< pos eol)
            (let* ((next (min eol (next-single-char-property-change pos 'face nil eol)
                              (next-single-char-property-change pos 'invisible nil eol)))
                   (inv (get-char-property pos 'invisible)))
              (unless (and inv (not (eq mode 'org-mode)))
                (unless (and inv (eq mode 'org-mode) (memq inv '(org-link)))
                  (setq html (concat html (format "<span style=\"%s\">%s</span>"
                                                  (r-style (r-faces-at pos))
                                                  (r-esc (buffer-substring-no-properties pos next)))))))
              (setq pos next)))
          (push (vector html lbg) lines))
        (forward-line 1))
      (vconcat (nreverse lines)))))

(defun r-face (f)
  (list :fg (r-hex (r-attr f :foreground)) :bg (r-hex (r-attr f :background))
        :style (r-style f)))

(let* ((dir (getenv "R_DIR"))
       (data (list :theme (symbol-name r-theme)
                   :py (r-buffer (getenv "R_PY") 'python-mode)
                   :org (r-buffer (concat dir "/sample.org") 'org-mode)
                   :diff (r-buffer (concat dir "/sample.diff") 'diff-mode)
                   :faces (cl-loop for f in '(default mode-line mode-line-inactive line-number line-number-current-line
                                              hl-line region cursor fringe vertical-border minibuffer-prompt isearch
                                              lazy-highlight show-paren-match header-line tab-bar tab-bar-tab
                                              tab-bar-tab-inactive vertico-current doom-modeline-bar
                                              doom-modeline-buffer-file doom-modeline-buffer-modified
                                              doom-modeline-project-dir completions-common-part
                                              font-lock-comment-face solaire-default-face orderless-match-face-0)
                                   append (list (intern (format ":%s" f)) (if (facep f) (r-face f) nil))))))
  (with-temp-file r-out (insert (json-encode data))))
