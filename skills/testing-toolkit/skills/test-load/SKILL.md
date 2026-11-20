---
name: test-load
description: "Writes load tests and benchmarks as code for hot paths, capacity planning and performance-sensitive changes. Every script carries thresholds on p95 or p99 latency and on error rate, so that a failed threshold fails the run. A smoke-size run goes on the PR, and load, stress, spike and soak runs go on a schedule. Use for load tests, k6, Locust, Gatling, performance tests, stress or soak tests, benchmarks with a regression comparison, \"will this handle the traffic\", or when the testing skill routes here. Not for correctness of the response (use test-integration)."
---

# Load tests

A load test is a script plus a run. The script is committed and reviewed like code. The run produces a pass or a fail from thresholds that the script states, so that nobody has to read a graph to learn whether performance regressed.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` where it applies. This file adds the rules that are specific to load tests.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| Locust | k6 | Gatling | k6 | k6, Goose |

## Five rules

1. **State thresholds in the script.** Put a threshold on p95 or p99 latency and one on the error rate. A failed threshold makes the tool exit with a non-zero code, which fails the CI job.
2. **Use percentiles.** An average hides the slow tail, and the tail is what users notice.
3. **Size the run for its stage.** A smoke run of a few users for under a minute goes on the PR. Average-load, stress, spike and soak profiles run nightly or before a release.
4. **Vary the data.** Draw IDs, search terms and payloads from a data file. A script that requests one key measures the cache.
5. **Take every target from the environment.** The base URL and credentials come from variables. Never point a stress, spike or soak profile at production without the user's explicit agreement.

## Reject the script if

- It has no threshold, or its only threshold is on an average.
- A soak or stress profile runs in PR CI.
- Every iteration requests the same key.

## Profiles

| Profile | Shape | Answers | Runs |
|---|---|---|---|
| Smoke | 1 to 5 users, under 1 minute | Does the script work, and is the path healthy? | PR |
| Average load | Normal traffic for 10 to 30 minutes | Does it meet its targets on a normal day? | Nightly |
| Stress | A ramp beyond normal traffic | Where does it degrade, and how? | Nightly or before a release |
| Spike | A sudden jump and drop | Does it survive and recover? | Before a release |
| Soak | Normal traffic for hours | Does it leak memory or connections? | Weekly |

## Workflow

1. **Get the targets.** Ask for the latency and error-rate targets, or take them from the SLO. When none exists, measure a baseline, propose a threshold from it, and say that the user must confirm the number.
2. **Apply step 0** of assured generation. The credible bug is a regression: a query without an index, a lost cache, a pool that is too small.
3. **Write the script** with thresholds, checks on the response, and varied data. Keep one script and select the profile with a variable.
4. **Run the smoke profile** against a local or staging target. When the tool or a target is not available, write the script and list the run under "Not run".
5. **Report** the thresholds and where each number came from, the profiles, the schedule for each, and the command for CI.

For a micro-benchmark, commit the benchmark and a stored baseline, and fail only on a slowdown that is larger than the run-to-run noise.

## The report

End your reply with this table, even when you wrote one threshold. The user reads it to decide whether each row earns its place.

| Threshold or check | Where the number comes from | Regression that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```js
// Bad. The run never fails, the only number is an average, and every
// request reads the same product.
export default function () {
  const res = http.get('https://shop.example.com/products/1');
  console.log(res.timings.duration);
}
```

```js
// Good. Thresholds fail the run, the data varies, and the profile comes
// from the environment with smoke as the default.
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const products = new SharedArray('products', () => JSON.parse(open('./data/products.json')));

const profiles = {
  smoke: { vus: 2, duration: '30s' },
  average: { stages: [{ duration: '5m', target: 50 }, { duration: '20m', target: 50 }, { duration: '2m', target: 0 }] },
};

export const options = {
  ...profiles[__ENV.PROFILE || 'smoke'],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300', 'p(99)<800'],
  },
};

export default function () {
  const product = products[Math.floor(Math.random() * products.length)];
  const res = http.get(`${__ENV.BASE_URL}/products/${product.id}`);
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Before the first script |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | You place each profile in a CI stage |
