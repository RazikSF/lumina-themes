.PHONY: build verify clean

build:
	python3 generators/lumina_gen.py all

verify: build
	@d=0; for f in emacs/themes/lumina-*-theme.el; do \
	  t=$$(basename "$$f" -theme.el); \
	  r=$$(emacs -Q --batch \
	    --eval "(setq custom-theme-load-path (list \"$(CURDIR)/emacs/themes\"))" \
	    --eval "(condition-case e (progn (load-theme (intern \"$$t\") t) (message \"OK   $$t\")) (error (message \"FAIL $$t -- %S\" e)))" \
	    2>&1 | grep -E '^(OK|FAIL)' | head -1); \
	  echo "$$r"; \
	  case "$$r" in FAIL*) d=1 ;; esac; \
	done; \
	if [ $$d -eq 0 ]; then \
	  echo "OK: all 14 themes load on pure vanilla Emacs"; \
	else echo "FAIL: see above"; exit 1; fi

clean:
	rm -rf emacs/themes/*.el wezterm/*.toml base24/*.yaml __pycache__
