# Apalache

Apalache is a symbolic model checker for the same TLA+ specifications `fv-tlc` reads. It encodes a bounded number of steps as one SMT query instead of enumerating states, and it can start that query from any state that satisfies a named operator, not only from `Init`. `${CLAUDE_PLUGIN_ROOT}/scripts/fv-apalache` runs it and prints `fv-tlc`-style verdict lines, because `apalache-mc` prints only an exit code and a log.

## When to reach for Apalache over TLC

| Situation | Why |
|---|---|
| The invariant needs an inductive proof, not a bounded search | Setting `INIT` to the invariant's own name checks `Inv /\ Next => Inv'` directly, for any state that satisfies `Inv`, reachable or not. TLC only ever starts from `Init`, so it can confirm an invariant on every state it reaches without ever confirming the invariant is inductive. See `../examples/good/lease-induction/` and `../examples/bad/non-inductive-invariant/` |
| The constants are large enough that TLC's explicit search does not finish | Apalache reasons about one symbolic step at a time, so its cost depends on the formula, not on how many concrete states that formula could instantiate to |
| You need a proof that holds for an arbitrary setting of a constant, not the one value TLC was given | An inductive proof carries over to any value of a constant that does not appear in the invariant |

TLC remains the first tool to reach for. Write the model, run `fv-tlc`, and bring in Apalache specifically to turn a confirmed-but-bounded invariant into an inductive one, or when TLC cannot finish.

## Type annotations

Apalache's type checker, Snowcat, rejects a spec when it cannot infer a variable's type from how the variable is used. A `VARIABLE` whose value is a string literal needs an explicit annotation:

```tla
VARIABLES
    \* @type: Int;
    leases,
    \* @type: Str;
    phase
```

Reproduced on this plugin's `Lease.tla` with no annotations:

```text
Lease.tla:4:19-4:23: type input error: Expected a type annotation for VARIABLE phase
```

Common annotations: `Int`, `Str`, `Bool`, `Set(Int)`, `Seq(Str)`, and a record type such as `{x: Int, y: Str}`. Put the annotation on the comment line directly above the name it describes.

## Measured on Apalache 0.52.1

Each fact below was reproduced with this plugin's examples.

| Fact | Consequence |
|---|---|
| `apalache-mc` exits with `EXITCODE: OK` for no error and `EXITCODE: ERROR (12)` for a violated invariant | `fv-apalache` reads the exit code and the `invariant N violated` line, not the process's own exit status, because every outcome exits non-zero except `OK` |
| A parse, type or assignment error also exits `EXITCODE: ERROR (255)`, with no `invariant ... violated` line | `fv-apalache` reports this as `ERROR`, never as a violation. A broken spec must never count as the counterexample a check expects |
| `apalache-mc` never prints the violating trace to stdout; it writes `MCviolation1.out` under `--out-dir` and prints that path | `fv-apalache --trace` reads the file before its temporary `--out-dir` is removed |
| `--init` takes any operator name, not only `Init` | Setting `--init=Inv --inv=Inv --length=1` is the inductive step: an arbitrary `Inv`-satisfying state, one `Next` step, then `Inv` is checked again |
| An `--init` formula that constrains some variables and not others fails with `Assignment error: No assignments found for: <var>` | Every variable needs a value or a membership test in the `--init` operator, even one that is meant to leave the variable unconstrained, as in `phase \in {"idle", "held"}` |
| Apalache 0.59.0 and later are compiled for JDK 21 (`UnsupportedClassVersionError: ... class file version 65.0 ... only recognizes ... up to 64.0` under JDK 20) | The pin in `scripts/installers/apalache` stays at 0.52.1, the newest release this plugin found that runs on a JDK no newer than 20. Move the pin only after checking the new version's class file requirement |

## From the Apalache documentation, not reproduced here

- `apalache-mc check` defaults to `--length=10`. Set it explicitly; the three-step inductive pattern needs `--length=0` for the base case and the safety implication, and `--length=1` for the inductive step.
- `--tuning-options-file` and `--smt-encoding` affect solver performance on larger specs, not the verdict.
- The `rows` typing feature is the default for records since Apalache 0.29.0. A record literal written for an older tutorial may need `--features=no-rows`.

## Reading the output

`fv-apalache` reuses `fv-tlc`'s verdict lines: `PASS <check>.icfg: holds`, `PASS <check>.icfg: violated <Inv>`, `FAIL <check>.icfg: expected <X>, got <Y>`, `ERROR <check>.icfg: ...`, `UNAVAILABLE apalache: ...`. A check file is a small text file with an `\* expect:` header and four keys: `INIT`, `NEXT` (default `Next`), `INV`, and `LENGTH` (default `0`).
