/** Exact exhaustive search over a deliberately bounded, inspectable design space. */
export const interventions = [
  {
    id: "trees",
    name: "A grove of trees",
    short: "Tree grove",
    cost: 14,
    shade: 8,
    access: 1,
    play: 1,
    water: 3,
    maintenance: 3,
    people: 28,
    space: 4,
    color: "#327568",
    cell: [2, 1],
    description:
      "Four young trees, permeable ground and establishment care. Shade grows over time.",
  },
  {
    id: "canopy",
    name: "Shade, from day one",
    short: "Shade canopy",
    cost: 18,
    shade: 9,
    access: 2,
    play: 2,
    water: 0,
    maintenance: 1,
    people: 36,
    space: 3,
    color: "#dd7557",
    cell: [4, 1],
    description:
      "A fabric canopy over a step-free gathering area. Immediate shade; structural review needed.",
  },
  {
    id: "path",
    name: "An accessible loop",
    short: "Access loop",
    cost: 12,
    shade: 0,
    access: 10,
    play: 2,
    water: 1,
    maintenance: 1,
    people: 44,
    space: 3,
    color: "#d6ad60",
    cell: [3, 3],
    description:
      "A firm, continuous route linking entrances and amenities. Detailed access design still required.",
  },
  {
    id: "benches",
    name: "Places to pause",
    short: "Resting places",
    cost: 6,
    shade: 1,
    access: 5,
    play: 0,
    water: 0,
    maintenance: 1,
    people: 20,
    space: 1,
    color: "#b38469",
    cell: [2, 3],
    description:
      "Seats with backrests and armrests, companion spaces and several resting heights.",
  },
  {
    id: "garden",
    name: "Catch the rain",
    short: "Rain garden",
    cost: 10,
    shade: 1,
    access: 0,
    play: 2,
    water: 9,
    maintenance: 3,
    people: 15,
    space: 3,
    color: "#7b9a70",
    cell: [1, 2],
    description:
      "A planted basin for runoff, designed after infiltration testing and drainage review.",
  },
  {
    id: "play",
    name: "Play without gates",
    short: "Inclusive play",
    cost: 16,
    shade: 0,
    access: 6,
    play: 10,
    water: 0,
    maintenance: 3,
    people: 35,
    space: 4,
    color: "#de795d",
    cell: [4, 3],
    description:
      "Ground-level sensory play and inclusive social play, with surfacing and inspection.",
  },
  {
    id: "meadow",
    name: "Let a corner grow",
    short: "Wildflower patch",
    cost: 4,
    shade: 0,
    access: 0,
    play: 2,
    water: 4,
    maintenance: 1,
    people: 8,
    space: 2,
    color: "#d2ab5b",
    cell: [5, 2],
    description:
      "A small seasonal meadow with clear edges and a pollinator interpretation sign.",
  },
  {
    id: "fountain",
    name: "Refill and reconnect",
    short: "Refill point",
    cost: 9,
    shade: 0,
    access: 3,
    play: 1,
    water: 2,
    maintenance: 2,
    people: 18,
    space: 1,
    color: "#5d9db1",
    cell: [5, 3],
    description:
      "An accessible drinking-water refill point. Plumbing, water quality and upkeep need an operator.",
  },
  {
    id: "table",
    name: "A table for everyone",
    short: "Community table",
    cost: 7,
    shade: 1,
    access: 4,
    play: 4,
    water: 0,
    maintenance: 1,
    people: 18,
    space: 2,
    color: "#ae896c",
    cell: [3, 1],
    description:
      "A shared picnic and games table with accessible positions and maneuvering space.",
  },
  {
    id: "lighting",
    name: "A gentler evening",
    short: "Path lighting",
    cost: 8,
    shade: 0,
    access: 3,
    play: 0,
    water: 0,
    maintenance: 2,
    people: 15,
    space: 1,
    color: "#dbbd75",
    cell: [1, 3],
    description:
      "Shielded, timed pathway lighting. Ecological effects and local lighting requirements need review.",
  },
  {
    id: "mural",
    name: "Make it ours",
    short: "Community mural",
    cost: 3,
    shade: 0,
    access: 1,
    play: 3,
    water: 0,
    maintenance: 1,
    people: 10,
    space: 1,
    color: "#bb7986",
    cell: [4, 4],
    description:
      "A paid, community-led mural workshop. Local artists and residents determine the work.",
  },
  {
    id: "paving",
    name: "Ground that breathes",
    short: "Permeable ground",
    cost: 11,
    shade: 0,
    access: 4,
    play: 1,
    water: 7,
    maintenance: 2,
    people: 16,
    space: 3,
    color: "#969e95",
    cell: [2, 4],
    description:
      "Permeable paving at an existing hard-surface area. Site testing and maintenance plan required.",
  },
];
export const rules = [
  {
    id: "shade",
    label: "Shade & shelter",
    unit: "design points",
    hint: "A place to gather out of direct sun.",
  },
  {
    id: "access",
    label: "Access & rest",
    unit: "design points",
    hint: "Continuous routes, resting places and inclusive amenities.",
  },
  {
    id: "play",
    label: "Play & belonging",
    unit: "design points",
    hint: "Things to do together, across ages and abilities.",
  },
  {
    id: "water",
    label: "Rain & biodiversity",
    unit: "design points",
    hint: "Permeable ground, planting and water stewardship.",
  },
];
export const defaults = {
  budget: 55,
  space: 16,
  maintenance: 9,
  minimums: { shade: 9, access: 12, play: 8, water: 7 },
  weights: { shade: 1, access: 1, play: 1, water: 1 },
  locked: [],
  excluded: [],
};
export function validate(c) {
  if (!c || typeof c !== "object") throw Error("A scenario is required");
  for (const k of ["budget", "space", "maintenance"])
    if (!Number.isFinite(c[k]) || c[k] < 0)
      throw Error(k + " must be a non-negative number");
  for (const group of ["minimums", "weights"])
    for (const r of rules)
      if (!Number.isFinite(c[group]?.[r.id]) || c[group][r.id] < 0)
        throw Error(group + " " + r.id + " must be non-negative");
  for (const k of ["locked", "excluded"])
    if (
      !Array.isArray(c[k]) ||
      c[k].some((id) => !interventions.some((x) => x.id === id))
    )
      throw Error("Unknown intervention");
  if (c.locked.some((id) => c.excluded.includes(id)))
    throw Error("An intervention cannot be both protected and excluded");
  return c;
}
export function measure(items, c = defaults) {
  const result = {
    cost: 0,
    space: 0,
    maintenance: 0,
    shade: 0,
    access: 0,
    play: 0,
    water: 0,
    people: 0,
  };
  for (const x of items) for (const k of Object.keys(result)) result[k] += x[k];
  result.score = rules.reduce((s, r) => s + result[r.id] * c.weights[r.id], 0);
  return result;
}
const all = Array.from({ length: 1 << interventions.length }, (_, mask) => {
  const items = interventions.filter((_, i) => mask & (1 << i));
  return { mask, ids: items.map((x) => x.id), ...measure(items) };
});
export function constraints(c) {
  return [
    {
      id: "budget",
      label: "Budget ≤ €" + c.budget + "k",
      passes: (p) => p.cost <= c.budget,
    },
    {
      id: "space",
      label: "Space ≤ " + c.space + " units",
      passes: (p) => p.space <= c.space,
    },
    {
      id: "maintenance",
      label: "Care capacity ≤ " + c.maintenance,
      passes: (p) => p.maintenance <= c.maintenance,
    },
    ...rules.map((r) => ({
      id: r.id,
      label: r.label + " ≥ " + c.minimums[r.id],
      passes: (p) => p[r.id] >= c.minimums[r.id],
    })),
    ...c.locked.map((id) => ({
      id: "lock:" + id,
      label: "Keep " + interventions.find((x) => x.id === id).short,
      passes: (p) => p.ids.includes(id),
    })),
    ...c.excluded.map((id) => ({
      id: "exclude:" + id,
      label: "Exclude " + interventions.find((x) => x.id === id).short,
      passes: (p) => !p.ids.includes(id),
    })),
  ];
}
export function solve(raw) {
  const c = validate(raw),
    cs = constraints(c);
  const feasible = all
    .filter((p) => cs.every((x) => x.passes(p)))
    .map((p) => ({
      ...p,
      score: rules.reduce((s, r) => s + p[r.id] * c.weights[r.id], 0),
    }))
    .sort(
      (a, b) =>
        b.score - a.score ||
        a.cost - b.cost ||
        a.maintenance - b.maintenance ||
        a.mask - b.mask,
    );
  if (feasible.length)
    return {
      status: "feasible",
      checked: all.length,
      count: feasible.length,
      best: feasible[0],
      alternatives: feasible.slice(1, 4),
      core: [],
      repairs: [],
      frontier: feasible
        .filter(
          (p) =>
            !feasible.some(
              (q) =>
                q.cost <= p.cost &&
                q.score >= p.score &&
                (q.cost < p.cost || q.score > p.score),
            ),
        )
        .filter(
          (p, i, a) =>
            a.findIndex((q) => q.cost === p.cost && q.score === p.score) === i,
        ),
    };
  // Deletion filtering yields an irreducible infeasible subsystem, not a minimum-cardinality core.
  let core = [...cs];
  for (const x of cs) {
    const fewer = core.filter((y) => y !== x);
    if (!all.some((p) => fewer.every((y) => y.passes(p)))) core = fewer;
  }
  const repairs = [];
  for (const x of cs.filter(
    (x) => !x.id.startsWith("lock:") && !x.id.startsWith("exclude:"),
  )) {
    const candidates = all.filter((p) =>
      cs.filter((y) => y !== x).every((y) => y.passes(p)),
    );
    if (!candidates.length) continue;
    const cap = ["budget", "space", "maintenance"].includes(x.id);
    const field = x.id === "budget" ? "cost" : x.id;
    const target = cap
      ? Math.min(...candidates.map((p) => p[field]))
      : Math.max(...candidates.map((p) => p[field]));
    const patch = cap
      ? { [x.id]: target }
      : { minimums: { ...c.minimums, [x.id]: target } };
    repairs.push({
      id: x.id,
      from: cap ? c[x.id] : c.minimums[x.id],
      to: target,
      patch,
      label:
        x.id === "budget"
          ? "Increase budget to €" + target + "k"
          : cap
            ? "Increase " + x.id + " to " + target
            : "Lower " +
              rules.find((r) => r.id === x.id).label +
              " target to " +
              target,
    });
  }
  return {
    status: "infeasible",
    checked: all.length,
    count: 0,
    best: null,
    alternatives: [],
    core: core.map(({ id, label }) => ({ id, label })),
    repairs,
    frontier: [],
  };
}
export function verifyCertificate(c, result) {
  validate(c);
  if (result.status === "feasible") {
    const selected = interventions.filter((x) =>
      result.best.ids.includes(x.id),
    );
    const actual = measure(selected, c);
    return (
      constraints(c).every((x) =>
        x.passes({ ...actual, ids: selected.map((x) => x.id) }),
      ) && Object.keys(actual).every((k) => actual[k] === result.best[k])
    );
  }
  const cs = constraints(c).filter((x) =>
    result.core.some((y) => y.id === x.id),
  );
  return (
    cs.length > 0 &&
    !all.some((p) => cs.every((x) => x.passes(p))) &&
    cs.every((x) =>
      all.some((p) => cs.filter((y) => y !== x).every((y) => y.passes(p))),
    )
  );
}
