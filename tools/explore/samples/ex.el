;; Bascule entre les deux variantes d'un thème Lumina
(defvar ma/lumina-saveur "sienne"
  "Saveur Lumina utilisée par défaut.")

(defun ma/basculer-theme (&optional sombre)
  "Charge la variante claire, ou sombre si SOMBRE est non nul."
  (interactive "P")
  (let ((theme (intern (format "lumina-%s-%s" ma/lumina-saveur
                               (if sombre "dark" "light")))))
    (mapc #'disable-theme custom-enabled-themes)
    (load-theme theme t)
    (message "Thème : %s" theme)))
