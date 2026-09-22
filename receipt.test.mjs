import test from 'node:test';
import assert from 'node:assert/strict';
import {defaults,interventions,solve} from './engine.mjs';
import {replayProposal} from './receipt.mjs';
function proposal(budget){const scenario={...structuredClone(defaults),budget};return{project:'Common Ground',version:1,scenario,result:solve(scenario),interventions:structuredClone(interventions),verified:true};}
test('replay rejects repeated constraints before expensive conflict extraction',()=>{for(const field of ['locked','excluded']){const p=proposal(30);p.scenario[field]=Array(10000).fill(interventions[0].id);assert.throws(()=>replayProposal(p),/at most once/);p.scenario[field]=[interventions[0].id,interventions[0].id];assert.throws(()=>replayProposal(p),/at most once/);}});
test('replay accepts both a repaired plan and an infeasibility certificate',()=>{assert.equal(replayProposal(proposal(37)).result.count,1);assert.equal(replayProposal(proposal(30)).result.count,0);});
test('a forged count or selected score cannot pass on the saved verified flag',()=>{for(const field of ['count','checked']){const p=proposal(37);p.result[field]++;assert.throws(()=>replayProposal(p),/fresh search/);}const p=proposal(37);p.result.best.access++;assert.throws(()=>replayProposal(p),/fresh search/);});
test('modified source costs, unknown versions and inconsistent conflicts are rejected',()=>{const p=proposal(37);p.interventions[0].cost=0;assert.throws(()=>replayProposal(p),/definitions/);const q=proposal(30);q.result.core.pop();assert.throws(()=>replayProposal(q),/fresh search/);assert.throws(()=>replayProposal({...proposal(37),version:2}),/version 1/);});
