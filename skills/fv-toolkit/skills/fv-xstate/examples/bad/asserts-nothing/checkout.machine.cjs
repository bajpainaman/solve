// The XState machine for the checkout wizard. It exists only to generate
// paths; nothing in the real application runs this file.
//
// Source read at: 0000000
// Covers: no real repository; this models catalog F2's multi-step wizard.
"use strict";
const path = require("node:path");
const { createRequire } = require("node:module");

const FV_HOME = process.env.FV_HOME || path.join(require("node:os").homedir(), ".cache", "fv");
const xstate = createRequire(path.join(FV_HOME, "xstate", "shim.cjs"))("xstate");
const { createMachine, assign } = xstate;

function define(shippingGuarded) {
  return createMachine({
    id: "checkout",
    initial: "cart",
    context: { hasAddress: false, hasPayment: false },
    states: {
      cart: {
        on: { NEXT: "shipping" },
      },
      shipping: {
        on: {
          SET_ADDRESS: { actions: assign({ hasAddress: true }) },
          NEXT: shippingGuarded
            ? { target: "payment", guard: ({ context }) => context.hasAddress }
            : "payment",
          BACK: "cart",
        },
      },
      payment: {
        on: {
          SET_PAYMENT: { actions: assign({ hasPayment: true }) },
          NEXT: { target: "confirmed", guard: ({ context }) => context.hasPayment },
          BACK: "shipping",
        },
      },
      confirmed: { type: "final" },
    },
  });
}

// The chosen design: NEXT only leaves "shipping" once an address is set.
const checkoutMachine = define(true);
// The rejected design: NEXT leaves "shipping" unconditionally. Its paths are
// the witness that skipping validation is a reachable state to describe;
// the real Checkout class (always guarded) must refuse to follow them.
const checkoutMachineUnguarded = define(false);

module.exports = { checkoutMachine, checkoutMachineUnguarded };
