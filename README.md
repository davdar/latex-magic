This project has a few things in it:

- `py/magic_jinja.py`: A Python script that processes a bunch of files
  as Jinja2 templates, using a bunch of TOML files as the data object.

- `py/magic_bib.py`: A Python script that automatically fetches bibtex info for
  dois and automatically grab bib entries for any DOI or MLR uri, caches them in
  a database file, and automatically builds bibtex files.

- `hooks/*`: Bash wrappers around the python scripts that specialize them
  somewhat (via command line flag options) to building latex documents. (E.g.,
  Jinja2 templates are configured to process files in place and use `<< X >>`,
  `<@ X @>` and `<# X #>` instead of `{{ X }}`, `{% X %}` and `{# X #}`.)

- `latexmkrc`: A copy of Overleaf's default `latexmkrc` that calls all scripts
  in `hooks/pre_process` before each call to `pdflatex`, likewise for
  `hooks/post_process` after each call to `pdflatex`.

- `latex/`: An example latex project directory that uses the python scripts and
  hooks (via `latexmkrc`) to do automatic bib fetching and Jinja2 templating.

- `latex/Makefile`: A generic Makefile that assumes a project structure of:
  ```
  - common/{bib,data,hooks/py,tex}
  - variants/VAR1/{bib,data,hooks/py,tex}
  - variants/VAR2/{bib,data,hooks/py,tex}
  ```
  The idea is that we are separating the build into explicit variants (e.g.,
  draft, submit, redacted). Stuff that is common to every variant goes in
  `common`, and stuff specific to variant `VAR1` goes in `variants/VAR1`. When
  building, the Makefile will union the contents of a variant's folder with
  common before building, and it will also set a flag `\isVAR1` that is
  accessible in latex, so you know what variant you are building, e.g., for
  placing logic in `common` that is still variant-specific.

