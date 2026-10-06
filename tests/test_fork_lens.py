import json

PROJECT="relay-sdk"; CANDIDATE=PROJECT+".upgrade-01"
DB="1"*40; DT="2"*40; CB="3"*40; CT="4"*40; DIGEST="a"*64

def bootstrap(deploy):
    c=deploy("contracts/fork_lens.py")
    c.register_project(PROJECT,"https://github.com/example/dependency","https://github.com/example/consumer",DB,CB)
    c.open_candidate(CANDIDATE,PROJECT,DB,DT,CB,CT,"src/adapter.ts src/verifier.ts","tests/adapter.test.ts")
    return c

def add_required(c):
    for kind,sha in (("DEPENDENCY_DIFF",DT),("CONSUMER_DIFF",CT),("REGRESSION_TESTS",CT),("CI_RESULT",CT)):
        c.add_evidence(CANDIDATE,kind,f"https://raw.githubusercontent.com/example/repo/{sha}/{kind.lower()}.json",sha,DIGEST,"Exact commit-pinned evidence for compatibility review")

def mock(vm,verdict="COMPATIBLE",issues=None,valid=True):
    vm.mock_llm(r"Assess whether a Web3 consumer",json.dumps({"verdict":verdict,"issues":issues or [],"summary":"The exact implementation and regression evidence cover the dependency breaking change."}))
    vm.mock_llm(r"Independently validate a dependency",json.dumps({"valid":valid}))

def test_deployer_has_no_global_authority(direct_deploy,direct_vm,direct_alice):
    c=direct_deploy("contracts/fork_lens.py")
    with direct_vm.prank(direct_alice): c.register_project(PROJECT,"https://github.com/example/dependency","https://github.com/example/consumer",DB,CB)
    assert json.loads(c.get_project(PROJECT))["owner"].endswith(bytes(direct_alice).hex())
    with direct_vm.expect_revert("PROJECT_OWNER_REQUIRED"): c.open_candidate(CANDIDATE,PROJECT,DB,DT,CB,CT,"src/a.ts","tests/a.ts")

def test_happy_path_attests_and_activates(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy);add_required(c);c.seal_candidate(CANDIDATE);mock(direct_vm)
    assert c.assess_candidate(CANDIDATE)=="COMPATIBLE"
    x=json.loads(c.get_candidate(CANDIDATE));assert x["status"]=="ATTESTED" and x["attestation_digest"]
    c.activate_candidate(CANDIDATE,x["attestation_digest"])
    p=json.loads(c.get_project(PROJECT));x=json.loads(c.get_candidate(CANDIDATE))
    assert p["active_dependency"]==DT and p["active_consumer"]==CT and p["epoch"]==2 and x["status"]=="ACTIVATED"

def test_required_evidence_cannot_be_replaced_by_report(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy)
    c.add_evidence(CANDIDATE,"MIGRATION_NOTE","https://github.com/example/consumer/blob/main/MIGRATION.md",CT,DIGEST,"Author migration report")
    with direct_vm.expect_revert("REQUIRED_EVIDENCE_MISSING"): c.seal_candidate(CANDIDATE)

def test_missing_required_slot_rejects_seal(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy)
    with direct_vm.expect_revert("REQUIRED_EVIDENCE_MISSING"): c.seal_candidate(CANDIDATE)

def test_wrong_commit_evidence_rolls_back(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy);before=json.loads(c.get_candidate(CANDIDATE))
    with direct_vm.expect_revert("EVIDENCE_REVISION_MISMATCH"):
        c.add_evidence(CANDIDATE,"CI_RESULT",f"https://example.com/{CB}/ci.json",CB,DIGEST,"CI for stale commit")
    assert json.loads(c.get_candidate(CANDIDATE))==before

def test_duplicate_slot_is_rejected_without_mutation(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy);url=f"https://raw.githubusercontent.com/example/dependency/{DT}/diff.json"
    c.add_evidence(CANDIDATE,"DEPENDENCY_DIFF",url,DT,DIGEST,"Dependency diff")
    before=json.loads(c.get_candidate(CANDIDATE))
    with direct_vm.expect_revert("EVIDENCE_SLOT_ALREADY_FILLED"): c.add_evidence(CANDIDATE,"DEPENDENCY_DIFF",url,DT,DIGEST,"Duplicate")
    assert json.loads(c.get_candidate(CANDIDATE))==before

def test_semantic_non_positive_never_creates_attestation(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy);add_required(c);c.seal_candidate(CANDIDATE);mock(direct_vm,"INCOMPATIBLE",["AUTH_DOMAIN_NOT_BOUND"])
    assert c.assess_candidate(CANDIDATE)=="INCOMPATIBLE"
    x=json.loads(c.get_candidate(CANDIDATE));assert x["status"]=="BLOCKED" and not x["attestation_digest"]

def test_malformed_consensus_fails_closed(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy);add_required(c);c.seal_candidate(CANDIDATE)
    direct_vm.mock_llm(r"Assess whether a Web3 consumer",'{"verdict":"COMPATIBLE","issues":["HIDDEN"]}')
    direct_vm.mock_llm(r"Independently validate a dependency",'{"valid":true}')
    assert c.assess_candidate(CANDIDATE)=="INSUFFICIENT_EVIDENCE"
    assert json.loads(c.get_candidate(CANDIDATE))["status"]=="BLOCKED"

def test_wrong_attestation_and_replay_preserve_state(direct_deploy,direct_vm):
    c=bootstrap(direct_deploy);add_required(c);c.seal_candidate(CANDIDATE);mock(direct_vm);c.assess_candidate(CANDIDATE)
    before=json.loads(c.get_candidate(CANDIDATE))
    with direct_vm.expect_revert("ATTESTATION_BINDING_MISMATCH"): c.activate_candidate(CANDIDATE,"b"*64)
    assert json.loads(c.get_candidate(CANDIDATE))==before
    c.activate_candidate(CANDIDATE,before["attestation_digest"]);after=json.loads(c.get_candidate(CANDIDATE))
    with direct_vm.expect_revert("ATTESTATION_NOT_AVAILABLE"): c.activate_candidate(CANDIDATE,before["attestation_digest"])
    assert json.loads(c.get_candidate(CANDIDATE))==after

def test_schema_and_runner_pin(direct_deploy):
    c=direct_deploy("contracts/fork_lens.py");assert json.loads(c.get_contract_version())["schema"]=="semantic-dependency-upgrade-gate-v1"
    assert open("contracts/fork_lens.py",encoding="utf-8").read().splitlines()[:2]==["# v0.2.16",'# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }']
