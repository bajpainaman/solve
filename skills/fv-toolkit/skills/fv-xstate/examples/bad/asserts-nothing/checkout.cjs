// The real checkout flow. No XState at runtime; a plain class the browser
// would ship, driven by the same four event types as checkout.machine.cjs.
"use strict";

class Checkout {
  constructor() {
    this.step = "cart";
    this.hasAddress = false;
    this.hasPayment = false;
  }

  send(eventType) {
    if (this.step === "cart" && eventType === "NEXT") {
      this.step = "shipping";
    } else if (this.step === "shipping" && eventType === "SET_ADDRESS") {
      this.hasAddress = true;
    } else if (this.step === "shipping" && eventType === "NEXT" && this.hasAddress) {
      this.step = "payment";
    } else if (this.step === "shipping" && eventType === "BACK") {
      this.step = "cart";
    } else if (this.step === "payment" && eventType === "SET_PAYMENT") {
      this.hasPayment = true;
    } else if (this.step === "payment" && eventType === "NEXT" && this.hasPayment) {
      this.step = "confirmed";
    } else if (this.step === "payment" && eventType === "BACK") {
      this.step = "shipping";
    }
    // Any other event has no transition, same as the machine.
  }
}

module.exports = { Checkout };
