// Broken on purpose: "cancelled" has no incoming transition from any state,
// so no generated path ever reaches it.
//
// Source read at: 0000000
// Covers: no real repository.
"use strict";
const path = require("node:path");
const { createRequire } = require("node:module");

const FV_HOME = process.env.FV_HOME || path.join(require("node:os").homedir(), ".cache", "fv");
const { createMachine, assign } = createRequire(path.join(FV_HOME, "xstate", "shim.cjs"))("xstate");

// The intent was CANCEL from "shipping" to "cancelled", the same as the real
// app's cancel button. The event was never added to "shipping"'s `on` map,
// so this is the same mistake as a `cancel()` method nothing calls.
const checkoutMachine = createMachine({
  id: "checkout",
  initial: "cart",
  context: { hasAddress: false },
  states: {
    cart: { on: { NEXT: "shipping" } },
    shipping: {
      on: {
        SET_ADDRESS: { actions: assign({ hasAddress: true }) },
        NEXT: { target: "payment", guard: ({ context }) => context.hasAddress },
      },
    },
    payment: { type: "final" },
    cancelled: { type: "final" }, // BUG: nothing transitions here
  },
});

module.exports = { checkoutMachine };
