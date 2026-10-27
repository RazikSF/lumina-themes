;;; lumina-themes.el --- Lumina: a curated theme family -*- lexical-binding: t; -*-
;;
;; Author: Razik Ikhlef <https://github.com/RazikSF>
;; Maintainer: Razik Ikhlef <https://github.com/RazikSF>
;; URL: https://github.com/RazikSF/lumina-themes
;; Version: 1.0.0
;; Package-Requires: ((emacs "27.1"))
;; Keywords: faces, themes
;;
;; Copyright (C) 2026 Razik Ikhlef
;; SPDX-License-Identifier: MIT
;;
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;;
;; The above copyright notice and this permission notice shall be included in all
;; copies or substantial portions of the Software.
;;
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
;; SOFTWARE.
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;; Lumina is a family of fifteen flavors, each in a dark and a light
;; variant, plus Vitrail, a high-contrast pair: 32 themes.  Rayleigh is
;; the default flavor, by night and by day.  The themes are plain
;; `deftheme' files with no dependency, close to 3 000 faces each:
;; core UI, built-in modes and over 150 packages (org, magit, vertico,
;; corfu, lsp, treemacs, mu4e, ...).
;;
;;   (load-theme 'lumina-rayleigh-dark t)
;;
;; M-x lumina-themes-select to pick a theme with completion,
;; M-x lumina-themes-toggle to switch between the dark and light twin.
;;
;; Optional customisation, set BEFORE loading a theme (or call
;; `lumina-themes-reapply' after toggling them):
;;
;;   (setq lumina-themes-brighter-comments  nil)  ; bolder comments
;;   (setq lumina-themes-comment-bg         nil)  ; tinted comment bg
;;   (setq lumina-themes-padded-modeline    nil)  ; extra modeline padding
;;   (setq lumina-themes-italic-comments    t)    ; italic on comments (default)
;;   (setq lumina-themes-italic-types       nil)  ; italic on types
;;   (setq lumina-themes-bold-keywords      nil)  ; bold on keywords
;;
;;; Code:

(require 'cl-lib)

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
Keywords are already semi-bold; this makes them bold."
  :type 'boolean
  :group 'lumina-themes)

(defvar lumina-themes-dir
  (let* ((here (file-name-directory (or load-file-name buffer-file-name)))
         (sub (expand-file-name "themes/" here)))
    (if (file-directory-p sub) sub here))
  "Directory holding the Lumina theme files.
The themes/ subdirectory of a source checkout, or the package
directory itself when the files are installed flat (MELPA).")

;;;###autoload
(when load-file-name
  (let* ((here (file-name-directory load-file-name))
         (sub (expand-file-name "themes/" here)))
    (add-to-list 'custom-theme-load-path (if (file-directory-p sub) sub here))))

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

(defun lumina-themes--flavors ()
  "Return the names of the installed Lumina flavors."
  (delete-dups
   (delq nil (mapcar (lambda (s)
                       (when (string-match "\\`lumina-\\(.+?\\)-\\(dark\\|light\\)" (symbol-name s))
                         (match-string 1 (symbol-name s))))
                     (lumina-themes--list)))))

(defun lumina-themes-name (flavor mode)
  "Return the Lumina theme for FLAVOR and MODE (`dark' or `light')."
  (intern (format "lumina-%s-%s" flavor mode)))

;;;###autoload
(defun lumina-themes-load (flavor &optional mode)
  "Load the Lumina FLAVOR in MODE, `dark' or `light'.
Interactively, dark, or light with a prefix."
  (interactive (list (completing-read "Lumina flavor: " (lumina-themes--flavors) nil t)
                     (if current-prefix-arg 'light 'dark)))
  (let ((theme (lumina-themes-name flavor (or mode 'dark))))
    (mapc #'disable-theme custom-enabled-themes)
    (load-theme theme t)
    (message "Loaded %s" theme)))

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
                 ('dark  (cl-remove-if-not (lambda (s) (string-match-p "-dark" (symbol-name s))) all))
                 ('light (cl-remove-if-not (lambda (s) (string-match-p "-light" (symbol-name s))) all))
                 (_      all))))
    (unless pool
      (user-error "No Lumina themes found in %s" lumina-themes-dir))
    (mapc #'disable-theme custom-enabled-themes)
    (let ((pick (nth (random (length pool)) pool)))
      (load-theme pick t)
      (message "Loaded %s" pick))))

;;;###autoload
(defun lumina-themes-select (theme)
  "Load the Lumina THEME chosen with completion, disabling every other theme."
  (interactive
   (list (intern (completing-read "Lumina theme: "
                                  (mapcar #'symbol-name (lumina-themes--list))
                                  nil t))))
  (mapc #'disable-theme custom-enabled-themes)
  (load-theme theme t)
  (message "Loaded %s" theme))

;;;###autoload
(defun lumina-themes-toggle ()
  "Switch between the dark and the light twin of the current Lumina theme.
Contrast variants keep their suffix."
  (interactive)
  (let* ((cur (lumina-themes--current-lumina-theme))
         (name (if cur (symbol-name cur) (user-error "No Lumina theme is enabled")))
         (next (cond ((string-match-p "-dark" name) (replace-regexp-in-string "-dark" "-light" name t t))
                     ((string-match-p "-light" name) (replace-regexp-in-string "-light" "-dark" name t t))
                     (t (user-error "No twin for %s" name)))))
    (mapc #'disable-theme custom-enabled-themes)
    (load-theme (intern next) t)
    (message "Loaded %s" next)))

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
