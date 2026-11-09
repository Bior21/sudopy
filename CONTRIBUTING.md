# Working on Sudopy

## Run it

You need Python 3.10 or newer, with Tkinter.

```bash
pip install -r requirements.txt
cd app
python3 main.py
```

## Test it

From inside `app/`:

```bash
python3 -m pytest
python3 -m tools.validate_content      # checks every problem file for mistakes
python3 -m tools.verify_all_solvable   # checks every problem's solution passes its tests
```

## Add or change problems

Each topic has a script in `tools/`, such as `write_loops_content.py`, that lists
its problems: the prompt, a correct solution, and the test arguments. Running it
rewrites that topic's files in `content/`, working out every expected output by
running the solution.

```bash
python3 -m tools.write_loops_content
```

## Build the app

```bash
cd app
python3 -m tools.compress_content
pyinstaller packaging/build.spec --distpath dist --workpath build --noconfirm
```

This makes one file in `app/dist/`. Build on each system you want to support
(Windows, macOS, Linux). Then upload it as a GitHub Release and update the
download link in `website/index.html`.
