"""Helpers shared by the checker wrappers: find a Java that runs, and run TLC once."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

JAVA_UNAVAILABLE = ("UNAVAILABLE java: no java binary runs; install a JDK 17 or later, "
                    "or set JAVA to its java binary")
LISTEN_FAILED = "Listen failed on port"
AGENT_JAR = "no-rmi-listen.jar"


def fv_home():
    return Path(os.environ.get("FV_HOME", Path.home() / ".cache" / "fv"))


def find_java():
    """Return the path of a java binary that runs, or None.

    JAVA wins when it is set. Otherwise the java on PATH is tried first, then
    JAVA_HOME and the Homebrew locations. The macOS java on PATH is a stub, and
    it fails in a shell that cannot see the user's installed runtimes.
    """
    explicit = os.environ.get("JAVA")
    if explicit:
        candidates = [explicit]
    else:
        candidates = ["java"]
        if os.environ.get("JAVA_HOME"):
            candidates.append(os.path.join(os.environ["JAVA_HOME"], "bin", "java"))
        candidates += ["/opt/homebrew/opt/openjdk/bin/java", "/usr/local/opt/openjdk/bin/java"]
    for candidate in candidates:
        path = shutil.which(candidate)
        if path and subprocess.run([path, "-version"], capture_output=True).returncode == 0:
            return path
    return None


def run_tlc(java, jar, arguments, cwd):
    """Run TLC once and return (exit code, output).

    Each run gets a private temp directory. TLC unpacks its standard modules
    into java.io.tmpdir, and two runs that share that directory race on the files.

    TLC exports its fingerprint set over RMI, which opens a listening socket even
    for a check on one machine. A sandboxed shell forbids that socket. When TLC
    fails for that reason, the run is repeated with a Java agent that hands RMI a
    socket that never listens. fv-install tla builds the agent beside the TLC jar.
    """
    def once(extra):
        with tempfile.TemporaryDirectory(prefix="fv-tlc-") as scratch:
            run = subprocess.run(
                [java, "-XX:+UseParallelGC", f"-Djava.io.tmpdir={scratch}", *extra,
                 "-cp", str(jar), "tlc2.TLC",
                 "-workers", os.environ.get("FV_TLC_WORKERS", "1"),
                 "-metadir", scratch, *arguments],
                cwd=cwd, capture_output=True, text=True,
            )
        return run.returncode, run.stdout + run.stderr

    code, output = once([])
    if LISTEN_FAILED in output:
        agent = Path(jar).parent / AGENT_JAR
        if agent.is_file():
            code, output = once([f"-javaagent:{agent}"])
        else:
            output += ("\nTLC could not open a local socket, which a sandboxed shell forbids. "
                       "Run fv-install tla with a JDK to build the socket agent, "
                       "or run this command outside the sandbox.")
    return code, output
