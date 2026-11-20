#!/usr/bin/env node
// Generate the shortest path to every reachable (state, context) of a
// checkout machine, replay each path's events against the real Checkout
// class, and compare state after every step.
//
// Usage: run-paths.cjs --machine guarded|unguarded
//
// guarded   is the chosen design. Its paths are the conformance check: the
//           real Checkout class must follow every one of them exactly.
// unguarded is the rejected design: a machine whose NEXT leaves "shipping"
//           with no address set. Its paths are the witness that skipping
//           validation is a state a model can describe; the check must
//           fail here, because the real Checkout class refuses to follow
//           a path the rejected design allows.
//
// Verdict lines:
//   PASS path ConformsToMachine: <event sequence> -> <state>
//   FAIL path ConformsToMachine: expected <state>, got <state> on <event sequence>
//
// Exit codes: 0 every path conforms, 1 some path diverges, 2 usage error.
"use strict";
const { checkoutMachine, checkoutMachineUnguarded } = require("./checkout.machine.cjs");
const { Checkout } = require("./checkout.cjs");

function loadGraph() {
  const path = require("node:path");
  const os = require("node:os");
  const { createRequire } = require("node:module");
  const FV_HOME = process.env.FV_HOME || path.join(os.homedir(), ".cache", "fv");
  return createRequire(path.join(FV_HOME, "xstate", "shim.cjs"))("@xstate/graph");
}

function conforms(path) {
  const impl = new Checkout();
  for (const step of path.steps) {
    if (step.event.type !== "xstate.init") impl.send(step.event.type);
    if (impl.step !== step.state.value) {
      return { ok: false, expected: step.state.value, got: impl.step };
    }
    if (impl.hasAddress !== step.state.context.hasAddress || impl.hasPayment !== step.state.context.hasPayment) {
      return {
        ok: false,
        expected: JSON.stringify(step.state.context),
        got: JSON.stringify({ hasAddress: impl.hasAddress, hasPayment: impl.hasPayment }),
      };
    }
  }
  return { ok: true };
}

function main(argv) {
  const choice = argv[0] === "--machine" ? argv[1] : null;
  const machine = { guarded: checkoutMachine, unguarded: checkoutMachineUnguarded }[choice];
  if (!machine) {
    console.error("usage: run-paths.cjs --machine guarded|unguarded");
    return 2;
  }
  const { getShortestPaths } = loadGraph();
  const paths = getShortestPaths(machine);
  let failed = false;
  for (const path of paths) {
    const label = path.steps.map((s) => s.event.type).join(" -> ");
    const result = conforms(path);
    if (result.ok) {
      console.log(`PASS path ConformsToMachine: ${label} -> ${path.state.value}`);
    } else {
      console.log(`FAIL path ConformsToMachine: expected ${result.expected}, got ${result.got} on ${label}`);
      failed = true;
    }
  }
  return failed ? 1 : 0;
}

process.exit(main(process.argv.slice(2)));
