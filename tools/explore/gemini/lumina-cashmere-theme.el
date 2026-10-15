;;; lumina-cashmere-theme.el --- Lumina Cashmere -*- lexical-binding: t; -*-
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
;; Lumina Cashmere: Warm pastel & espresso dark theme.
;; Soft terracotta, honey, sage green, and peach pastels over an espresso velvet dark canvas.
;;
;;; Code:

(deftheme lumina-cashmere
  "Lumina Cashmere, warm pastel dark theme.")

(let ((bg           "#181416")  ; Expresso sombre et doux
      (bg-alt       "#120F11")  ; Marron très foncé pour les barres
      (bg-hl        "#231D20")  ; Surlignage chaud feutré
      (bg-block     "#201B1E")  ; Blocs de code / Org
      (bg-pop       "#282125")  ; Popups & Menus
      (bg-subtle    "#322B30")  ; Bordures & sélections secondaires
      (selection    "#3D2C34")  ; Sélection terracotta foncé
      
      (fg           "#ECE1D3")  ; Crème d'amande / Lin doux
      (fg-dim       "#C7BBAE")  ; Beige secondaire
      (fg-subtle    "#9C8F92")  ; Neutre
      (comment      "#8E8183")  ; Bois de rose poudré / Gris chaud
      (comment-doc  "#A39496")
      
      (honey        "#F0B97B")  ; Fonctions (Miel pastel)
      (terracotta   "#E5989B")  ; Mots-clés (Rose terracotta)
      (peach        "#F4A27E")  ; Types / Classes (Pêche douce)
      (sage         "#B5C99A")  ; Chaînes (Vert sauge)
      (apricot      "#F7C59F")  ; Builtins / Propriétés (Abricot pastel)
      (plum         "#D8A7CA")  ; Variables / Accent alternatif (Prune pastel)
      (melon        "#E29578")  ; Constantes (Melon doux)
      (blush        "#FFB5A7")  ; Nombres / Caractères
      (rose-red     "#E07A5F")  ; Erreurs / Alertes (Rouge brique doux)
      
      (diff-add-bg  "#222E23")
      (diff-del-bg  "#3B2023")
      (diff-chg-bg  "#382D1D")
      (border       "#322B30"))

  (custom-theme-set-faces
   'lumina-cashmere
   `(default ((t (:foreground ,fg :background ,bg))))
   `(fringe ((t (:foreground "#453B40" :background ,bg))))
   `(mode-line ((t (:foreground ,fg-dim :background ,bg-alt :box (:line-width 6 :color ,bg-alt)))))
   `(mode-line-inactive ((t (:foreground ,comment :background ,bg :box (:line-width 6 :color ,bg)))))
   `(mode-line-buffer-id ((t (:foreground ,fg :weight semi-bold))))
   `(header-line ((t (:foreground ,fg-subtle :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-highlight ((t (:foreground ,honey))))
   `(cursor ((t (:background ,honey))))
   `(region ((t (:background ,selection :extend t))))
   `(secondary-selection ((t (:background ,bg-subtle :extend t))))
   `(hl-line ((t (:background ,bg-hl :extend t))))
   `(highlight ((t (:background ,bg-subtle))))
   `(vertical-border ((t (:foreground ,bg-subtle))))
   `(window-divider ((t (:foreground ,bg-subtle))))
   `(internal-border ((t (:background ,bg))))
   `(line-number ((t (:foreground "#453B40" :background ,bg))))
   `(line-number-current-line ((t (:foreground ,honey :background ,bg-hl :weight semi-bold))))
   `(minibuffer-prompt ((t (:foreground ,honey))))
   `(isearch ((t (:foreground ,bg :background ,honey))))
   `(isearch-fail ((t (:foreground ,rose-red :background ,diff-del-bg))))
   `(lazy-highlight ((t (:foreground ,fg :background ,bg-subtle))))
   `(match ((t (:foreground ,honey :background ,bg-hl))))
   `(show-paren-match ((t (:foreground ,honey :background "#302421" :weight semi-bold :box (:line-width -1 :color ,honey)))))
   `(show-paren-mismatch ((t (:foreground ,rose-red :background "#3D2024" :weight semi-bold :box (:line-width -1 :color ,rose-red)))))
   `(link ((t (:foreground ,peach :underline (:color ,peach :style line)))))
   `(link-visited ((t (:foreground ,plum :underline (:color ,comment :style line)))))
   `(button ((t (:inherit link))))
   `(error ((t (:foreground ,rose-red))))
   `(warning ((t (:foreground ,apricot))))
   `(success ((t (:foreground ,sage))))
   `(escape-glyph ((t (:foreground ,honey))))
   `(shadow ((t (:foreground ,comment))))
   `(trailing-whitespace ((t (:background ,diff-del-bg))))
   
   ;; Font Lock (Syntax Highlighting Pastel Chaud)
   `(font-lock-keyword-face ((t (:foreground ,terracotta :weight semi-bold))))
   `(font-lock-comment-face ((t (:foreground ,comment :slant italic))))
   `(font-lock-comment-delimiter-face ((t (:inherit font-lock-comment-face))))
   `(font-lock-doc-face ((t (:foreground ,comment-doc :slant italic))))
   `(font-lock-string-face ((t (:foreground ,sage))))
   `(font-lock-function-name-face ((t (:foreground ,honey :weight semi-bold))))
   `(font-lock-variable-name-face ((t (:foreground ,fg))))
   `(font-lock-type-face ((t (:foreground ,peach :weight semi-bold))))
   `(font-lock-constant-face ((t (:foreground ,melon))))
   `(font-lock-builtin-face ((t (:foreground ,apricot))))
   `(font-lock-preprocessor-face ((t (:foreground ,terracotta))))
   `(font-lock-negation-char-face ((t (:foreground ,rose-red))))
   `(font-lock-warning-face ((t (:inherit warning))))
   `(font-lock-function-call-face ((t (:foreground ,honey))))
   `(font-lock-property-name-face ((t (:foreground ,apricot))))
   `(font-lock-property-use-face ((t (:foreground ,apricot))))
   `(font-lock-number-face ((t (:foreground ,blush))))
   `(font-lock-operator-face ((t (:foreground ,fg-subtle))))
   `(font-lock-escape-face ((t (:foreground ,apricot))))
   `(font-lock-bracket-face ((t (:foreground ,fg-subtle))))
   `(font-lock-delimiter-face ((t (:foreground ,fg-subtle))))
   `(font-lock-punctuation-face ((t (:foreground ,fg-subtle))))

   ;; Org Mode & Structure
   `(outline-1 ((t (:foreground ,honey :weight semi-bold :height 1.25))))
   `(outline-2 ((t (:foreground ,terracotta :weight semi-bold :height 1.12))))
   `(outline-3 ((t (:foreground ,peach :weight semi-bold :height 1.05))))
   `(outline-4 ((t (:foreground ,sage :weight semi-bold))))
   `(outline-5 ((t (:foreground ,plum))))
   `(org-level-1 ((t (:inherit outline-1))))
   `(org-level-2 ((t (:inherit outline-2))))
   `(org-level-3 ((t (:inherit outline-3))))
   `(org-level-4 ((t (:inherit outline-4))))
   `(org-document-title ((t (:foreground ,honey :weight semi-bold :height 1.5))))
   `(org-block ((t (:background ,bg-block :extend t))))
   `(org-block-begin-line ((t (:foreground ,comment :background ,bg-block :extend t :height 0.85))))
   `(org-block-end-line ((t (:inherit org-block-begin-line))))
   `(org-todo ((t (:foreground ,apricot :weight semi-bold))))
   `(org-done ((t (:foreground ,sage :weight semi-bold))))
   `(org-table ((t (:foreground ,fg-dim))))

   ;; Vertico / Corfu / Autocomplétion
   `(vertico-current ((t (:foreground ,honey :background ,bg-subtle :weight semi-bold :extend t))))
   `(corfu-current ((t (:foreground ,honey :background ,bg-subtle :weight semi-bold))))
   `(corfu-default ((t (:foreground ,fg :background ,bg-pop))))
   `(corfu-border ((t (:background ,border))))

   ;; Magit & Git Diffs
   `(magit-diff-added ((t (:foreground ,sage :background ,diff-add-bg :extend t))))
   `(magit-diff-removed ((t (:foreground ,rose-red :background ,diff-del-bg :extend t))))
   `(magit-diff-context-highlight ((t (:foreground ,fg-dim :background ,bg-hl :extend t))))))

(custom-theme-set-variables
 'lumina-cashmere
 '(hl-todo-keyword-faces '(("TODO" . "#F7C59F") ("FIXME" . "#E07A5F") ("HACK" . "#D8A7CA") ("REVIEW" . "#F4A27E") ("NOTE" . "#B5C99A")))
 '(vc-annotate-background "#181416")
 '(pdf-view-midnight-colors '("#ECE1D3" . "#181416")))

;;;###autoload
(when load-file-name
  (add-to-list 'custom-theme-load-path
               (file-name-as-directory (file-name-directory load-file-name))))

(provide-theme 'lumina-cashmere)

;;; lumina-cashmere-theme.el ends here
