;;; lumina-borealis-theme.el --- Lumina Borealis -*- lexical-binding: t; -*-
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
;; Lumina Borealis: Desaturated nordic frost & aurora dark theme.
;; Muted pine greens, glacial cyans, arctic lavenders, and patinated golds over a deep misty forest canvas.
;;
;;; Code:

(deftheme lumina-borealis
  "Lumina Borealis, desaturated nordic frost dark theme.")

(let ((bg           "#101614")  ; Vert pin arctique sombre et mat
      (bg-alt       "#0B100E")  ; Noir forestier profond pour les barres
      (bg-hl        "#18221E")  ; Surlignage de ligne feutré
      (bg-block     "#151D1A")  ; Blocs de code / Org
      (bg-pop       "#1E2A26")  ; Popups & Menus
      (bg-subtle    "#273531")  ; Bordures & sélections secondaires
      (selection    "#213833")  ; Sélection menthe/pin sombre
      
      (fg           "#D0DCD9")  ; Blanc givré / Brume de givre
      (fg-dim       "#A6B5B2")  ; Gris d'eau secondaire
      (fg-subtle    "#7C8D89")  ; Neutre
      (comment      "#697B76")  ; Gris ardoise bleuté (discret et chic)
      (comment-doc  "#849691")
      
      (glacier      "#68B5A6")  ; Fonctions (Cyan glacier poudré)
      (lavender     "#9F94C2")  ; Mots-clés (Lavande arctique)
      (patina-gold  "#D4B26A")  ; Types / Classes (Or patiné)
      (mint-frost   "#88C0A8")  ; Chaînes (Menthe givrée)
      (nordic-peach "#D18A78")  ; Constantes & Nombres (Terracotta minérale)
      (soft-amber   "#E0A96D")  ; Builtins & Propriétés (Ambre nordique)
      (arctic-rose  "#C97A85")  ; Erreurs / Alertes
      
      (diff-add-bg  "#162B22")
      (diff-del-bg  "#331C1A")
      (diff-chg-bg  "#302A19")
      (border       "#273531"))

  (custom-theme-set-faces
   'lumina-borealis
   `(default ((t (:foreground ,fg :background ,bg))))
   `(fringe ((t (:foreground "#273531" :background ,bg))))
   `(mode-line ((t (:foreground ,fg-dim :background ,bg-alt :box (:line-width 6 :color ,bg-alt)))))
   `(mode-line-inactive ((t (:foreground ,comment :background ,bg :box (:line-width 6 :color ,bg)))))
   `(mode-line-buffer-id ((t (:foreground ,fg :weight semi-bold))))
   `(header-line ((t (:foreground ,fg-subtle :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-inactive ((t (:foreground ,comment :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(header-line-highlight ((t (:foreground ,glacier))))
   `(cursor ((t (:background ,glacier))))
   `(region ((t (:background ,selection :extend t))))
   `(secondary-selection ((t (:background ,bg-subtle :extend t))))
   `(hl-line ((t (:background ,bg-hl :extend t))))
   `(highlight ((t (:background ,bg-subtle))))
   `(vertical-border ((t (:foreground ,bg-subtle))))
   `(window-divider ((t (:foreground ,bg-subtle))))
   `(internal-border ((t (:background ,bg))))
   `(line-number ((t (:foreground "#24322E" :background ,bg))))
   `(line-number-current-line ((t (:foreground ,glacier :background ,bg-hl :weight semi-bold))))
   `(minibuffer-prompt ((t (:foreground ,glacier))))
   `(isearch ((t (:foreground ,bg :background ,glacier))))
   `(isearch-fail ((t (:foreground ,arctic-rose :background ,diff-del-bg))))
   `(lazy-highlight ((t (:foreground ,fg :background ,bg-subtle))))
   `(match ((t (:foreground ,glacier :background ,bg-hl))))
   `(show-paren-match ((t (:foreground ,glacier :background "#1B332E" :weight semi-bold :box (:line-width -1 :color ,glacier)))))
   `(show-paren-mismatch ((t (:foreground ,arctic-rose :background "#331C20" :weight semi-bold :box (:line-width -1 :color ,arctic-rose)))))
   `(link ((t (:foreground ,glacier :underline (:color ,glacier :style line)))))
   `(link-visited ((t (:foreground ,lavender :underline (:color ,comment :style line)))))
   `(button ((t (:inherit link))))
   `(error ((t (:foreground ,arctic-rose))))
   `(warning ((t (:foreground ,soft-amber))))
   `(success ((t (:foreground ,mint-frost))))
   `(escape-glyph ((t (:foreground ,glacier))))
   `(shadow ((t (:foreground ,comment))))
   `(trailing-whitespace ((t (:background ,diff-del-bg))))
   
   ;; Font Lock (Syntax Highlighting Désaturé / Effet Waouh Nordique)
   `(font-lock-keyword-face ((t (:foreground ,lavender :weight semi-bold))))
   `(font-lock-comment-face ((t (:foreground ,comment :slant italic))))
   `(font-lock-comment-delimiter-face ((t (:inherit font-lock-comment-face))))
   `(font-lock-doc-face ((t (:foreground ,comment-doc :slant italic))))
   `(font-lock-string-face ((t (:foreground ,mint-frost))))
   `(font-lock-function-name-face ((t (:foreground ,glacier :weight semi-bold))))
   `(font-lock-variable-name-face ((t (:foreground ,fg))))
   `(font-lock-type-face ((t (:foreground ,patina-gold :weight semi-bold))))
   `(font-lock-constant-face ((t (:foreground ,nordic-peach))))
   `(font-lock-builtin-face ((t (:foreground ,soft-amber))))
   `(font-lock-preprocessor-face ((t (:foreground ,lavender))))
   `(font-lock-negation-char-face ((t (:foreground ,arctic-rose))))
   `(font-lock-warning-face ((t (:inherit warning))))
   `(font-lock-function-call-face ((t (:foreground ,glacier))))
   `(font-lock-property-name-face ((t (:foreground ,soft-amber))))
   `(font-lock-property-use-face ((t (:foreground ,soft-amber))))
   `(font-lock-number-face ((t (:foreground ,nordic-peach))))
   `(font-lock-operator-face ((t (:foreground ,fg-subtle))))
   `(font-lock-escape-face ((t (:foreground ,soft-amber))))
   `(font-lock-bracket-face ((t (:foreground ,fg-subtle))))
   `(font-lock-delimiter-face ((t (:foreground ,fg-subtle))))
   `(font-lock-punctuation-face ((t (:foreground ,fg-subtle))))

   ;; Org Mode & Structure
   `(outline-1 ((t (:foreground ,glacier :weight semi-bold :height 1.25))))
   `(outline-2 ((t (:foreground ,lavender :weight semi-bold :height 1.12))))
   `(outline-3 ((t (:foreground ,patina-gold :weight semi-bold :height 1.05))))
   `(outline-4 ((t (:foreground ,mint-frost :weight semi-bold))))
   `(outline-5 ((t (:foreground ,soft-amber))))
   `(org-level-1 ((t (:inherit outline-1))))
   `(org-level-2 ((t (:inherit outline-2))))
   `(org-level-3 ((t (:inherit outline-3))))
   `(org-level-4 ((t (:inherit outline-4))))
   `(org-document-title ((t (:foreground ,glacier :weight semi-bold :height 1.5))))
   `(org-block ((t (:background ,bg-block :extend t))))
   `(org-block-begin-line ((t (:foreground ,comment :background ,bg-block :extend t :height 0.85))))
   `(org-block-end-line ((t (:inherit org-block-begin-line))))
   `(org-todo ((t (:foreground ,soft-amber :weight semi-bold))))
   `(org-done ((t (:foreground ,mint-frost :weight semi-bold))))
   `(org-table ((t (:foreground ,fg-dim))))

   ;; Vertico / Corfu / Autocomplétion
   `(vertico-current ((t (:foreground ,glacier :background ,bg-subtle :weight semi-bold :extend t))))
   `(corfu-current ((t (:foreground ,glacier :background ,bg-subtle :weight semi-bold))))
   `(corfu-default ((t (:foreground ,fg :background ,bg-pop))))
   `(corfu-border ((t (:background ,border))))

   ;; Magit & Git Diffs
   `(magit-diff-added ((t (:foreground ,mint-frost :background ,diff-add-bg :extend t))))
   `(magit-diff-removed ((t (:foreground ,arctic-rose :background ,diff-del-bg :extend t))))
   `(magit-diff-context-highlight ((t (:foreground ,fg-dim :background ,bg-hl :extend t))))))

(custom-theme-set-variables
 'lumina-borealis
 '(hl-todo-keyword-faces '(("TODO" . "#E0A96D") ("FIXME" . "#C97A85") ("HACK" . "#9F94C2") ("REVIEW" . "#68B5A6") ("NOTE" . "#88C0A8")))
 '(vc-annotate-background "#101614")
 '(pdf-view-midnight-colors '("#D0DCD9" . "#101614")))

;;;###autoload
(when load-file-name
  (add-to-list 'custom-theme-load-path
               (file-name-as-directory (file-name-directory load-file-name))))

(provide-theme 'lumina-borealis)

;;; lumina-borealis-theme.el ends here
