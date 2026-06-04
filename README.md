This project has three things in it:

- Some general infrastructure for running arbitrary script files before and
  after latex builds, called "hooks". Things are set up so that you can run
  builds locally with the `Makefile`, and also push them to `Overleaf` and
  things also "just work" when built there. See small caveat in discussion
  below on `py/magic_dblp.py` regarding Overleaf's sandbox and its inability to
  fetch data from the web during builds.

- `py/magic_dblp.py`: a "hook" that automagically grabs bib entries from dblp.org.

- `py/magic_sed.py`: a "hook" `*.tex` files to replace unicode characters and
  unicode markup shorthands with latex commands.

# How it Works

- The `latexmkrc` file is a copy of the one Overleaf uses, instrumented to call
  all of the python scripts in `hooks/{post_process,pre_process}` after and
  before (respectively) the main latex build.

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
  of them to all of the `*.tex` files before they are processed by latex. The
  processing is done in-place, and assumes the build is happening in a staged
  folder that has copies of all of the original files. (Which the `Makefile`
  sets up—see next bullet.)

- The `Makefile` drives `latexmk` by first copying everything into a `stage`
  directory, and then running the build locally from there. This is also what
  Overleaf does as they perform every build of the document in a local sandbox.

- The `with_python_version.sh` script is only used by the `Makefile` and
  attempts to run the build in an environment that pins the Python version. The
  version is selected to match the one used on Overleaf to maximize the
  property of "if it works locally then it will work on Overleaf".
  Note: Overleaf doesn't use this `Makefile` when it builds, it just calls
  `latexmk` which picks up the `latexmkrc` configuration file.

# How to use it

You could use this project as a starter template, or you could just move some
of the feels into your own project and it should work fine.

Files you would need to move:

- `hooks/` (just the scripts you plan to use)
- `py/` (just the scripts you plan to use)
- `sed/` (if you want to use `sed` magic)
- `latexmkrc`
- `Makefile` (if you want to build locally, or if you're using `dblp` magic,
  which requires local builds to populate the db cache)
- `with_python_version.sh` (only if you're using the Makefile)

And changes you would need to make to your project files:

- Assuming you're using `biblatex` for citations...
  - Add `\addbibresource{dblp.bib}` to your configuration (before
    `\begin{document}`).
- If you're using `natbib` or something else for citations...
  - I haven't tested these to know if they work or not. It may work out of the
    box, or it may require small tweaks to things to get it working.
