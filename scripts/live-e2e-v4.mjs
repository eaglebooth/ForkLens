import { mkdirSync, writeFileSync } from "node:fs";
import { createInterface } from "node:readline";
import { createAccount, createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

const CONTRACT = process.argv[2];
if (!/^0x[0-9a-fA-F]{40}$/.test(CONTRACT || "")) throw new Error("Usage: node scripts/live-e2e-v4.mjs <contract-address> [run-id]");
const run = process.argv[3] || Date.now().toString().slice(-10);
const project = `vault-${run}`;
const unavailableProject = `unavailable-${run}`;
const ids = {
  happy: `${project}.happy`,
  missingProduction: `${project}.missing-production`,
  missingTests: `${project}.missing-tests`,
  missingChecks: `${project}.missing-checks`,
  conflict: `${project}.semantic-conflict`,
  unavailable: `${unavailableProject}.source-down`,
};
const dependencyRepo = "eaglebooth/forklens-dependency";
const consumerRepo = "eaglebooth/forklens-consumer";
const dependencyBase = "6cc2c3bf8aad0c0c23515e9ac01530c0d08243af";
const dependencyTarget = "59e9de2b40b74f287c0ad9cf2d1ccebf3b74b846";
const consumerBase = "1f22697154ae777b723b81df4fe043ae95d3a9d6";
const consumerTarget = "5113a6eac492e3d135601b2981f858803d094ae5";
const missingChecksTarget = "842d09e63591ee09ba9a1f96d8913f37da775fee";
const conflictTarget = "44d9f604b202661a5dd8cbf3554df2dcf8dd9ab4";
const productionPaths = "src/vault-approval.js,package.json";
const testPaths = "test/vault-approval.test.js";

async function readKeys() {
  const rl = createInterface({ input: process.stdin, terminal: false });
  const lines = [];
  return await new Promise((resolve, reject) => {
    rl.on("line", line => {
      const value = line.trim().replace(/^0x/, "");
      if (value) lines.push(value);
      if (lines.length === 2) { rl.close(); resolve(lines); }
    });
    rl.on("close", () => { if (lines.length < 2) reject(new Error("Two non-deployer wallet inputs are required on stdin")); });
  });
}

const [keyA, keyB] = await readKeys();
const walletA = createAccount(`0x${keyA}`), walletB = createAccount(`0x${keyB}`);
const clientA = createClient({ chain: studionet, account: walletA });
const clientB = createClient({ chain: studionet, account: walletB });
const report = {
  contract: CONTRACT,
  network: "GenLayer StudioNet 61999",
  run,
  actors: { projectOwner: walletA.address, independentAssessor: walletB.address },
  sources: { dependencyRepo, consumerRepo, dependencyBase, dependencyTarget, consumerBase, consumerTarget, missingChecksTarget, conflictTarget },
  transactions: [], assertions: [], final: {},
};
mkdirSync("docs/live-evidence", { recursive: true });
const path = `docs/live-evidence/studionet-v4-${run}.json`;
const save = () => writeFileSync(path, `${JSON.stringify(report, null, 2)}\n`);
const check = (condition, label, details = {}) => { report.assertions.push({ label, pass: Boolean(condition), details }); save(); if (!condition) throw new Error(`Assertion failed: ${label}`); };
const read = async (method, args = []) => JSON.parse(await clientA.readContract({ address: CONTRACT, functionName: method, args }));
const execution = tx => {
  const validators = tx.consensus_data?.validators || [];
  if (validators.some(v => v.vote === "agree" && v.execution_result === "SUCCESS")) return "SUCCESS";
  if (validators.some(v => v.vote === "agree" && v.execution_result === "ERROR")) return "ERROR";
  const leader = tx.consensus_data?.leader_receipt?.[0]?.genvm_result;
  return leader && !leader.error_code ? "SUCCESS" : leader?.error_code ? "ERROR" : "UNKNOWN";
};
const readbackFor = async (method, args) => {
  if (method === "register_project") return read("get_project", [args[0]]);
  if (["open_candidate", "assess_candidate", "activate_candidate"].includes(method)) return read("get_candidate", [args[0]]);
  return null;
};
const write = async (label, client, method, args, expected = "SUCCESS") => {
  const before = await readbackFor(method, args);
  const raw = await client.writeContract({ address: CONTRACT, functionName: method, args, value: 0n });
  const hash = typeof raw === "string" ? raw : raw?.txId;
  process.stdout.write(`${label}: ${hash}\n`);
  let tx = {};
  for (let i = 0; i < 360; i++) {
    try { tx = await client.getTransaction({ hash }); } catch { await new Promise(resolve => setTimeout(resolve, 2500)); continue; }
    if (["FINALIZED", "CANCELED", "UNDETERMINED"].includes(tx.statusName)) break;
    await new Promise(resolve => setTimeout(resolve, 2500));
  }
  const actual = execution(tx);
  const after = await readbackFor(method, args);
  report.transactions.push({ label, caller: client.account?.address, method, args, expected, hash, status: tx.statusName || "UNKNOWN", execution: actual, readback: { before, after } });
  save();
  check(tx.statusName === "FINALIZED" && actual === expected, `${label} finalized with ${expected}`, { hash, status: tx.statusName, execution: actual });
  return hash;
};
const assessWithSourceRetry = async (label, candidatePrefix, consumerHead, production, tests, accept) => {
  for (let attempt = 1; attempt <= 4; attempt++) {
    const candidateId = attempt === 1 ? candidatePrefix : `${candidatePrefix}-retry-${attempt}`;
    if (attempt > 1) await write(`${label} opens source retry ${attempt}`, clientA, "open_candidate", [candidateId, project, dependencyBase, dependencyTarget, consumerBase, consumerHead, production, tests]);
    await write(`${label} assessment ${attempt}`, clientB, "assess_candidate", [candidateId]);
    const state = await read("get_candidate", [candidateId]);
    if (accept(state)) return state;
    check(state.status === "BLOCKED" && state.verdict === "SOURCE_UNAVAILABLE" && !state.attestation_digest, `${label} transient source outage fails closed`, state);
  }
  throw new Error(`${label} exhausted authoritative-source retries`);
};

const version = await read("get_contract_version");
check(version.schema === "github-authoritative-dependency-gate-v4" && version.version === 4, "deployed ForkLens V4 identity", version);
await write("wallet A registers authoritative source pair", clientA, "register_project", [project, dependencyRepo, consumerRepo, dependencyBase, consumerBase]);
await write("wallet A opens happy candidate", clientA, "open_candidate", [ids.happy, project, dependencyBase, dependencyTarget, consumerBase, consumerTarget, productionPaths, testPaths]);
await write("wallet A opens missing-production candidate", clientA, "open_candidate", [ids.missingProduction, project, dependencyBase, dependencyTarget, consumerBase, consumerTarget, "src/not-present.js", testPaths]);
await write("wallet A opens missing-tests candidate", clientA, "open_candidate", [ids.missingTests, project, dependencyBase, dependencyTarget, consumerBase, consumerTarget, productionPaths, "test/not-present.test.js"]);
await write("wallet A opens missing-checks candidate", clientA, "open_candidate", [ids.missingChecks, project, dependencyBase, dependencyTarget, consumerBase, missingChecksTarget, productionPaths, testPaths]);
await write("wallet A opens semantic-conflict candidate", clientA, "open_candidate", [ids.conflict, project, dependencyBase, dependencyTarget, consumerBase, conflictTarget, productionPaths, testPaths]);

const missingProduction = await assessWithSourceRetry("missing production", ids.missingProduction, consumerTarget, "src/not-present.js", testPaths, state => state.status === "BLOCKED" && state.verdict === "INSUFFICIENT_EVIDENCE" && !state.attestation_digest);
check(missingProduction.status === "BLOCKED" && missingProduction.verdict === "INSUFFICIENT_EVIDENCE" && !missingProduction.attestation_digest, "missing production path blocks without attestation", missingProduction);
const missingTests = await assessWithSourceRetry("missing tests", ids.missingTests, consumerTarget, productionPaths, "test/not-present.test.js", state => state.status === "BLOCKED" && state.verdict === "INSUFFICIENT_EVIDENCE" && !state.attestation_digest);
check(missingTests.status === "BLOCKED" && missingTests.verdict === "INSUFFICIENT_EVIDENCE" && !missingTests.attestation_digest, "missing regression path blocks without attestation", missingTests);
const missingChecks = await assessWithSourceRetry("missing checks", ids.missingChecks, missingChecksTarget, productionPaths, testPaths, state => state.status === "BLOCKED" && state.verdict === "INSUFFICIENT_EVIDENCE" && !state.attestation_digest);
check(missingChecks.status === "BLOCKED" && missingChecks.verdict === "INSUFFICIENT_EVIDENCE" && !missingChecks.attestation_digest, "absent exact-head check blocks without attestation", missingChecks);
const conflict = await assessWithSourceRetry("semantic conflict", ids.conflict, conflictTarget, productionPaths, testPaths, state => state.status === "BLOCKED" && state.verdict !== "SOURCE_UNAVAILABLE" && state.verdict !== "COMPATIBLE" && !state.attestation_digest);
check(conflict.status === "BLOCKED" && conflict.verdict !== "COMPATIBLE" && !conflict.attestation_digest, "semantic conflict blocks despite changed paths and green CI", conflict);

await write("wallet A registers unavailable source project", clientA, "register_project", [unavailableProject, "eaglebooth/repository-that-does-not-exist", consumerRepo, dependencyBase, consumerBase]);
await write("wallet A opens unavailable source candidate", clientA, "open_candidate", [ids.unavailable, unavailableProject, dependencyBase, dependencyTarget, consumerBase, consumerTarget, productionPaths, testPaths]);
await write("wallet B assesses unavailable source", clientB, "assess_candidate", [ids.unavailable]);
const unavailable = await read("get_candidate", [ids.unavailable]);
check(unavailable.status === "BLOCKED" && unavailable.verdict === "SOURCE_UNAVAILABLE" && !unavailable.attestation_digest, "unavailable authoritative source fails closed", unavailable);

let happy = await assessWithSourceRetry("happy candidate", ids.happy, consumerTarget, productionPaths, testPaths, state => state.status === "ATTESTED" && state.verdict === "COMPATIBLE" && Boolean(state.attestation_digest));
check(happy.status === "ATTESTED" && happy.verdict === "COMPATIBLE" && Boolean(happy.attestation_digest), "authoritative compatible candidate receives exact attestation", happy);
const beforeWrongActor = happy;
const happyId = happy.candidate_id;
await write("wallet B cannot activate owner candidate", clientB, "activate_candidate", [happyId, happy.attestation_digest], "ERROR");
check(JSON.stringify(await read("get_candidate", [happyId])) === JSON.stringify(beforeWrongActor), "wrong actor preserves candidate state");
await write("wrong digest cannot activate", clientA, "activate_candidate", [happyId, "f".repeat(64)], "ERROR");
check(JSON.stringify(await read("get_candidate", [happyId])) === JSON.stringify(beforeWrongActor), "wrong digest preserves candidate state");
await write("wallet A activates exact attestation", clientA, "activate_candidate", [happyId, happy.attestation_digest]);
happy = await read("get_candidate", [happyId]);
check(happy.status === "ACTIVATED" && happy.activated === true, "exact attestation activates once", happy);
const afterActivation = happy;
await write("activation replay is rejected", clientA, "activate_candidate", [happyId, happy.attestation_digest], "ERROR");
check(JSON.stringify(await read("get_candidate", [happyId])) === JSON.stringify(afterActivation), "replay preserves activated state");

const mainProject = await read("get_project", [project]);
const unavailableProjectState = await read("get_project", [unavailableProject]);
const stats = await read("get_stats");
check(mainProject.epoch === 2 && mainProject.active_dependency === dependencyTarget && mainProject.active_consumer === consumerTarget && stats.open_attestations === 0, "project revision and counters match finalized activation", { mainProject, stats });
report.final = { version, happy, missingProduction, missingTests, missingChecks, conflict, unavailable, mainProject, unavailableProject: unavailableProjectState, stats };
save();
process.stdout.write(`Evidence: ${path}\n`);
