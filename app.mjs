import {
  interventions,
  rules,
  defaults,
  solve,
  verifyCertificate,
} from "./engine.mjs";
const $ = (s) => document.querySelector(s),
  copy = (x) => structuredClone(x);
let c = copy(defaults),
  result;
try {
  const s = JSON.parse(localStorage.getItem("common-ground-v1"));
  if (s) {
    solve(s);
    c = s;
  }
} catch {}
const icons = ["♧", "⌂", "⌁", "▱", "❧", "◈", "✿", "♒", "⊞", "☼", "◒", "▦"],
  esc = (s) =>
    String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
function svg() {
  let s = `<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="#bfccb8"/></pattern><filter id="shadow"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#50624c" flood-opacity=".15"/></filter></defs><rect width="760" height="490" fill="url(#grid)"/><g transform="translate(80 25)"><path d="M80 320L380 395 598 220 304 143Z" fill="#ced8c1"/><path d="M80 309L380 383 598 208 304 130Z" fill="#e0e6d5" stroke="#bfcbb2" stroke-width="2"/><path d="M101 307L378 372 575 213 305 144Z" fill="#eaf0dc"/><path d="M69 338L381 417 620 224" fill="none" stroke="#d6d6c9" stroke-width="16"/><path d="M61 349L382 430 633 231" fill="none" stroke="#fefcf6" stroke-width="3" stroke-dasharray="7 8"/><path d="M95 104L295 151 300 117 101 70Z" fill="#dedfd3"/><path d="M95 104L101 70 101 18 95 53Z" fill="#bfc5b5"/><path d="M101 70L300 117 300 65 101 18Z" fill="#e6e5d9"/><path d="M101 18L300 65 339 35 141-12Z" fill="#f7f5ed"/><g fill="#acb9ab">${[0, 1, 2, 3, 4, 5].map((i) => `<path d="M${114 + i * 31} ${33 + i * 7.2}l17 4v24l-17-4Z"/>`).join("")}</g>`;
  const xy = {
    trees: [240, 193],
    canopy: [435, 211],
    path: [300, 272],
    benches: [207, 281],
    garden: [173, 237],
    play: [391, 310],
    meadow: [501, 259],
    fountain: [471, 297],
    table: [337, 183],
    lighting: [134, 297],
    mural: [341, 346],
    paving: [263, 330],
  };
  for (const x of interventions) {
    let [px, py] = xy[x.id],
      active = result.best?.ids.includes(x.id);
    s += `<g class="ground-object ${active ? "present" : "absent"}" transform="translate(${px} ${py})"><title>${esc(x.name)}${active ? " — selected" : " — not selected"}</title>`;
    if (x.id === "trees")
      s += `<g filter="url(#shadow)">${[
        [-22, 0],
        [16, -20],
        [34, 17],
        [-11, 34],
      ]
        .map(
          ([a, b]) =>
            `<g transform="translate(${a} ${b})"><ellipse cy="8" rx="22" ry="10" fill="#99b488" opacity=".45"/><path d="M0 5V-29" stroke="#99775a" stroke-width="5"/><ellipse cy="-34" rx="23" ry="24" fill="#67916b"/><ellipse cx="-5" cy="-41" rx="15" ry="16" fill="#8ba777"/></g>`,
        )
        .join("")}</g>`;
    else if (x.id === "canopy")
      s += `<path d="M-35 0v-41M35 17v-41M68-11v-41M0-28v-41" stroke="#a69b7e" stroke-width="3"/><path d="M-38-42L34-25 71-53 0-71Z" fill="#dda66a"/><path d="M-38-42L0-71 12-43 34-25Z" fill="#e9c58e"/>`;
    else if (x.id === "path")
      s += `<path d="M-80 9Q-46-55 25-36T102 2" fill="none" stroke="#e2c793" stroke-width="17"/><path d="M-80 9Q-46-55 25-36T102 2" fill="none" stroke="#f0dfb9" stroke-width="11"/>`;
    else if (x.id === "garden")
      s += `<ellipse rx="40" ry="20" fill="#94b19a"/><ellipse cy="-3" rx="31" ry="12" fill="#76a49a"/>${[-24, -9, 8, 23].map((a) => `<path d="M${a} 0q-10-26-3-35M${a} 0q8-22 13-18" stroke="#587d5b" fill="none" stroke-width="3"/>`).join("")}`;
    else if (x.id === "play")
      s += `<ellipse rx="43" ry="23" fill="#dbc397"/><path d="M-22 0v-39l30 8v38" stroke="#d78061" stroke-width="6" fill="none"/><path d="M9-29Q42-21 32 10" stroke="#daa464" stroke-width="9" fill="none"/><circle cx="-19" cy="-4" r="8" fill="#66988f"/><path d="M-19-23V-8" stroke="#405f58"/><circle cx="21" cy="9" r="7" fill="#b17b73"/>`;
    else if (x.id === "meadow")
      s += `<ellipse rx="32" ry="16" fill="#a9bd8b"/>${Array.from({ length: 12 }, (_, i) => `<circle cx="${Math.sin(i * 5) * 24}" cy="${Math.cos(i * 5) * 10 - 5}" r="3" fill="${i % 2 ? "#f0cf7b" : "#e8bda3"}"/>`).join("")}`;
    else if (x.id === "table")
      s += `<path d="M-20 5v-15M24 16v-15" stroke="#92734f" stroke-width="4"/><path d="M-30-16l48 12 20-14-48-12Z" fill="#d6ad76"/><path d="M-32-3l49 12M-14-29l47 12" stroke="#b88d5e" stroke-width="5"/>`;
    else if (x.id === "benches")
      s += `<path d="M-25 3v-13M23 14v-13" stroke="#7e8068" stroke-width="3"/><path d="M-28-13l49 12 10-7-49-12Z" fill="#bf9462"/><path d="M-19-29l50 13v10l-50-13Z" fill="#d4b07e"/>`;
    else if (x.id === "fountain")
      s += `<ellipse cy="7" rx="15" ry="7" fill="#bbcbb6"/><path d="M-5 4v-29h12v29" fill="#87a9a8"/><ellipse cy="-26" cx="1" rx="11" ry="5" fill="#b9d3ce"/><path d="M3-25q5-13 9-7" stroke="#78b7c9" fill="none" stroke-width="2"/>`;
    else if (x.id === "lighting")
      s += `<path d="M0 5v-58q0-7 12-5" stroke="#8e9684" stroke-width="3"/><ellipse cx="12" cy="-58" rx="8" ry="3" fill="#e9c36c"/><ellipse cy="4" rx="25" ry="11" fill="#eddfad" opacity=".5"/>`;
    else if (x.id === "mural")
      s += `<path d="M-27-17l58 15v23l-58-15Z" fill="#d1a7a0"/><path d="M-24 0q20-35 29 6T28 7" fill="none" stroke="#f6e1a9" stroke-width="8"/><path d="M-12-14l14 22" stroke="#7ea79b" stroke-width="10"/>`;
    else
      s += `<path d="M-30-4l39 10 25-19-39-10Z" fill="#afb4a3" stroke="#899480"/><path d="M-20-7l38 10M-10-15l36 10M-11 0l24-19M0 4l23-19" stroke="#dbe0d1" stroke-width="2"/>`;
    s += "</g>";
  }
  s += `<g transform="translate(367 251)"><ellipse cy="6" rx="9" ry="4" fill="#b9c6ac"/><path d="M0 0v-13" stroke="#c17d60" stroke-width="5"/><circle cy="-19" r="4" fill="#dab297"/><path d="M0-1l-3 9M0-1l4 7" stroke="#586f67" stroke-width="2"/></g><g transform="translate(303 221)"><circle cy="-17" r="4" fill="#b0876e"/><path d="M0-12v12" stroke="#e7c165" stroke-width="6"/><circle cx="-1" cy="5" r="7" stroke="#667975" stroke-width="2" fill="none"/><path d="M1-3h9v10" stroke="#667975" stroke-width="2" fill="none"/></g></g>`;
  $("#park").innerHTML = s;
}
function update() {
  result = solve(c);
  localStorage.setItem("common-ground-v1", JSON.stringify(c));
  $("#budget").value = c.budget;
  $("#budget-out").textContent = "€" + c.budget + "k";
  $("#space").value = c.space;
  $("#maintenance").value = c.maintenance;
  $("#priorities").innerHTML = rules
    .map(
      (r) =>
        `<div class="priority"><div class="priority-head"><label for="min-${r.id}">${r.label}</label><output>${c.minimums[r.id]}</output></div><input aria-label="Minimum ${r.label}" id="min-${r.id}" data-priority="${r.id}" type="range" min="0" max="25" value="${c.minimums[r.id]}"></div>`,
    )
    .join("");
  $("#interventions").innerHTML = interventions
    .map(
      (x, i) =>
        `<div class="choice ${result.best?.ids.includes(x.id) ? "selected" : ""} ${c.excluded.includes(x.id) ? "excluded" : ""}" title="${esc(x.description)}"><div class="choice-icon">${icons[i]}</div><div class="choice-name">${x.short}<span>€${x.cost}k · care ${x.maintenance}</span></div><div class="choice-actions"><button data-lock="${x.id}" aria-label="Protect ${x.short}" aria-pressed="${c.locked.includes(x.id)}" title="Protect this choice">♡</button><button class="exclude" data-exclude="${x.id}" aria-label="Exclude ${x.short}" aria-pressed="${c.excluded.includes(x.id)}" title="Leave this out">−</button></div></div>`,
    )
    .join("");
  $("#status-pill").className = "pill " + (result.best ? "" : "warning");
  $("#status-pill").textContent = result.best
    ? "A PLAN THAT FITS"
    : "LET’S FIND COMMON GROUND";
  if (result.best) {
    const p = result.best;
    $("#outcome").innerHTML =
      `<div class="summary-row"><h3>${p.ids.length} small changes. One shared place.</h3><span>€${p.cost}k of €${c.budget}k</span></div><div class="metrics">${rules.map((r) => `<div class="metric"><b>${p[r.id]}</b><small>/ ${c.minimums[r.id]}</small><span>${r.label}</span><div class="meter"><i style="width:${Math.min(100, (p[r.id] / 25) * 100)}%"></i></div></div>`).join("")}</div>`;
  } else
    $("#outcome").innerHTML =
      `<div class="summary-row"><h3>These priorities need more room.</h3><span>0 feasible combinations</span></div><p class="warning-copy">Nothing has been quietly dropped. ${result.core.length} requirements form a verified conflict. ${result.repairs.length ? "Choose a change below, or adjust the priorities together." : "Try changing more than one priority, or unprotecting an intervention."}</p><div class="repairs">${result.repairs
        .slice(0, 3)
        .map((r, i) => `<button data-repair="${i}">${esc(r.label)} →</button>`)
        .join("")}</div>`;
  $("#proof-status").textContent =
    "◎ " +
    result.checked.toLocaleString() +
    " combinations checked · " +
    result.count +
    " fit";
  svg();
  reason();
}
function reason() {
  const verified = verifyCertificate(c, result);
  $("#reason-title").textContent = result.best
    ? "A feasible plan. An inspectable choice."
    : "The conflict, with nothing hidden.";
  $("#reason-copy").textContent = result.best
    ? `${result.count} combinations meet every requirement. This one maximizes the equally weighted sum of design points, with lower cost and care as tie-breakers. Another choice may better reflect your community; change the inputs together.`
    : "This is an irreducible conflict. These requirements cannot all hold, but removing any single one from this set makes the remaining set feasible. Other constraints outside this set may still prevent the full plan. The listed repairs are checked against the full scenario.";
  $("#reason-detail").innerHTML = result.best
    ? `<ul>${result.best.ids
        .map((id) => {
          let x = interventions.find((x) => x.id === id);
          return `<li>${x.name} · €${x.cost}k</li>`;
        })
        .join(
          "",
        )}</ul><p>Budget: €${result.best.cost}k / €${c.budget}k · Space: ${result.best.space} / ${c.space} · Care: ${result.best.maintenance} / ${c.maintenance}<br>Certificate: ${verified ? "verified by the independent verifier" : "FAILED"}. Alternatives available: ${Math.max(0, result.count - 1)}.</p>`
    : `<ul>${result.core.map((x) => `<li>${esc(x.label)}</li>`).join("")}</ul><p>Irreducibility certificate: ${verified ? "verified" : "FAILED"}. ${result.repairs.length} independently checked single-requirement repairs.</p>`;
}
$("#priorities").addEventListener("change", (e) => {
  if (e.target.dataset.priority) {
    c.minimums[e.target.dataset.priority] = Number(e.target.value);
    update();
  }
});
$("#budget").addEventListener("input", (e) => {
  c.budget = Number(e.target.value);
  update();
});
for (const k of ["space", "maintenance"])
  $("#" + k).addEventListener("change", (e) => {
    c[k] = Math.max(0, Number(e.target.value) || 0);
    update();
  });
$("#interventions").addEventListener("click", (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  const type = b.dataset.lock ? "locked" : "excluded",
    other = type === "locked" ? "excluded" : "locked",
    id = b.dataset.lock || b.dataset.exclude;
  if (c[type].includes(id)) c[type] = c[type].filter((x) => x !== id);
  else {
    c[type].push(id);
    c[other] = c[other].filter((x) => x !== id);
  }
  update();
});
$("#outcome").addEventListener("click", (e) => {
  const b = e.target.closest("[data-repair]");
  if (!b) return;
  Object.assign(c, result.repairs[Number(b.dataset.repair)].patch);
  update();
});
document.querySelectorAll("[data-scenario]").forEach((b) =>
  b.addEventListener("click", () => {
    document
      .querySelectorAll("[data-scenario]")
      .forEach((x) => x.classList.toggle("active", x === b));
    c = copy(defaults);
    if (b.dataset.scenario === "heat") {
      c.minimums.shade = 17;
      c.budget = 65;
    }
    if (b.dataset.scenario === "cut") c.budget = 30;
    update();
  }),
);
$("#reset").onclick = () => {
  c = copy(defaults);
  update();
};
$("#certificate").onclick = () => {
  $("#reasoning").classList.toggle("hidden");
  if (!$("#reasoning").classList.contains("hidden"))
    $("#reasoning").scrollIntoView({ behavior: "smooth", block: "center" });
};
$("#how").onclick = () => $("#info").showModal();
$("#close-info").onclick = () => $("#info").close();
$("#export").onclick = () => {
  const payload = {
    project: "Common Ground",
    version: 1,
    createdAt: new Date().toISOString(),
    notice:
      "All costs and scores are illustrative workshop assumptions. Not a construction plan or measured impact prediction.",
    scenario: c,
    result,
    verified: verifyCertificate(c, result),
    interventions,
  };
  const a = document.createElement("a"),
    url = URL.createObjectURL(
      new Blob([JSON.stringify(payload, null, 2)], {
        type: "application/json",
      }),
    );
  a.href = url;
  a.download = "common-ground-proposal.json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
update();
