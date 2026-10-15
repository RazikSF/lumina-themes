;;; lumina-neon-cyber-theme.el --- Lumina Neon Cyber -*- lexical-binding: t; -*-
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
;; Lumina Neon Cyber: High-saturation vibrant dark theme.
;; Electric cyan, hot magenta, cyber yellow, and laser green over a deep urban night canvas.
;;
;;; Code:

(deftheme lumina-neon-cyber
  "Lumina Neon Cyber, high-saturation vibrant dark theme.")

(let ((bg           "#0C0D19")  ; Nuit urbaine profonde (indigo sombre)
      (bg-alt       "#070810")  ; Noir absolu pour les barres
      (bg-hl        "#14162B")  ; Surlignage de ligne électrique
      (bg-block     "#111324")  ; Blocs de code / Org
      (bg-pop       "#1B1E38")  ; Popups & Menus
      (bg-subtle    "#25294D")  ; Bordures & sélections secondaires
      (selection    "#2E234B")  ; Sélection violette profonde
      
      (fg           "#E8EEF2")  ; Blanc néon clair
      (fg-dim       "#B8C2CC")  ; Gris argenté secondaire
      (fg-subtle    "#8B98A9")  ; Neutre
      (comment      "#6A6B9E")  ; Indigo orbitale (discret mais lisible)
      (comment-doc  "#8587B8")
      
      (cyan         "#00F0FF")  ; Fonctions (Cyan électrique)
      (magenta      "#FF007F")  ; Mots-clés (Magenta fluo)
      (yellow       "#FFE600")  ; Types / Classes (Jaune cyber)
      (green        "#39FF14")  ; Chaînes (Vert laser)
      (orange       "#FF5F1F")  ; Constantes & Nombres (Orange corail)
      (purple       "#BD00FF")  ; Prétraitement / Vraie variable
      (pink         "#FF66B2")  ; Builtins / Propriétés
      (red          "#FF2A6D")  ; Erreurs / Alertes
      
      (diff-add-bg  "#0E2E1B")
      (diff-del-bg  "#3A1122")
      (diff-chg-bg  "#322811")
      (border       "#25294D"))

  (custom-theme-set-faces
   'lumina-neon-cyber
   `(default ((t (:foreground ,fg :background ,bg))))
   `(fringe ((t (:foreground "#25294D" :background ,bg))))
   `(mode-line ((t (:foreground ,fg-dim :background ,bg-alt :box (:line-width 6 :color ,bg-alt)))))
   `(mode-line-inactive ((t (:foreground ,comment :background ,bg :box (:line-width 6 :color ,bg)))))
   `(mode-line-buffer-id ((t (:foreground ,fg :weight semi-bold))))
   `(header-line ((t (:foreground ,fg-subtle :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-highlight ((t (:foreground ,cyan))))
   `(cursor ((t (:background ,cyan))))
   `(region ((t (:background ,selection :extend t))))
   `(secondary-selection ((t (:background ,bg-subtle :extend t))))
   `(hl-line ((t (:background ,bg-hl :extend t))))
   `(highlight ((t (:background ,bg-subtle))))
   `(vertical-border ((t (:foreground ,bg-subtle))))
   `(window-divider ((t (:foreground ,bg-subtle))))
   `(internal-border ((t (:background ,bg))))
   `(line-number ((t (:foreground "#2B3054" :background ,bg))))
   `(line-number-current-line ((t (:foreground ,cyan :background ,bg-hl :weight semi-bold))))
   `(minibuffer-prompt ((t (:foreground ,cyan))))
   `(isearch ((t (:foreground ,bg :background ,cyan))))
   `(isearch-fail ((t (:foreground ,red :background ,diff-del-bg))))
   `(lazy-highlight ((t (:foreground ,fg :background ,bg-subtle))))
   `(match ((t (:foreground ,cyan :background ,bg-hl))))
   `(show-paren-match ((t (:foreground ,cyan :background "#102F40" :weight semi-bold :box (:line-width -1 :color ,cyan)))))
   `(show-paren-mismatch ((t (:foreground ,red :background "#3A1020" :weight semi-bold :box (:line-width -1 :color ,red)))))
   `(link ((t (:foreground ,cyan :underline (:color ,cyan :style line)))))
   `(link-visited ((t (:foreground ,magenta :underline (:color ,comment :style line)))))
   `(button ((t (:inherit link))))
   `(error ((t (:foreground ,red))))
   `(warning ((t (:foreground ,yellow))))
   `(success ((t (:foreground ,green))))
   `(escape-glyph ((t (:foreground ,cyan))))
   `(shadow ((t (:foreground ,comment))))
   `(trailing-whitespace ((t (:background ,diff-del-bg))))
   
   ;; Font Lock (Syntax Highlighting Saturé / Cyberpunk)
   `(font-lock-keyword-face ((t (:foreground ,magenta :weight semi-bold))))
   `(font-lock-comment-face ((t (:foreground ,comment :slant italic))))
   `(font-lock-comment-delimiter-face ((t (:inherit font-lock-comment-face))))
   `(font-lock-doc-face ((t (:foreground ,comment-doc :slant italic))))
   `(font-lock-string-face ((t (:foreground ,green))))
   `(font-lock-function-name-face ((t (:foreground ,cyan :weight semi-bold))))
   `(font-lock-variable-name-face ((t (:foreground ,fg))))
   `(font-lock-type-face ((t (:foreground ,yellow :weight semi-bold))))
   `(font-lock-constant-face ((t (:foreground ,orange))))
   `(font-lock-builtin-face ((t (:foreground ,pink))))
   `(font-lock-preprocessor-face ((t (:foreground ,purple))))
   `(font-lock-negation-char-face ((t (:foreground ,red))))
   `(font-lock-warning-face ((t (:inherit warning))))
   `(font-lock-function-call-face ((t (:foreground ,cyan))))
   `(font-lock-property-name-face ((t (:foreground ,pink))))
   `(font-lock-property-use-face ((t (:foreground ,pink))))
   `(font-lock-number-face ((t (:foreground ,orange))))
   `(font-lock-operator-face ((t (:foreground ,fg-subtle))))
   `(font-lock-escape-face ((t (:foreground ,pink))))
   `(font-lock-bracket-face ((t (:foreground ,fg-subtle))))
   `(font-lock-delimiter-face ((t (:foreground ,fg-subtle))))
   `(font-lock-punctuation-face ((t (:foreground ,fg-subtle))))

   ;; Org Mode & Structure
   `(outline-1 ((t (:foreground ,cyan :weight semi-bold :height 1.25))))
   `(outline-2 ((t (:foreground ,magenta :weight semi-bold :height 1.12))))
   `(outline-3 ((t (:foreground ,yellow :weight semi-bold :height 1.05))))
   `(outline-4 ((t (:foreground ,green :weight semi-bold))))
   `(outline-5 ((t (:foreground ,purple))))
   `(org-level-1 ((t (:inherit outline-1))))
   `(org-level-2 ((t (:inherit outline-2))))
   `(org-level-3 ((t (:inherit outline-3))))
   `(org-level-4 ((t (:inherit outline-4))))
   `(org-document-title ((t (:foreground ,cyan :weight semi-bold :height 1.5))))
   `(org-block ((t (:background ,bg-block :extend t))))
   `(org-block-begin-line ((t (:foreground ,comment :background ,bg-block :extend t :height 0.85))))
   `(org-block-end-line ((t (:inherit org-block-begin-line))))
   `(org-todo ((t (:foreground ,yellow :weight semi-bold))))
   `(org-done ((t (:foreground ,green :weight semi-bold))))
   `(org-table ((t (:foreground ,fg-dim))))

   ;; Vertico / Corfu / Autocomplétion
   `(vertico-current ((t (:foreground ,cyan :background ,bg-subtle :weight semi-bold :extend t))))
   `(corfu-current ((t (:foreground ,cyan :background ,bg-subtle :weight semi-bold))))
   `(corfu-default ((t (:foreground ,fg :background ,bg-pop))))
   `(corfu-border ((t (:background ,border))))

   ;; Magit & Git Diffs
   `(magit-diff-added ((t (:foreground ,green :background ,diff-add-bg :extend t))))
   `(magit-diff-removed ((t (:foreground ,red :background ,diff-del-bg :extend t))))
   `(magit-diff-context-highlight ((t (:foreground ,fg-dim :background ,bg-hl :extend t))))))

(custom-theme-set-variables
 'lumina-neon-cyber
 '(hl-todo-keyword-faces '(("TODO" . "#FFE600") ("FIXME" . "#FF2A6D") ("HACK" . "#BD00FF") ("REVIEW" . "#00F0FF") ("NOTE" . "#39FF14")))
 '(vc-annotate-background "#0C0D19")
 '(pdf-view-midnight-colors '("#E8EEF2" . "#0C0D19")))

;;;###autoload
(when load-file-name
  (add-to-list 'custom-theme-load-path
               (file-name-as-directory (file-name-directory load-file-name))))

(provide-theme 'lumina-neon-cyber)

;;; lumina-neon-cyber-theme.el ends here
