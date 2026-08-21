uv run py/magic_jinja.py \
  --debug \
  --log-level 10 \
  --toml-files data/*.toml bib/*.toml \
  --tmpl-files tex/**/*.tex \
  --out-dir . \
  --angle-delimiters
