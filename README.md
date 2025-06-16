# How it Works

- The `latexmkrc` file is a copy of the one Overleaf uses, instrumented to call
  all of the python scripts in `hooks/{post_process,pre_process}` after and
  before the main latex build.

- The `py/magic_dblp.py` script looks for strings of the form `DBLP:<id>`, and
  where `<id>` is of the form `*/*/*`. 
  - Bib entries for these citations are
    automatically fetched from dblp.org. To find the `<id>` for an article you
    want to cite, you can:
    - When you find the article, mouse over `view` and click `details &
      citations`. The `<id>` is everything in the URL after `dblp.org/rec/`
    - When you find the article, mouse over `export record`: the `<id>` is the
      shown under `dblp key:`.
  - Bib entries are cached when fetched and reused across builds. The cache
    file is `dblp_db`.
  - When using Overleaf, the Overleaf build sandbox won't allow fetching data
    from the internet. But you can easily just build locally, populate the
    `dblp_db` cache file, push to Overleaf, and then the magic will happen
    on the Overleaf side just fine.

- The `py/magic_sed.py` script looks for sed scripts in `sed/` and applies all
  of them to all of the `*.tex` files before they are processed by latex.
