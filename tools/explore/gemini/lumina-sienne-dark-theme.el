;;; lumina-sienne-dark-theme.el --- Lumina Sienne Dark -*- lexical-binding: t; -*-
;;
;; Author: razik <https://github.com/RazikSF>
;; Maintainer: razik <https://github.com/RazikSF>
;; URL: https://github.com/RazikSF/lumina-themes
;; Version: 2.2.0
;; Package-Requires: ((emacs "29.1"))
;; Keywords: faces, themes
;;
;;; Commentary:
;;
;; Lumina Sienne, dark variant.
;; Slate night under warm inks: beige text at 9:1 above every accent, teal functions, mauve keywords, gold types, olive strings, coral constants, apricot builtins.
;;
;;; Code:

(deftheme lumina-sienne-dark
  "Lumina Sienne, dark variant.")

(let ((bg           "#131822")
      (bg-alt       "#0D131C")
      (bg-hl        "#161F2C")
      (bg-block     "#192230")
      (bg-pop       "#202935")
      (bg-subtle    "#29313E")
      (selection    "#243C4C")
      
      (fg           "#C9BBAD")
      (fg-dim       "#A89C90")
      (fg-subtle    "#818A9A")
      (comment      "#70798C")
      (comment-doc  "#7E889B")
      
      (teal         "#50AFB9")
      (teal-alt     "#6EAECD")
      (mauve        "#C48ECF")
      (purple       "#A28ACD")
      (blue         "#729CC8")
      (gold         "#E5C675")
      (olive        "#A8B96E")
      (coral        "#E87A6E")
      (apricot      "#F29E4C")
      (red          "#E44065")
      
      (diff-add-bg  "#1A2E1E")
      (diff-del-bg  "#3E1E1E")
      (diff-chg-bg  "#302810")
      (border       "#29313E"))

  (custom-theme-set-faces
   'lumina-sienne-dark
   `(default ((t (:foreground ,fg :background ,bg))))
   `(fringe ((t (:foreground "#404856" :background ,bg))))
   `(mode-line ((t (:foreground ,fg-dim :background ,bg-alt :box (:line-width 6 :color ,bg-alt)))))
   `(mode-line-inactive ((t (:foreground ,comment :background ,bg :box (:line-width 6 :color ,bg)))))
   `(mode-line-buffer-id ((t (:foreground ,fg :weight semi-bold))))
   `(header-line ((t (:foreground ,fg-subtle :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-highlight ((t (:foreground ,teal))))
   `(cursor ((t (:background ,teal))))
   `(region ((t (:background ,selection :extend t))))
   `(secondary-selection ((t (:background "#1F2734" :extend t))))
   `(hl-line ((t (:background ,bg-hl :extend t))))
   `(highlight ((t (:background "#1F2734"))))
   `(vertical-border ((t (:foreground "#1F2734"))))
   `(window-divider ((t (:foreground "#1F2734"))))
   `(window-divider-first-pixel ((t (:foreground "#1F2734"))))
   `(window-divider-last-pixel ((t (:foreground "#1F2734"))))
   `(internal-border ((t (:background ,bg))))
   `(line-number ((t (:foreground "#404856" :background ,bg))))
   `(line-number-current-line ((t (:foreground ,teal :background ,bg-hl :weight semi-bold))))
   `(minibuffer-prompt ((t (:foreground ,teal))))
   `(isearch ((t (:foreground ,bg :background ,teal))))
   `(isearch-fail ((t (:foreground ,red :background ,diff-del-bg))))
   `(lazy-highlight ((t (:foreground ,fg :background ,bg-subtle))))
   `(match ((t (:foreground ,teal :background "#181F2C"))))
   `(show-paren-match ((t (:foreground ,teal :background "#1C2B35" :weight semi-bold :box (:line-width -1 :color ,teal)))))
   `(show-paren-mismatch ((t (:foreground ,red :background "#32222D" :weight semi-bold :box (:line-width -1 :color ,red)))))
   `(link ((t (:foreground ,blue :underline (:color "#49729C" :style line)))))
   `(link-visited ((t (:foreground ,purple :underline (:color ,comment :style line)))))
   `(button ((t (:inherit link))))
   `(error ((t (:foreground ,red))))
   `(warning ((t (:foreground ,apricot))))
   `(success ((t (:foreground ,olive))))
   `(escape-glyph ((t (:foreground ,teal))))
   `(nobreak-space ((t (:inherit escape-glyph))))
   `(shadow ((t (:foreground ,comment))))
   `(trailing-whitespace ((t (:background ,diff-del-bg))))
   
   ;; Font Lock
   `(font-lock-keyword-face ((t (:foreground ,mauve))))
   `(font-lock-comment-face ((t (:foreground ,comment :slant italic))))
   `(font-lock-comment-delimiter-face ((t (:inherit font-lock-comment-face))))
   `(font-lock-doc-face ((t (:foreground ,comment-doc :slant italic))))
   `(font-lock-string-face ((t (:foreground ,olive))))
   `(font-lock-function-name-face ((t (:foreground ,teal :weight semi-bold))))
   `(font-lock-variable-name-face ((t (:foreground ,fg))))
   `(font-lock-type-face ((t (:foreground ,gold))))
   `(font-lock-constant-face ((t (:foreground ,coral))))
   `(font-lock-builtin-face ((t (:foreground ,apricot))))
   `(font-lock-preprocessor-face ((t (:foreground ,mauve))))
   `(font-lock-negation-char-face ((t (:foreground ,red))))
   `(font-lock-warning-face ((t (:inherit warning))))
   `(font-lock-function-call-face ((t (:foreground ,teal))))
   `(font-lock-property-name-face ((t (:foreground ,apricot))))
   `(font-lock-property-use-face ((t (:foreground ,apricot))))
   `(font-lock-number-face ((t (:foreground ,coral))))
   `(font-lock-operator-face ((t (:foreground ,fg-subtle))))
   `(font-lock-escape-face ((t (:foreground ,apricot))))
   `(font-lock-bracket-face ((t (:foreground ,fg-subtle))))
   `(font-lock-delimiter-face ((t (:foreground ,fg-subtle))))
   `(font-lock-punctuation-face ((t (:foreground ,fg-subtle))))

   ;; Tab bar & Tab line
   `(tab-bar ((t (:foreground ,fg-dim :background ,bg-alt))))
   `(tab-bar-tab ((t (:foreground ,fg :background ,bg :box (:line-width 4 :color ,bg) :overline ,teal))))
   `(tab-bar-tab-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(tab-line ((t (:foreground ,fg-dim :background ,bg-alt))))
   `(tab-line-tab ((t (:foreground ,fg :background ,bg :box (:line-width 4 :color ,bg)))))
   `(tab-line-tab-current ((t (:foreground ,fg :background ,bg :box (:line-width 4 :color ,bg) :overline ,teal))))
   `(tab-line-tab-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))

   ;; Outlines & Org Mode
   `(outline-1 ((t (:foreground ,teal :weight semi-bold :height 1.25))))
   `(outline-2 ((t (:foreground ,mauve :weight semi-bold :height 1.12))))
   `(outline-3 ((t (:foreground ,gold :weight semi-bold :height 1.05))))
   `(outline-4 ((t (:foreground ,olive :weight semi-bold))))
   `(outline-5 ((t (:foreground ,teal))))
   `(outline-6 ((t (:foreground ,mauve))))
   `(outline-7 ((t (:foreground ,gold))))
   `(outline-8 ((t (:foreground ,olive))))
   `(org-level-1 ((t (:inherit outline-1))))
   `(org-level-2 ((t (:inherit outline-2))))
   `(org-level-3 ((t (:inherit outline-3))))
   `(org-level-4 ((t (:inherit outline-4))))
   `(org-level-5 ((t (:inherit outline-5))))
   `(org-level-6 ((t (:inherit outline-6))))
   `(org-level-7 ((t (:inherit outline-7))))
   `(org-level-8 ((t (:inherit outline-8))))
   `(org-document-title ((t (:foreground ,teal :weight semi-bold :height 1.5))))
   `(org-block ((t (:background ,bg-block :extend t))))
   `(org-block-begin-line ((t (:foreground ,comment :background ,bg-block :extend t :height 0.85))))
   `(org-block-end-line ((t (:inherit org-block-begin-line))))
   `(org-todo ((t (:foreground ,apricot :weight semi-bold))))
   `(org-done ((t (:foreground ,olive :weight semi-bold))))
   `(org-table ((t (:foreground ,fg-dim))))
   `(org-link ((t (:inherit link))))
   `(org-date ((t (:foreground ,purple))))
   `(org-code ((t (:foreground ,apricot))))
   `(org-verbatim ((t (:foreground ,olive))))
   `(org-special-keyword ((t (:foreground ,comment))))
   `(org-drawer ((t (:foreground ,comment))))
   `(org-meta-line ((t (:foreground ,comment))))
   `(org-document-info ((t (:foreground ,fg-dim :height 1.05))))
   `(org-document-info-keyword ((t (:foreground ,comment))))
   `(org-property-value ((t (:foreground ,fg-dim))))
   `(org-priority ((t (:foreground ,red))))
   `(org-tag ((t (:foreground ,comment :slant italic))))
   `(org-quote ((t (:foreground ,fg-dim :background ,bg-block :slant italic :extend t))))
   `(org-verse ((t (:inherit org-quote))))

   ;; Vertico & Corfu & Completion
   `(vertico-current ((t (:foreground ,teal :background "#1C2B35" :weight semi-bold :extend t))))
   `(vertico-group-title ((t (:foreground ,fg-subtle :slant italic))))
   `(corfu-current ((t (:foreground ,teal :background "#1C2B35" :weight semi-bold))))
   `(corfu-default ((t (:foreground ,fg :background ,bg-pop))))
   `(corfu-border ((t (:background ,border))))
   `(corfu-bar ((t (:background ,comment))))
   `(corfu-popupinfo ((t (:foreground ,fg-dim :background ,bg-pop))))

   ;; Magit & Diff
   `(magit-section-heading ((t (:foreground ,teal :weight semi-bold))))
   `(magit-diff-added ((t (:foreground ,olive :background ,diff-add-bg :extend t))))
   `(magit-diff-added-highlight ((t (:foreground ,olive :background ,diff-add-bg :extend t))))
   `(magit-diff-removed ((t (:foreground ,red :background ,diff-del-bg :extend t))))
   `(magit-diff-removed-highlight ((t (:foreground ,red :background ,diff-del-bg :extend t))))
   `(magit-diff-context ((t (:foreground ,comment :extend t))))
   `(magit-diff-context-highlight ((t (:foreground ,fg-dim :background ,bg-hl :extend t))))
   `(magit-diff-hunk-heading ((t (:foreground ,fg-subtle :background "#1F2734" :extend t))))
   `(magit-diff-hunk-heading-highlight ((t (:foreground ,fg :background ,bg-subtle :extend t))))
   `(diff-added ((t (:foreground ,olive :background ,diff-add-bg :extend t))))
   `(diff-removed ((t (:foreground ,red :background ,diff-del-bg :extend t))))
   `(diff-changed ((t (:foreground ,gold :background ,diff-chg-bg :extend t))))

   ;; Tree-sitter & LSP
   `(tree-sitter-hl-face:attribute ((t (:foreground ,purple))))
   `(tree-sitter-hl-face:comment ((t (:foreground ,comment :slant italic))))
   `(tree-sitter-hl-face:constant ((t (:foreground ,coral))))
   `(tree-sitter-hl-face:constant.builtin ((t (:foreground ,apricot))))
   `(tree-sitter-hl-face:constructor ((t (:foreground ,gold))))
   `(tree-sitter-hl-face:function ((t (:foreground ,teal))))
   `(tree-sitter-hl-face:keyword ((t (:foreground ,mauve))))
   `(tree-sitter-hl-face:number ((t (:foreground ,coral))))
   `(tree-sitter-hl-face:property ((t (:foreground ,apricot))))
   `(tree-sitter-hl-face:string ((t (:foreground ,olive))))
   `(tree-sitter-hl-face:type ((t (:foreground ,gold))))

   `(lsp-face-semhl-class ((t (:foreground ,gold))))
   `(lsp-face-semhl-comment ((t (:foreground ,comment :slant italic))))
   `(lsp-face-semhl-constant ((t (:foreground ,coral))))
   `(lsp-face-semhl-function ((t (:foreground ,teal))))
   `(lsp-face-semhl-keyword ((t (:foreground ,mauve))))
   `(lsp-face-semhl-number ((t (:foreground ,coral))))
   `(lsp-face-semhl-property ((t (:foreground ,apricot))))
   `(lsp-face-semhl-string ((t (:foreground ,olive))))
   `(lsp-face-semhl-type ((t (:foreground ,gold))))))

(custom-theme-set-variables
 'lumina-sienne-dark
 '(hl-todo-keyword-faces '(("TODO" . "#F29E4C") ("FIXME" . "#E44065") ("HACK" . "#A28ACD") ("REVIEW" . "#729CC8") ("NOTE" . "#A8B96E") ("DEPRECATED" . "#70798C") ("BUG" . "#E44065") ("XXX" . "#C48ECF")))
 '(vc-annotate-color-map '((20 . "#E44065") (40 . "#F29E4C") (60 . "#E5C675") (80 . "#A8B96E") (100 . "#50AFB9") (120 . "#6EAECD") (140 . "#729CC8") (160 . "#49729C") (180 . "#A28ACD") (200 . "#C48ECF") (220 . "#818A9A") (240 . "#818A9A") (260 . "#70798C") (280 . "#70798C") (300 . "#70798C") (320 . "#70798C") (340 . "#70798C") (360 . "#70798C")))
 '(vc-annotate-very-old-color nil)
 '(vc-annotate-background "#131822")
 '(pdf-view-midnight-colors '("#C9BBAD" . "#131822"))
 '(rustic-ansi-faces ["#131822" "#E44065" "#A8B96E" "#E5C675" "#729CC8" "#C48ECF" "#6EAECD" "#C9BBAD"])
 '(fci-rule-color "#1F2734"))

;;;###autoload
(when load-file-name
  (add-to-list 'custom-theme-load-path
               (file-name-as-directory (file-name-directory load-file-name))))

(provide-theme 'lumina-sienne-dark)

;;; lumina-sienne-dark-theme.el ends here
