# Sudopy

A desktop app for practicing Python without an internet connection. Built for [Junub Code](https://inspirejunub.org), a program that teaches programming to kids in South Sudan.

## Why it exists

Most "learn to code" tools assume a reliable connection: a browser-based IDE, a cloud grader, an account to sign into. That doesn't hold in South Sudan, where students may get online sometimes but not reliably enough to depend on during class.

Sudopy is a single downloadable executable with a real Python interpreter, a set of practice problems, and an auto-grader, all bundled inside. It currently contains problems for the topics we teach at Junub Code, and we hope to add more as time goes on.

## How it works

A student picks a problem from the sidebar, writes Python in the editor, and clicks Run. Their code runs in a separate process against that problem's test cases, and its output is compared against what a correct solution produces. Nothing leaves the machine: there's no server, no account, no network call anywhere in the grading path.

If a problem stumps them, Show Solution reveals a working answer, but only after they've run their own code at least once.

## Repository structure

```
app/
├── main.py                 entry point; also re-invoked as a subprocess to run student code
├── core/
│   ├── problem_loader.py   reads and validates problem JSON
│   ├── runner.py           runs student code in a sandboxed subprocess
│   ├── grader.py           compares captured output to expected output
│   ├── submission.py       appends the function call before running student code
│   └── solutions.py        one correct solution per problem
├── gui/                    the Tkinter interface — sidebar, editor, results
├── huffman/                a from-scratch Huffman compressor for the bundled content
├── content/                problem JSON, one folder per topic
├── content_authoring.py    shared logic behind every write_<topic>_content.py script
├── validate_content.py     checks content/ for schema errors and mismatches
├── verify_all_solvable.py  confirms every problem's solution actually solves it
├── compress_content.py     packs content/ into content.huff for the packaged build
├── tests/                  pytest suite
└── packaging/build.spec    PyInstaller spec for the standalone executable

website/                    the download page, deployed to GitHub Pages
```

## Design decisions

**Tkinter.** It ships with Python, so it adds no dependency weight, and it keeps the packaged executable around 10 MB — small enough for the laptops most students actually have.

**Student code runs in a subprocess, not `exec()`.** A crash or infinite loop in submitted code can't take down the GUI, and a wall-clock timeout kills anything that hangs.

**Grading compares stdout.** A student's function is called with a test's arguments, and whatever it prints gets checked against an expected string. A returned value is printed automatically too, so either style works.

**Huffman compression for the bundled content.** `huffman/` builds its own tree, encoder, and bit-level packer rather than reaching for `zlib`. On the actual problem content it gets about a 29% reduction; `zlib` gets closer to 59% on the same files, since it can also exploit repeated substrings, which plain Huffman coding can't. `tests/test_huffman.py` records that comparison directly. The interpreter and GUI framework that PyInstaller bundles get compressed separately, at the OS packaging layer, with `zlib` doing that job.

## Running locally

Requires Python 3.10+ and Tkinter (usually included; on Debian/Ubuntu: `sudo apt-get install python3-tk`).

```bash
pip install -r requirements.txt
cd app
python3 main.py
```

In this mode the app reads directly from `content/` — no compression step needed while editing problems.

## Tests

```bash
cd app
python3 -m pytest -v
```

On a machine without a display:

```bash
xvfb-run -a python3 -m pytest -v
```

Worth running too before committing new content:

```bash
python3 validate_content.py      # schema errors, duplicate ids, mismatched topics
python3 verify_all_solvable.py   # confirms every problem has a working solution
```

## Adding content

Each topic has its own `write_<topic>_content.py` script that defines its problems: prompt, correct solution, and test arguments. It hands them to `content_authoring.py`, which runs the real solution to compute every `expected_output`, confirms any "debug it" problem's broken starter code actually fails a test, and writes the JSON files. `write_loops_content.py` is a good one to read first. A new topic's folder just needs a name that sorts into the right place, e.g. `06_functions` sorting between `05_loops` and `06_strings`.

Every problem also needs a matching entry in `core/solutions.py`, checked by `verify_all_solvable.py`. That's what catches an `expected_output` that doesn't actually match what correct code produces, and it's also what Show Solution reveals to students.

## Building the standalone executable

```bash
cd app
python3 compress_content.py
pyinstaller packaging/build.spec --distpath dist --workpath build --noconfirm
```

Produces a single executable in `app/dist/`. PyInstaller doesn't cross-compile, so building for Windows, macOS, and Linux means running this on each target OS.

The macOS build isn't code-signed or notarized, so first-time openers see a Gatekeeper warning. The download page documents the workaround (System Settings → Privacy & Security → Open Anyway).

## Deploying the download page

`website/` is a static page with no build step, deployed to GitHub Pages via `.github/workflows/deploy-pages.yml` on every push to `website/`. After publishing a new build as a GitHub Release, update the download link in `index.html`.

## License

MIT — see [LICENSE](LICENSE).
