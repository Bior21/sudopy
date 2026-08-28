# Sudopy — offline Python practice, for zero-connectivity learners

A free desktop app built for [Junub Code](https://inspirejunub.org), a program where we teach programming to kids in South Sudan. Internet accesss is very unreliable or sometimes not available at all  in South Sudan. We want our students to be able to practice coding skills they learn in class with problems but lacking internet often becomes a challenge. Sudopy allows student to practice with our already preloaded problems without needing to connect to the internet.

## Why this exists

Most "learn to code" tools assume a persistent internet connection: a
browser-based IDE, a cloud grader, an account to sign in to. That assumption
doesn't hold in the places like South Sudan. Students may get online
occasionally but not reliably enough to depend on it day-to-day, and not during the class itself.

The whole app is a single downloadable executable with a real Python
interpreter, practice problems, and an auto-grader, all bundled inside. It currently contains problems for the topics we teach at Junub Code, and we hope to add more as time goes on.

## What's in the repo

```
app/
├── main.py                 # entry point (dev + packaged mode)
├── core/
│   ├── problem_loader.py   # reads/validates problem JSON, organized by topic
│   ├── runner.py           # sandboxed subprocess execution of student code
│   ├── grader.py           # compares captured output to expected output
│   ├── submission.py       # appends the function call before running student code
│   └── solutions.py        # one correct solution per problem, for verification + Show Solution
├── gui/
│   ├── main_window.py      # topic sidebar + problem list
│   ├── problem_view.py     # prompt, code editor, run/reset buttons
│   ├── code_editor.py      # the editable code text widget
│   └── results_view.py     # pass/fail + actual vs expected output
├── huffman/
│   ├── tree.py              # heap-based Huffman tree construction
│   ├── encoder.py           # text -> compressed bytes (self-contained format)
│   ├── decoder.py           # compressed bytes -> text
│   └── bitio.py              # real bit-level packing (BitWriter/BitReader)
├── content/                 # problem JSON files, one folder per topic
├── tests/                   # pytest suite (unit + integration)
├── validate_content.py       # lints content/ for schema errors, dupes, mismatches
├── verify_all_solvable.py    # confirms every problem has a working correct solution
├── compress_content.py       # packages content/ into content.huff for bundling
├── seed_content.py            # one-time authoring script that generated the baseline content
└── packaging/
    └── build.spec              # PyInstaller spec for building the standalone executable

website/
├── index.html                 # download landing page
└── style.css

.github/workflows/ci.yml       # runs tests + content validation on every push
```

## Design decisions

**Tkinter** We chose Tkinter because it ships with Python, adds no
dependency weight, and keeps the packaged executable around 12 MB which is reasonable
for most of the laptops our kids use. 



**Subprocess sandboxing.** Student code runs in an isolated
subprocess with a wall-clock timeout, not via in-process `exec()`. This
means a crash or infinite loop in submitted code can't take down the GUI,
and resource limits are enforceable at the OS level.

**Grading by stdout comparison.** `core/grader.py` compares captured output
to an expected string — simple and reliable for the problems in `content/`
today. A topic needing a different grading approach would need
`core/grader.py` extended.

**Huffman coding** `huffman/` is a from-scratch implementation (min-heap
tree construction, real bit-level packing, prefix-free code verification)
used to compress `content/` into `content.huff`, which the packaged app
decompresses at startup — genuinely load-bearing, not a demo script sitting
unused in a folder. But it's honest about its limits: on the actual JSON
problem content, it achieves roughly a 5% reduction, while `zlib`/DEFLATE
(which combines LZ77 substring matching with Huffman coding) does
significantly better on the same input, because pure Huffman can't exploit
repeated substrings the way LZ77 can. `tests/test_huffman.py` documents
this comparison directly rather than hiding it. The interpreter and GUI
framework bundled by PyInstaller are compressed separately at the OS
packaging layer — that's a different, already-solved problem, and reusing
a battle-tested compressor there was the right call.

## Running in development

Requires Python 3.10+ and Tkinter (usually included; on Debian/Ubuntu:
`sudo apt-get install python3-tk`).

```bash
pip install -r requirements.txt
cd app
python3 main.py
```

In dev mode, the app reads directly from `content/` — no compression step
needed while you're iterating on problems.

## Running the tests

```bash
cd app
python3 -m pytest -v
```

On a machine without a display, run under a virtual framebuffer:

```bash
xvfb-run -a python3 -m pytest -v
```

Also worth running before committing new content:

```bash
python3 validate_content.py      # schema checks, duplicate ids, mismatched topics
python3 verify_all_solvable.py   # confirms every problem actually has a working solution
```

## Adding a new problem

Drop a JSON file into the relevant `content/<NN>_<topic>/` folder. Most
problems take arguments and return a value, rather than reading via
`input()`:

```json
{
  "id": "loops_003",
  "topic": "loops",
  "title": "sum_of_range",
  "prompt": "Given two ints start and end, return the sum of every number from start through end, inclusive. e.g. start=3, end=6 returns 18 (3+4+5+6).",
  "starter_code": "def sum_of_range(start, end):\n    # TODO: implement this\n    pass\n",
  "function_name": "sum_of_range",
  "tests": [
    { "args": [3, 6], "expected_output": "18" },
    { "args": [1, 10], "expected_output": "55" }
  ],
  "hint": "optional nudge in the right direction"
}
```

`title` is the bare function name (matching Stanford CS106A's own
practice-problem convention), not a human-readable phrase — it's shown
as-is at the top of the problem view. `prompt` follows that same
convention: one direct paragraph — what's given, what to do, one or two
`e.g.` examples inline, and a loop/method hint only where practicing
that specific construct is the point of the problem (e.g. "Use a while
loop.") — never a separate headed sections, an explicit hook/story, or a
bulleted constraints list.

`starter_code` is a function stub — the student only edits what's inside
it. `function_name` must match the `def` name; `core/submission.py`
appends the call automatically before running the code, so the starter
code itself never includes the call. A solution can either `print()`
its answer or `return` it — the appended call prints whatever the
function returns, unless it returns `None`, so either style produces
the same stdout to grade against a test's `expected_output`.

Each test case supplies its data one of two ways: `args` (a list of
positional arguments — used by every topic except I/O) or `input`
(stdin text, for an I/O-topic problem that still reads via `input()`
because that's literally its subject). `tests` needs at least one
entry; a problem with no meaningful input variation (e.g. one that just
prints a fixed literal) can have just the one. Each test is run as a
separate execution of the submission, and all of them have to pass for
the problem to pass — this is what catches a solution that's hardcoded
to one sample input rather than actually solving the problem. Never
hand-type an `expected_output` — compute it by actually running a
correct solution (see `write_loops_content.py` for the pattern: write
the reference solution as a real Python function, then execute it
through `core.submission.run_and_grade_all` to get real output).

Then add that same hand-written correct solution to `SOLUTIONS` in
`core/solutions.py` and run `verify_all_solvable.py` — this catches the
class of bug that schema validation can't (an `expected_output` that
doesn't actually match what correct code produces). An entry is either
a real function definition matching `function_name` (everything but
I/O — verified by running it through `core.submission`, exactly like a
student submission), or a plain top-level script that reads via
`input()` (I/O topic only — verified by running it directly, since it
was never meant to be called as a function).
`verify_all_solvable.py` tells the two apart by whether the solution
text starts with `"def "`. Every problem needs a registered solution:
it's also what the GUI's Show Solution button reveals to a student,
once they've attempted the problem at least once.

A "debug it" problem uses this same schema — the only difference is
that `starter_code` is a near-complete but broken solution instead of a
`# TODO` stub, and the `prompt` says what the function is supposed to
do and that it currently doesn't. When authoring one, confirm the bug
is real by actually running the buggy `starter_code` through
`core.submission.run_and_grade_all` and checking it fails at least one
test — a "bug" that doesn't actually reproduce shouldn't ship.

## Building the standalone executable

```bash
cd app
python3 compress_content.py                 # regenerate content.huff from content/
pyinstaller packaging/build.spec --distpath dist --workpath build --noconfirm
```

Produces a single executable in `app/dist/`. PyInstaller doesn't
cross-compile — building Windows/macOS/Linux binaries requires running this
on each target OS (or via CI matrix builds).

The macOS build isn't code-signed or notarized with Apple, so first-time
openers will see a Gatekeeper warning ("Apple could not verify..."). It's
not a sign anything's wrong — it just means the app isn't registered with
Apple's developer program. The download page documents the workaround
(System Settings → Privacy & Security → Open Anyway). Apple Developer
notarization ($99/year) would remove the warning entirely if that becomes
worth the cost later.

## Deploying the download page

`website/` is a static page with no build step, deployed to GitHub Pages
via `.github/workflows/deploy-pages.yml` on every push to `website/`
(enable it once under repo Settings → Pages → Source → GitHub Actions).
After publishing a new build as a GitHub Release, update the download
link in `index.html` to point at that release's asset.

## License

MIT — see [LICENSE](LICENSE).
