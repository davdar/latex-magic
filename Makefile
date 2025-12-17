PRJ_NAME := document
TEX_MAIN := main

# Use the same python version as overleaf, to avoid surprises
PYENV_VERSION := 3.10.6

.PHONY: main
main:
	rsync --archive --exclude=stage . stage
	cd stage && \
		sh sh/with_python_version.sh $(PYENV_VERSION) \
		latexmk -pdflatex -halt-on-error -interaction=nonstopmode $(TEX_MAIN)
	cp stage/dblp_db ./
	cp stage/$(TEX_MAIN).pdf $(PRJ_NAME).pdf

.PHONY: lax
lax:
	rsync --archive --exclude=stage . stage
	cd stage && \
		sh sh/with_python_version.sh $(PYENV_VERSION) \
		latexmk -pdflatex -halt-on-error -interaction=nonstopmode -f $(TEX_MAIN)
	cp stage/dblp_db ./
	cp stage/$(TEX_MAIN).pdf $(PRJ_NAME).pdf

.PHONY: dev
dev:
	until (find * -name "*.tex" -maxdepth 0 && find tex -name "*.tex") | entr -d make; do true; done

.PHONY: clean
clean:
	rm -rf stage

.PHONY: deep-clean
deep-clean: clean
	rm -f dblp_db

.PHONY: sync
sync:
	(git commit -am "⇈" || true) && git pull --no-edit && git push
