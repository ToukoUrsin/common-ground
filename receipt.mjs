import { solve, verifyCertificate, interventions, rules } from './engine.mjs';

const canonical = x => JSON.stringify(x, (_, v) => v && !Array.isArray(v) && typeof v === 'object' ? Object.fromEntries(Object.entries(v).sort(([a], [b]) => a.localeCompare(b))) : v);

export function replayProposal(payload) {
  if (!payload || payload.project !== 'Common Ground' || payload.version !== 1) throw Error('Choose a Common Ground version 1 proposal.');
  if (canonical(payload.interventions) !== canonical(interventions)) throw Error('The intervention definitions differ from this version of the studio. This file cannot be verified here.');
  const actual = solve(payload.scenario);
  if (canonical(actual) !== canonical(payload.result)) throw Error('The saved result does not match a fresh search. The proposal may have been changed.');
  if (!verifyCertificate(payload.scenario, actual)) throw Error('The certificate failed its separate constraint check.');
  return { scenario: structuredClone(payload.scenario), result: actual, interventions, rules };
}
