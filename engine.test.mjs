import { test } from "node:test";
import assert from "node:assert/strict";
import {
  solve,
  defaults,
  interventions,
  measure,
  verifyCertificate,
} from "./engine.mjs";
test("default plan satisfies every constraint", () => {
  const r = solve(defaults);
  assert.equal(r.status, "feasible");
  assert.ok(verifyCertificate(defaults, r));
  assert.equal(r.checked, 4096);
});
test("budget cut returns a genuinely irreducible conflict and working repairs", () => {
  const c = { ...defaults, budget: 30 },
    r = solve(c);
  assert.equal(r.status, "infeasible");
  assert.ok(verifyCertificate(c, r));
  assert.ok(r.core.length >= 2);
  for (const repair of r.repairs) {
    const a = { ...c, ...repair.patch };
    assert.equal(solve(a).status, "feasible");
    if (repair.id === "budget")
      assert.equal(solve({ ...a, budget: repair.to - 1 }).status, "infeasible");
  }
});
test("protected choices survive optimization", () => {
  const c = {
      ...defaults,
      budget: 90,
      space: 25,
      maintenance: 20,
      locked: ["trees", "play"],
    },
    r = solve(c);
  assert.ok(r.best.ids.includes("trees"));
  assert.ok(r.best.ids.includes("play"));
  assert.ok(verifyCertificate(c, r));
});
test("excluded interventions stay excluded", () => {
  const c = { ...defaults, excluded: ["canopy"] },
    r = solve(c);
  if (r.best) assert.ok(!r.best.ids.includes("canopy"));
  assert.ok(verifyCertificate(c, r));
});
test("zero budget and targets allow empty plan", () => {
  const c = {
    ...defaults,
    budget: 0,
    minimums: { shade: 0, access: 0, play: 0, water: 0 },
    weights: { shade: 0, access: 0, play: 0, water: 0 },
  };
  assert.deepEqual(solve(c).best.ids, []);
});
test("invalid inputs rejected", () => {
  assert.throws(() => solve({ ...defaults, budget: -1 }));
  assert.throws(() => solve({ ...defaults, weights: {} }));
  assert.throws(() => solve({ ...defaults, locked: ["unknown"] }));
  assert.throws(() =>
    solve({ ...defaults, locked: ["play"], excluded: ["play"] }),
  );
});
test("tampered certificate fails", () => {
  const r = solve(defaults);
  r.best.cost = 0;
  assert.equal(verifyCertificate(defaults, r), false);
});
test("independent recursion matches exact optimum across random scenarios", () => {
  let seed = 7142;
  const rand = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 2 ** 32;
  for (let t = 0; t < 20; t++) {
    const c = {
      ...structuredClone(defaults),
      budget: 20 + Math.floor(rand() * 60),
      minimums: Object.fromEntries(
        ["shade", "access", "play", "water"].map((k) => [
          k,
          Math.floor(rand() * 15),
        ]),
      ),
    };
    let best = null,
      count = 0;
    function visit(i, items) {
      if (i === interventions.length) {
        const m = measure(items, c);
        if (
          m.cost <= c.budget &&
          m.space <= c.space &&
          m.maintenance <= c.maintenance &&
          Object.entries(c.minimums).every(([k, v]) => m[k] >= v)
        ) {
          count++;
          if (
            !best ||
            m.score > best.score ||
            (m.score === best.score && m.cost < best.cost)
          )
            best = m;
        }
        return;
      }
      visit(i + 1, items);
      visit(i + 1, [...items, interventions[i]]);
    }
    visit(0, []);
    const r = solve(c);
    assert.equal(r.count, count);
    assert.equal(r.best?.score, best?.score);
    assert.ok(verifyCertificate(c, r));
  }
});
