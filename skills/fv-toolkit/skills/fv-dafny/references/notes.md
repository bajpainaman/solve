# Installing and invoking Dafny

## Measured on Dafny 4.11.0 and Z3 5.4.1

Each fact below was reproduced with this plugin's examples.

| Fact | Consequence |
|---|---|
| The `dafny` dotnet-tool package ships no SMT solver; `dafny verify` alone fails with `Error: Z3 is not found` | `scripts/installers/dafny` downloads a pinned Z3 build separately, and `fv-dafny` always passes `--solver-path` |
| `dafny verify`'s apphost (`$FV_HOME/dafny/dafny`) needs `DOTNET_ROOT` set to find the .NET runtime; `dotnet <path-to-Dafny.dll> verify ...` needs no such variable | `fv-dafny` invokes `dotnet` on the `Dafny.dll` path directly, which is also simpler to locate than guessing where a given machine's `dotnet` SDK keeps its runtimes |
| `dafny verify` also runs a compile step by default, which exits 2 on any warning even when verification itself succeeded (`Compilation failed because warnings were found and --allow-warnings is false`) | `fv-dafny` always passes `--allow-warnings`, so its exit code reflects only the verifier |
| A loop invariant about a sequence after `parts[i := v]` is not available to Z3 on its own; it needs an explicit lemma relating `Sum` before and after the update | `examples/good/allocation/Allocate.dfy`'s `SumUpdate` lemma, proved by induction on the index |
| `{:fuel F, low, high}` requires `high == low + 1` | Reproduced as `Error: fuel setting for function Fib must have high value == 1 + low value` while writing `examples/bad/masked-timeout/Slow.dfy` |
| Dafny's own timeout message suggests the fix that masks a slow proof instead of fixing it: `the limit can be increased using --verification-time-limit` | `examples/bad/masked-timeout/` |
| `dafny build --target:py` produces a package (`<module>-py/`) importable from a sibling script via `sys.path.insert`; a compiled method lives on a `default__` class | `examples/good/allocation/test_differential.py` |

## From the Dafny documentation, not reproduced here

- `--cores` controls how many assertion batches `dafny verify` checks in parallel; it does not change what gets proved.
- `{:isolate_assertions}` on a method checks each assertion as its own query, which can turn one timeout into several smaller, faster ones, or show which assertion is the slow one.
- `dafny build` also targets C#, Java, Go and JavaScript; the differential link works the same way in any of them, with the target language's own equivalent of `sys.path`.
