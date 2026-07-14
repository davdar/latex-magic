This project has three things in it:

- Some general infrastructure for running arbitrary script files before and
  after latex builds, called "hooks". Things are set up so that you can run
  builds locally with the `Makefile`, and also push them to `Overleaf` and
  things also "just work" when built there. See small caveat in discussion below
  on `py/magic_bib.py` regarding Overleaf's sandbox and its inability to fetch
  data from the web during builds.

- `py/magic_bib.py`: automatically grab bib entries for any DOI.

- `py/magic_jinja.py`: automatically apply jinja templates.

# How it Works

- The `latexmkrc` file is a copy of the one Overleaf uses, instrumented to call
  all of the python scripts in `hooks/{post_process,pre_process}` after and
  before (respectively) the main latex build, in lexicographic order of the
  script filenames.

- The `py/bib.py` script looks for strings of the form `DOI:<doi>`, and
  where `<doi>` is a valid DOI identifier.
  - Bib entries for these citations are automatically fetched from doi.org.
  - Bib entries are cached when fetched and reused across builds. The default
    cache file is `bib/bib_db`.
  - When using Overleaf, the Overleaf build sandbox won't allow fetching data
    from the internet. But you can easily just build locally, populate the
    `bib_db` cache file, push to Overleaf, and then the magic will happen
    on the Overleaf side just fine.

- The `py/magic_jinja.py` is configurable to concatenate a bunch of toml files
  and use those as the data object to instantiate a bunch of jinja template
  files.

- The `Makefile` drives `latexmk` by first copying everything into a `stage`
  directory, and then running the build locally from there. This is also what
  Overleaf does as they perform every build of the document in a local sandbox.

- The scripts use `uv` to run Python scripts with dependencies declared in
  comments at the top of the file.

# How to use it

You could use this project as a starter template, or you could just move some
of the feels into your own project and it should work fine.

Files you would need to move:

- `hooks/` (just the scripts you plan to use)
- `py/` (just the scripts you plan to use)
- `latexmkrc`
- `Makefile` (if you want to build locally, or if you're using `dblp` magic,
  which requires local builds to populate the db cache)

And changes you would need to make to your project files:

- Assuming you're using `biblatex` for citations...
  - Add `\addbibresource{bib/magic.bib}` to your configuration (before
    `\begin{document}`).
- If you're using `natbib` or something else for citations...
  - I haven't tested these to know if they work or not. It may work out of the
    box, or it may require small tweaks to things to get it working.
