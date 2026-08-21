# MAGIC VARIABLE REFERENCE:
# $@ = file name of target rule
# $(@D) = directory part of $@
# $(@F) = the file within directory part of $@
# $< = name of first prerequisite
# $^ = names of all prerequisites

include Makefile_Options
include Makefile_Options_Local

OUTPUT_PREFIX ?= main
RUN_LATEX ?= latexmk -pdflatex -shell-escape -halt-on-error -interaction=nonstopmode
VARIANTS ?= $(patsubst variants/%,%,$(wildcard variants/*))
ALL_TARGETS ?= $(VARIANTS)
MAIN_TARGETS ?= $(ALL_TARGETS)

.PHONY: main
main: $(MAIN_TARGETS)

.PHONY: again
again:
	touch common/main.tex
	$(MAKE)

.PHONY: all
all: $(ALL_TARGETS)

define EACH_VARIANT

SRC_FILES_$1 ?= \
	common/latexmkrc \
	common/main.tex \
	common/bib/bib_db \
	$(wildcard common/bib/*) \
	$(wildcard common/data/*) \
	$(wildcard common/fonts/*) \
	$(wildcard common/hooks/*) \
	$(wildcard common/images/*) \
	$(wildcard common/py/*) \
	$(wildcard common/tex/*) \
	$(wildcard variants/$1/bib/*) \
	$(wildcard variants/$1/data/*) \
	$(wildcard variants/$1/fonts/*) \
	$(wildcard variants/$1/hooks/*) \
	$(wildcard variants/$1/images/*) \
	$(wildcard variants/$1/py/*) \
	$(wildcard variants/$1/tex/*)

OUT_FILES_$1 ?= \
	$$(patsubst common/%,out/$1/%, \
	$$(patsubst variants/$1/%,out/$1/%, \
	$$(SRC_FILES_$1)))

PRETEX_$1 ?= "\\def\\isVariant$1{}"

OUTPUT_PREFIX_$1 ?= $$(OUTPUT_PREFIX)
OUTPUT_SUFFIX_$1 ?= _$1
OUTPUT_$1 ?= $$(OUTPUT_PREFIX_$1)$$(OUTPUT_SUFFIX_$1).pdf

DATA_FILES_$1 = \
	$(wildcard common/data/*.toml) \
	$(wildcard common/bib/*.toml) \
	$(wildcard variants/$1/data/*.toml) \
	$(wildcard variants/$1/bib/*.toml) \

out/$1/%: common/% $$(DATA_FILES_$1)
	mkdir -p $$(@D)
	cp -r $$< $$@

out/$1/%: variants/$1/% $$(DATA_FILES_$1)
	mkdir -p $$(@D)
	cp -r $$< $$@

out/$1/bib/bib_db: common/bib/bib_db
	mkdir -p $$(@D)
	cd out/$1/bib && ln -s ../../../common/bib/bib_db

out/$1/main.pdf: $$(OUT_FILES_$1)
	cd $$(@D) && $$(RUN_LATEX) -usepretex="$$(PRETEX_$1)" main.tex

$$(OUTPUT_$1): out/$1/main.pdf
	cp $$< $$@

.PHONY: $1
$1: $$(OUTPUT_$1)

endef

$(foreach v,$(VARIANTS),$(eval $(call EACH_VARIANT,$v)))

common/bib/bib_db:
	touch $@

.PHONY: debug
debug:
	@echo "MAIN_TARGETS="
	@echo "$(MAIN_TARGETS)"
	@echo "VARIANTS="
	@echo "$(VARIANTS)"
	@echo "--final--"
	@echo "SRC_FILES_final="
	@echo "$(SRC_FILES_final)"
	@echo "OUT_FILES_final="
	@echo "$(OUT_FILES_final)"
	@echo "OUTPUT_final="
	@echo "$(OUTPUT_final)"

.PHONY: clean
clean:
	rm -rf out
	rm -f $(foreach v,$(VARIANTS),$(OUTPUT_$v))

.PHONY: version
versions:
	pdflatex --version
	latexmk --version
	uv --version
