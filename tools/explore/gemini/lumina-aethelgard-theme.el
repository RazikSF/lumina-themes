;;; lumina-aethelgard-theme.el --- Lumina Aethelgard -*- lexical-binding: t; -*-
;;
;; Author: razik <https://github.com/RazikSF>
;; Maintainer: razik <https://github.com/RazikSF>
;; URL: https://github.com/RazikSF/lumina-themes
;; Version: 1.0.0
;; Package-Requires: ((emacs "29.1"))
;; Keywords: faces, themes
;;
;;; Commentary:
;;
;; Lumina Aethelgard: Midnight Velvet & Astral Gold.
;; An exquisite cosmic dark theme with deep stellar blacks, ivory text, 
;; emerald functions, amethyst keywords, and solar gold types.
;;
;;; Code:

(deftheme lumina-aethelgard
  "Lumina Aethelgard, cosmic dark variant.")

(let ((bg           "#0B0F19")
      (bg-alt       "#060911")
      (bg-hl        "#121929")
      (bg-block     "#0F1422")
      (bg-pop       "#161F33")
      (bg-subtle    "#1E2A42")
      (selection    "#1E2D4A")
      
      (fg           "#E2D9CE")
      (fg-dim       "#B5A89B")
      (fg-subtle    "#8A96B0")
      (comment      "#7A859E")
      (comment-doc  "#929EB8")
      
      (emerald      "#4FD6BE")
      (emerald-alt  "#70E2CD")
      (amethyst     "#CF8EF0")
      (purple       "#B084CC")
      (blue         "#73B9FF")
      (gold         "#FFD166")
      (mint         "#99E1D9")
      (coral        "#FF9F80")
      (amber        "#F4A261")
      (ruby         "#FF5C8A")
      
      (diff-add-bg  "#132B22")
      (diff-del-bg  "#331A26")
      (diff-chg-bg  "#2B2613")
      (border       "#1E2A42"))

  (custom-theme-set-faces
   'lumina-aethelgard
   `(default ((t (:foreground ,fg :background ,bg))))
   `(fringe ((t (:foreground "#2A3854" :background ,bg))))
   `(mode-line ((t (:foreground ,fg-dim :background ,bg-alt :box (:line-width 6 :color ,bg-alt)))))
   `(mode-line-inactive ((t (:foreground ,comment :background ,bg :box (:line-width 6 :color ,bg)))))
   `(mode-line-buffer-id ((t (:foreground ,fg :weight semi-bold))))
   `(header-line ((t (:foreground ,fg-subtle :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-highlight ((t (:foreground ,emerald))))
   `(cursor ((t (:background ,emerald))))
   `(region ((t (:background ,selection :extend t))))
   `(secondary-selection ((t (:background ,bg-subtle :extend t))))
   `(hl-line ((t (:background ,bg-hl :extend t))))
   `(highlight ((t (:background ,bg-subtle))))
   `(vertical-border ((t (:foreground ,bg-subtle))))
   `(window-divider ((t (:foreground ,bg-subtle))))
   `(internal-border ((t (:background ,bg))))
   `(line-number ((t (:foreground "#2A3854" :background ,bg))))
   `(line-number-current-line ((t (:foreground ,emerald :background ,bg-hl :weight semi-bold))))
   `(minibuffer-prompt ((t (:foreground ,emerald))))
   `(isearch ((t (:foreground ,bg :background ,emerald))))
   `(isearch-fail ((t (:foreground ,ruby :background ,diff-del-bg))))
   `(lazy-highlight ((t (:foreground ,fg :background ,bg-subtle))))
   `(match ((t (:foreground ,emerald :background ,bg-hl))))
   `(show-paren-match ((t (:foreground ,emerald :background "#162B36" :weight semi-bold :box (:line-width -1 :color ,emerald)))))
   `(show-paren-mismatch ((t (:foreground ,ruby :background "#361622" :weight semi-bold :box (:line-width -1 :color ,ruby)))))
   `(link ((t (:foreground ,blue :underline (:color ,blue :style line)))))
   `(link-visited ((t (:foreground ,amethyst :underline (:color ,comment :style line)))))
   `(button ((t (:inherit link))))
   `(error ((t (:foreground ,ruby))))
   `(warning ((t (:foreground ,amber))))
   `(success ((t (:foreground ,mint))))
   `(escape-glyph ((t (:foreground ,emerald))))
   `(shadow ((t (:foreground ,comment))))
   `(trailing-whitespace ((t (:background ,diff-del-bg))))
   
   ;; Font Lock (Syntax Highlighting)
   `(font-lock-keyword-face ((t (:foreground ,amethyst :weight semi-bold))))
   `(font-lock-comment-face ((t (:foreground ,comment :slant italic))))
   `(font-lock-comment-delimiter-face ((t (:inherit font-lock-comment-face))))
   `(font-lock-doc-face ((t (:foreground ,comment-doc :slant italic))))
   `(font-lock-string-face ((t (:foreground ,mint))))
   `(font-lock-function-name-face ((t (:foreground ,emerald :weight semi-bold))))
   `(font-lock-variable-name-face ((t (:foreground ,fg))))
   `(font-lock-type-face ((t (:foreground ,gold :weight semi-bold))))
   `(font-lock-constant-face ((t (:foreground ,coral))))
   `(font-lock-builtin-face ((t (:foreground ,amber))))
   `(font-lock-preprocessor-face ((t (:foreground ,amethyst))))
   `(font-lock-negation-char-face ((t (:foreground ,ruby))))
   `(font-lock-warning-face ((t (:inherit warning))))
   `(font-lock-function-call-face ((t (:foreground ,emerald))))
   `(font-lock-property-name-face ((t (:foreground ,amber))))
   `(font-lock-property-use-face ((t (:foreground ,amber))))
   `(font-lock-number-face ((t (:foreground ,coral))))
   `(font-lock-operator-face ((t (:foreground ,fg-subtle))))
   `(font-lock-escape-face ((t (:foreground ,amber))))
   `(font-lock-bracket-face ((t (:foreground ,fg-subtle))))
   `(font-lock-delimiter-face ((t (:foreground ,fg-subtle))))
   `(font-lock-punctuation-face ((t (:foreground ,fg-subtle))))

   ;; Org Mode & Outlines
   `(outline-1 ((t (:foreground ,emerald :weight semi-bold :height 1.25))))
   `(outline-2 ((t (:foreground ,amethyst :weight semi-bold :height 1.12))))
   `(outline-3 ((t (:foreground ,gold :weight semi-bold :height 1.05))))
   `(outline-4 ((t (:foreground ,mint :weight semi-bold))))
   `(org-level-1 ((t (:inherit outline-1))))
   `(org-level-2 ((t (:inherit outline-2))))
   `(org-level-3 ((t (:inherit outline-3))))
   `(org-level-4 ((t (:inherit outline-4))))
   `(org-document-title ((t (:foreground ,emerald :weight semi-bold :height 1.5))))
   `(org-block ((t (:background ,bg-block :extend t))))
   `(org-block-begin-line ((t (:foreground ,comment :background ,bg-block :extend t :height 0.85))))
   `(org-block-end-line ((t (:inherit org-block-begin-line))))
   `(org-todo ((t (:foreground ,amber :weight semi-bold))))
   `(org-done ((t (:foreground ,mint :weight semi-bold))))

   ;; Vertico / Corfu / Completion
   `(vertico-current ((t (:foreground ,emerald :background ,bg-subtle :weight semi-bold :extend t))))
   `(corfu-current ((t (:foreground ,emerald :background ,bg-subtle :weight semi-bold))))
   `(corfu-default ((t (:foreground ,fg :background ,bg-pop))))
   `(corfu-border ((t (:background ,border))))

   ;; Magit & Diffs
   `(magit-diff-added ((t (:foreground ,mint :background ,diff-add-bg :extend t))))
   `(magit-diff-removed ((t (:foreground ,ruby :background ,diff-del-bg :extend t))))
   `(magit-diff-context-highlight ((t (:foreground ,fg-dim :background ,bg-hl :extend t))))))

(custom-theme-set-variables
 'lumina-aethelgard
 '(hl-todo-keyword-faces '(("TODO" . "#F4A261") ("FIXME" . "#FF5C8A") ("HACK" . "#B084CC") ("REVIEW" . "#73B9FF") ("NOTE" . "#99E1D9")))
 '(vc-annotate-background "#0B0F19")
 '(pdf-view-midnight-colors '("#E2D9CE" . "#0B0F19")))

;;;###autoload
(when load-file-name
  (add-to-list 'custom-theme-load-path
               (file-name-as-directory (file-name-directory load-file-name))))

(provide-theme 'lumina-aethelgard)

;;; lumina-aethelgard-theme.el ends here
