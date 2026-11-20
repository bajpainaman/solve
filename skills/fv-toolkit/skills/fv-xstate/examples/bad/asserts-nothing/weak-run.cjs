#!/usr/bin/env node
// Broken on purpose: replays every generated path but checks only that the
// implementation's step is some string, never that it is the RIGHT string.
"use strict";
const path = require("node:path");
const os = require("node:os");
const { createRequire } = require("node:module");
const { checkoutMachine } = require("./checkout.machine.cjs");
const { Checkout } = require("./checkout.cjs");

const FV_HOME = process.env.FV_HOME || path.join(os.homedir(), ".cache", "fv");
const { getShortestPaths } = createRequire(path.join(FV_HOME, "xstate", "shim.cjs"))("@xstate/graph");

const paths = getShortestPaths(checkoutMachine);
let failed = false;
for (const p of paths) {
  const impl = new Checkout();
  for (const step of p.steps) {
    if (step.event.type !== "xstate.init") impl.send(step.event.type);
    // BUG: this checks that `impl.step` has a shape, never that it equals
    // `step.state.value`. A step that lands on the wrong state still has
    // a string for `impl.step`, so this can never fail.
    if (typeof impl.step !== "string") {
      failed = true;
    }
  }
  const label = p.steps.map((s) => s.event.type).join(" -> ");
  console.log(`PASS path ConformsToMachine: ${label} -> ${p.state.value}`);
}
process.exit(failed ? 1 : 0);
