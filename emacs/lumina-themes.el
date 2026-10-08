;;; lumina-themes.el --- Lumina: a curated theme family -*- lexical-binding: t; -*-
;;
;; Author: razik <https://github.com/RazikSF>
;; Maintainer: razik <https://github.com/RazikSF>
;; URL: https://github.com/RazikSF/lumina-themes
;; Version: 1.0.0
;; Package-Requires: ((emacs "26.1"))
;; Keywords: faces, themes
;;
;;; Commentary:
;;
;; Lumina is a family of nine flavors, each in a dark, a light and
;; two high-contrast variants, plus a black-and-white Prisma light --
;; 38 themes in total.  Pure `deftheme'
;; files, no external dependency.
;;
;; M-x load-theme RET lumina-dawn-dark RET to load any of them.
;;
;; Optional customisation, set BEFORE loading a theme (or call
;; `lumina-themes-reapply' after toggling them):
;;
;;   (setq lumina-themes-brighter-comments  nil)  ; bolder comments
;;   (setq lumina-themes-comment-bg         nil)  ; tinted comment bg
;;   (setq lumina-themes-padded-modeline    nil)  ; extra modeline padding
;;   (setq lumina-themes-italic-comments    t)    ; italic on comments
;;   (setq lumina-themes-italic-types       nil)  ; italic on types
;;   (setq lumina-themes-bold-keywords      nil)  ; bold on keywords
;;
;;; Code:

(defgroup lumina-themes nil
  "Lumina: a curated theme family."
  :group 'faces)

(defcustom lumina-themes-brighter-comments nil
  "When non-nil, comments are rendered at higher contrast.
The default muted comment colour places the active code first.  Set
this to t if you read or write extensive documentation directly in
source files and want comments to stand out."
  :type 'boolean
  :group 'lumina-themes)

(defcustom lumina-themes-comment-bg nil
  "When non-nil, comments get a subtle tinted background.
Helps comment blocks form visual paragraphs in dense code."
  :type 'boolean
  :group 'lumina-themes)

(defcustom lumina-themes-padded-modeline nil
  "When non-nil (or an integer), pad the modeline with extra space.
Pass an integer to set the padding width in pixels (default 4)."
  :type '(choice (boolean :tag "Default (4px when t)")
                 (integer :tag "Custom pixel width"))
  :group 'lumina-themes)

(defcustom lumina-themes-italic-comments t
  "When non-nil, render comments in italic.
Default in the Lumina family.  Disable if your font lacks an italic
variant or you find italics distracting."
  :type 'boolean
  :group 'lumina-themes)

(defcustom lumina-themes-italic-types nil
  "When non-nil, render type names in italic.
Off by default: Lumina keeps italics for comments only."
  :type 'boolean
  :group 'lumina-themes)

(defcustom lumina-themes-bold-keywords nil
  "When non-nil, render keywords in bold.
Off by default: Lumina sets hierarchy with one lamp colour, not weight."
  :type 'boolean
  :group 'lumina-themes)

(defvar lumina-themes-dir
  (expand-file-name "themes/"
                    (file-name-directory (or load-file-name buffer-file-name)))
  "Directory holding the generated Lumina theme files.")

;;;###autoload
(when (file-directory-p lumina-themes-dir)
  (add-to-list 'custom-theme-load-path lumina-themes-dir))

(defun lumina-themes--current-lumina-theme ()
  "Return the currently enabled Lumina theme symbol, or nil."
  (cl-find-if (lambda (th) (string-prefix-p "lumina-" (symbol-name th)))
              custom-enabled-themes))

(defun lumina-themes--apply-customizations (&optional theme)
  "Apply user customisation variables to the current Lumina theme.
THEME defaults to the currently enabled Lumina theme.  Only options
that depart from the theme's own design touch a face."
  (let ((theme (or theme (lumina-themes--current-lumina-theme))))
    (when theme
      (when lumina-themes-brighter-comments
        (set-face-attribute 'font-lock-comment-face nil
                            :foreground (face-attribute 'font-lock-doc-face :foreground nil t)))
      (when lumina-themes-comment-bg
        (set-face-attribute 'font-lock-comment-face nil
                            :background (face-attribute 'highlight :background nil t)))
      (unless lumina-themes-italic-comments
        (set-face-attribute 'font-lock-comment-face nil :slant 'normal))
      (when lumina-themes-italic-types
        (set-face-attribute 'font-lock-type-face nil :slant 'italic))
      (when lumina-themes-bold-keywords
        (set-face-attribute 'font-lock-keyword-face nil :weight 'bold))
      (let ((pad lumina-themes-padded-modeline))
        (when pad
          (let ((width (if (integerp pad) pad 4)))
            (dolist (f '(mode-line mode-line-inactive))
              (set-face-attribute f nil :box `(:line-width ,width
                                               :color ,(face-attribute f :background nil t))))))))))

;;;###autoload
(defun lumina-themes-reapply ()
  "Re-apply Lumina customisation variables to the current theme.
Call this after changing any `lumina-themes-*' variable to make
the change take effect."
  (interactive)
  (lumina-themes--apply-customizations))

(defun lumina-themes--list ()
  "Return the list of installed Lumina theme symbols."
  (when (file-directory-p lumina-themes-dir)
    (mapcar (lambda (f) (intern (replace-regexp-in-string
                                 "-theme$" ""
                                 (file-name-sans-extension f))))
            (directory-files lumina-themes-dir nil "^lumina-.*-theme\\.el$"))))

;;;###autoload
(defun lumina-themes-load-random (&optional variant)
  "Load a random Lumina theme.
With no argument, picks from all variants (dark + light).
With prefix arg \\[universal-argument] (or VARIANT = \\='dark), restricts to dark.
With \\[universal-argument] \\[universal-argument] (or \\='light), restricts to light."
  (interactive
   (list (cond ((equal current-prefix-arg '(4))  'dark)
               ((equal current-prefix-arg '(16)) 'light))))
  (let* ((all (lumina-themes--list))
         (pool (pcase variant
                 ('dark  (cl-remove-if-not (lambda (s) (string-suffix-p "-dark"  (symbol-name s))) all))
                 ('light (cl-remove-if-not (lambda (s) (string-suffix-p "-light" (symbol-name s))) all))
                 (_      all))))
    (unless pool
      (user-error "No Lumina themes found in %s" lumina-themes-dir))
    (mapc #'disable-theme custom-enabled-themes)
    (let ((pick (nth (random (length pool)) pool)))
      (load-theme pick t)
      (message "Loaded %s" pick))))

(defun lumina-themes--on-enable (theme)
  "Apply Lumina customisations when a Lumina THEME is enabled."
  (when (string-prefix-p "lumina-" (symbol-name theme))
    (lumina-themes--apply-customizations theme)))

;; Apply customisations automatically when a Lumina theme is enabled.
(if (boundp 'enable-theme-functions)
    ;; Emacs 29+: official hook.
    (add-hook 'enable-theme-functions #'lumina-themes--on-enable)
  ;; Older Emacs: advise `enable-theme'.
  (advice-add 'enable-theme :after
              (lambda (theme) (lumina-themes--on-enable theme))))

(provide 'lumina-themes)
;;; lumina-themes.el ends here
