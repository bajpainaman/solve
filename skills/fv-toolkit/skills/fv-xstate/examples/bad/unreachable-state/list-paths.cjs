#!/usr/bin/env node
// Prints the shortest path to every state the generator actually reaches.
// Run it and look at what it does NOT print.
"use strict";
const path = require("node:path");
const os = require("node:os");
const { createRequire } = require("node:module");
const { checkoutMachine } = require("./broken.machine.cjs");

const FV_HOME = process.env.FV_HOME || path.join(os.homedir(), ".cache", "fv");
const { getShortestPaths } = createRequire(path.join(FV_HOME, "xstate", "shim.cjs"))("@xstate/graph");

const paths = getShortestPaths(checkoutMachine);
for (const p of paths) {
  const label = p.steps.map((s) => s.event.type).join(" -> ");
  console.log(`PASS path reachable: ${label} -> ${p.state.value}`);
}
console.log(`${paths.length} states reached; the machine declares cart, shipping, payment, cancelled`);
process.exit(0);
