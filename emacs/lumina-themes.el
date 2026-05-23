;;; lumina-themes.el --- Lumina: a curated, single-light theme family -*- lexical-binding: t; -*-
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
;; Lumina is a theme family of seven flavors -- Dawn, Oxblood, Ember,
;; Tide, Indigo, Canopy, Slate -- each in dark and light, fourteen
;; themes in total.  Pure `deftheme' files, no external dependency.
;;
;; M-x load-theme RET lumina-dawn-dark RET to load any of them.
;;
;;; Code:

(defgroup lumina-themes nil
  "Lumina: a curated, single-light theme family."
  :group 'faces)

(defvar lumina-themes-dir
  (expand-file-name "themes/"
                    (file-name-directory (or load-file-name buffer-file-name)))
  "Directory holding the generated Lumina theme files.")

;;;###autoload
(when (file-directory-p lumina-themes-dir)
  (add-to-list 'custom-theme-load-path lumina-themes-dir))

(provide 'lumina-themes)
;;; lumina-themes.el ends here
