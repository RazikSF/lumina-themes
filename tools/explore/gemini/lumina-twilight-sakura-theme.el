;;; lumina-twilight-sakura-theme.el --- Lumina Twilight Sakura -*- lexical-binding: t; -*-
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
;; Lumina Twilight Sakura: Soft dusk blossom dark theme.
;; Sakura pinks, vaporous lavenders, soft peaches over a twilight plum night canvas.
;;
;;; Code:

(deftheme lumina-twilight-sakura
  "Lumina Twilight Sakura, soft dusk blossom dark theme.")

(let ((bg           "#151118")
      (bg-alt       "#0E0A11")
      (bg-hl        "#221C26")
      (bg-block     "#1C1621")
      (bg-pop       "#292230")
      (bg-subtle    "#352C3D")
      (selection    "#3B2A42")
      
      (fg           "#EAD9E8")
      (fg-dim       "#C4B3C2")
      (fg-subtle    "#9E8FA0")
      (comment      "#7D6D82")
      (comment-doc  "#94829A")
      
      (sakura-pink  "#F4A6BF")
      (lavender     "#C397D8")
      (peach        "#F9D3B4")
      (mint         "#A8E6CF")
      (sun-yellow   "#FFE79A")
      (rose-red     "#FF6B8B")
      
      (diff-add-bg  "#1A2E22")
      (diff-del-bg  "#3B1A24")
      (diff-chg-bg  "#33261C")
      (border       "#352C3D"))

  (custom-theme-set-faces
   'lumina-twilight-sakura
   `(default ((t (:foreground ,fg :background ,bg))))
   `(fringe ((t (:foreground "#352C3D" :background ,bg))))
   `(mode-line ((t (:foreground ,fg-dim :background ,bg-alt :box (:line-width 6 :color ,bg-alt)))))
   `(mode-line-inactive ((t (:foreground ,comment :background ,bg :box (:line-width 6 :color ,bg)))))
   `(header-line ((t (:foreground ,fg-subtle :background ,bg-alt :box (:line-width 4 :color ,bg-alt)))))
   `(cursor ((t (:background ,sakura-pink))))
   `(region ((t (:background ,selection :extend t))))
   `(hl-line ((t (:background ,bg-hl :extend t))))
   `(line-number ((t (:foreground "#32263A" :background ,bg))))
   `(line-number-current-line ((t (:foreground ,sakura-pink :background ,bg-hl :weight semi-bold))))
   `(minibuffer-prompt ((t (:foreground ,sakura-pink))))
   `(isearch ((t (:foreground ,bg :background ,sakura-pink))))
   
   ;; Font Lock
   `(font-lock-keyword-face ((t (:foreground ,lavender :weight semi-bold))))
   `(font-lock-comment-face ((t (:foreground ,comment :slant italic))))
   `(font-lock-string-face ((t (:foreground ,mint))))
   `(font-lock-function-name-face ((t (:foreground ,sakura-pink :weight semi-bold))))
   `(font-lock-variable-name-face ((t (:foreground ,fg))))
   `(font-lock-type-face ((t (:foreground ,peach :weight semi-bold))))
   `(font-lock-constant-face ((t (:foreground ,sun-yellow))))
   `(font-lock-builtin-face ((t (:foreground ,lavender))))

   ;; Org & Structure
   `(outline-1 ((t (:foreground ,sakura-pink :weight semi-bold :height 1.25))))
   `(outline-2 ((t (:foreground ,lavender :weight semi-bold :height 1.12))))
   `(org-block ((t (:background ,bg-block :extend t))))))

(provide-theme 'lumina-twilight-sakura)
