# Sudopy

A desktop app for practicing Python without an internet connection. Built for [Junub Code](https://inspirejunub.org/), a program that teaches programming to kids in South Sudan.

## Why it exists

Most "learn to code" tools assume a reliable internet connection: a browser-based IDE, a cloud grader, or an account to sign into. That doesn't work well in South Sudan, where students may have internet access sometimes but can't reliably depend on it during class.

Sudopy is a single downloadable application with a Python interpreter, practice problems, and an auto-grader built in. The problems currently cover the topics we teach at Junub Code, with more to be added as the curriculum grows.

## How it works

A student picks a problem from the sidebar, writes Python in the editor, and clicks Run. Sudopy runs their code against the problem's test cases and checks the result.

Everything happens on the student's computer. There is no account, server, or internet connection needed to solve and grade a problem.

If a student gets stuck, Show Solution reveals a working solution after they have attempted the problem.

## Repository structure

```text
app/
├── main.py                 entry point
├── core/                   running submissions, loading problems, and grading
├── gui/                    the Tkinter interface
├── huffman/                Huffman compression for bundled content
├── content/                Python practice problems
├── content_authoring.py    tools for creating problem content
├── validate_content.py     checks problem content
├── verify_all_solvable.py  checks that problems have working solutions
├── compress_content.py     compresses content for the packaged build
├── tests/                  pytest suite
└── packaging/build.spec    PyInstaller configuration

website/                    download page

.github/workflows/          automated tests and deployment
```

## Design decisions

### Tkinter

Sudopy uses Tkinter for the desktop interface because it comes with Python and keeps the application small.

### Student code runs separately

Student programs run in a separate process with a time limit. This prevents a crashing program or an infinite loop from taking down the rest of the application.

### Simple grading

Most problems ask students to write a function. Sudopy runs the function with several test cases and checks the output against the expected result.

### Huffman compression

The `huffman/` directory contains a from-scratch Huffman encoder and decoder used to compress the problem content before it is bundled with the application.

## Running locally

Requires Python 3.10+ and Tkinter. On Debian/Ubuntu, Tkinter may need to be installed separately:

```bash
sudo apt-get install python3-tk
```

Install the dependencies:

```bash
pip install -r requirements.txt
cd app
python3 main.py
```

During development, the app reads directly from `content/`, so problems can be edited without rebuilding the application.

## Tests

```bash
cd app
python3 -m pytest -v
```

On a machine without a display:

```bash
xvfb-run -a python3 -m pytest -v
```

For new or changed problems, also run:

```bash
python3 validate_content.py
python3 verify_all_solvable.py
```

## Adding content

Each topic has a `write_<topic>_content.py` script that defines its problems, solutions, and tests. `content_authoring.py` turns these definitions into the JSON files used by the app.

After adding new problems, run the content validation and solvability checks above.

## Building the standalone executable

```bash
cd app
python3 compress_content.py
pyinstaller packaging/build.spec --distpath dist --workpath build --noconfirm
```

The executable is placed in `app/dist/`.

PyInstaller builds for the operating system it is running on, so separate builds are needed for Windows, macOS, and Linux.

The current macOS build is not signed or notarized, so macOS may show a Gatekeeper warning when opening it for the first time.

## Deploying the download page

`website/` is a static page deployed to GitHub Pages through GitHub Actions.

After publishing a new build as a GitHub Release, update the download link in `website/index.html`.
