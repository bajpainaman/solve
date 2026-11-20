---
name: test-fuzz
description: "Writes fuzz harnesses for parsers, decoders, deserialisers and any code that reads untrusted bytes. One small harness per entry point, a seed corpus of real inputs, sanitizers on for native code, and every crash committed as a regression input. Use for fuzzing, a fuzz harness, Atheris, Jazzer, go test -fuzz, cargo-fuzz, libFuzzer, ClusterFuzzLite, hardening a parser after a security fix, or when the testing skill routes here. Not for rules over structured inputs (use test-property) or for fuzzing an HTTP API from its schema, which is a Schemathesis CI step."
---

# Fuzz tests

A fuzzer mutates inputs under coverage feedback to reach code that no written test reaches. The committed part is small: a harness, a seed corpus and the crash inputs. The long run happens in CI.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` where it applies. This file adds the rules that are specific to fuzzing.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| Atheris | Jazzer.js | Jazzer | native `go test -fuzz` | cargo-fuzz |

## Five rules

1. **Write one small harness per entry point.** The harness turns bytes into one call. It builds no state that outlives the call.
2. **Let unexpected errors escape.** Catch only the error type the parser documents for bad input. Every other exception, a hang or a sanitizer report is a finding. A harness that catches everything finds nothing.
3. **Assert a property where one exists.** After a successful parse, check a round trip or an invariant. A fuzzer that checks only for crashes misses wrong results.
4. **Commit a seed corpus of real inputs.** Take valid samples from fixtures, docs and production formats, one small file per shape. Without seeds the fuzzer spends its run learning the format.
5. **Turn every crash into a regression input.** Minimise the crashing input, commit it to the corpus, and add a plain test that replays it. Turn sanitizers on for native code: ASan and UBSan.

## Reject the harness if

- It catches every exception, or it catches a broad base class.
- It has no seed corpus.
- A crash was fixed and its input was not minimised and committed.

## Workflow

1. **Name the entry point and its contract.** Which function takes the untrusted bytes, and which error does it promise for bad input?
2. **Apply step 0** of assured generation. The credible bug is an input that raises an undocumented error, hangs, exhausts memory or parses to a wrong value.
3. **Write the harness and the seeds.**
4. **Run it for a short time**, such as 60 seconds, to confirm that it builds and that coverage grows. When the fuzzing tool is not installed, write the harness and list the run under "Not run".
5. **Show that the harness can fail.** Feed it a few inputs by hand that the contract rules out: truncated, empty, wrong encoding, a missing field. When one of them fails on the current code, you have found a bug, and no planted bug is needed. Otherwise plant a bug in the parser, such as a removed bounds check, confirm that a seed or the fuzzer reports it, and restore the code.
6. **Keep every failing input.** Save the smallest input that shows each failure in the corpus directory, under a name that says what it shows, such as `crash-empty-key`. Report it as a finding. Tell the user that each later crash from CI gets the same treatment: minimise it, commit it, and add a plain test that replays it.
7. **Report.** Give the harness, the corpus, the run length, what it found, and the CI commands: about 10 minutes on changed targets for a PR, and a batch run nightly that grows the corpus.

## The report

End your reply with this table, even when you wrote one check. The user reads it to decide whether each row earns its place.

| Check in the harness | Contract it protects | Bug it would report | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```python
# Bad. The harness swallows every exception, so no input can fail it, and it
# starts from an empty corpus.
def TestOneInput(data):
    try:
        parse_message(data)
    except Exception:
        pass
```

```python
# Good. Only the documented rejection is caught, a round trip checks the
# result, and the run starts from real samples in corpus/parse_message/.
import sys
import atheris

with atheris.instrument_imports():
    from wire.parser import ParseError, encode_message, parse_message


def TestOneInput(data: bytes) -> None:
    try:
        message = parse_message(data)
    except ParseError:
        return
    assert parse_message(encode_message(message)) == message


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

```bash
python fuzz/fuzz_parse_message.py fuzz/corpus/parse_message -max_total_time=600
```

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first harness |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | You add the PR and nightly fuzz jobs |
