import hashlib,json
P="relay-sdk";C=P+".upgrade";DB="1"*40;DT="2"*40;CB="3"*40;CT="4"*40;DEP="acme/dependency";CON="acme/consumer";PROD="src/adapter.ts";TEST="tests/adapter.test.ts"
def canon(v):return json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(",",":"))
def cmp(base,head,files):return {"status":"ahead","base_commit":{"sha":base},"commits":[{"sha":head}],"files":[{"filename":p,"patch":x} for p,x in files]}
def web(vm,prod=True,tests=True,ci=True,up=True,dependency_head=DT):
 d=cmp(DB,dependency_head,[("CHANGELOG.md","- verify(message,sig)\n+ verify(domain,message,sig)")]);fs=[]
 if prod:fs.append((PROD,"+ verifier(domain,message,signature)"))
 if tests:fs.append((TEST,"+ assert domain bound"))
 c=cmp(CB,CT,fs);r={"check_runs":[{"name":"regression","head_sha":CT,"status":"completed","conclusion":"success" if ci else "failure","app":{"slug":"github-actions"}}]};status=200 if up else 503
 vm.mock_web(r"acme/dependency/compare",{"method":"GET","status":status,"body":json.dumps(d) if up else "down"});vm.mock_web(r"acme/consumer/compare",{"method":"GET","status":status,"body":json.dumps(c) if up else "down"});vm.mock_web(r"check-runs",{"method":"GET","status":status,"body":json.dumps(r) if up else "down"});return d,c,r
def proof(d,c,r):
 def norm(x,b,h):return {"ok":True,"base":b,"head":h,"changed":[f["filename"] for f in x["files"]],"patches":[{"path":f["filename"],"patch":f["patch"]} for f in x["files"]]}
 dn,cn=norm(d,DB,DT),norm(c,CB,CT);run={"name":"regression","head_sha":CT,"status":"completed","conclusion":r["check_runs"][0]["conclusion"],"app":"github-actions"};ok=run["conclusion"]=="success"
 f={"dependency_compare":dn,"consumer_compare":cn,"checks":{"ok":ok,"error":"" if ok else "NO_SUCCESSFUL_EXACT_HEAD_CHECK","runs":[run]},"production_paths":[PROD],"test_paths":[TEST]};f["production_changed"]=PROD in cn["changed"];f["tests_changed"]=TEST in cn["changed"];return hashlib.sha256(canon(f).encode()).hexdigest()
def boot(deploy):
 c=deploy("contracts/fork_lens.py");c.register_project(P,DEP,CON,DB,CB);c.open_candidate(C,P,DB,DT,CB,CT,PROD,TEST);return c
def ai(vm,p,v="COMPATIBLE",issues=None):vm.mock_llm(r"Judge whether consumer",json.dumps({"verdict":v,"issues":issues or [],"summary":"Implementation and regression patches cover the dependency change.","proof_digest":p}));vm.mock_llm(r"Independently validate",'{"valid":true}')
def test_schema_deployer_neutral(direct_deploy,direct_vm,direct_alice):
 c=direct_deploy("contracts/fork_lens.py");v=json.loads(c.get_contract_version());assert v["version"]==4 and v["schema"]=="github-authoritative-dependency-gate-v4"
 with direct_vm.prank(direct_alice):c.register_project(P,DEP,CON,DB,CB)
 assert json.loads(c.get_project(P))["owner"].endswith(bytes(direct_alice).hex())
def test_same_repo_rejected(direct_deploy,direct_vm):
 c=direct_deploy("contracts/fork_lens.py")
 with direct_vm.expect_revert("INVALID_PROJECT"):c.register_project(P,DEP,DEP,DB,CB)
def test_authoritative_happy_path(direct_deploy,direct_vm):
 c=boot(direct_deploy);d,x,r=web(direct_vm);p=proof(d,x,r);ai(direct_vm,p);assert c.assess_candidate(C)=="COMPATIBLE";a=json.loads(c.get_candidate(C));assert a["proof_digest"]==p;c.activate_candidate(C,a["attestation_digest"]);assert json.loads(c.get_project(P))["epoch"]==2
def test_missing_ci_blocks(direct_deploy,direct_vm):c=boot(direct_deploy);web(direct_vm,ci=False);assert c.assess_candidate(C)=="INSUFFICIENT_EVIDENCE";assert json.loads(c.get_candidate(C))["status"]=="BLOCKED"
def test_missing_production_blocks(direct_deploy,direct_vm):c=boot(direct_deploy);web(direct_vm,prod=False);assert c.assess_candidate(C)=="INSUFFICIENT_EVIDENCE"
def test_missing_tests_blocks(direct_deploy,direct_vm):c=boot(direct_deploy);web(direct_vm,tests=False);assert c.assess_candidate(C)=="INSUFFICIENT_EVIDENCE"
def test_unavailable_fails_closed(direct_deploy,direct_vm):c=boot(direct_deploy);web(direct_vm,up=False);assert c.assess_candidate(C)=="SOURCE_UNAVAILABLE";assert not json.loads(c.get_candidate(C))["attestation_digest"]
def test_compare_head_mismatch_fails_closed(direct_deploy,direct_vm):
 c=boot(direct_deploy);web(direct_vm,dependency_head="9"*40);assert c.assess_candidate(C)=="SOURCE_UNAVAILABLE"
def test_semantic_conflict_blocks(direct_deploy,direct_vm):c=boot(direct_deploy);d,x,r=web(direct_vm);p=proof(d,x,r);ai(direct_vm,p,"INCOMPATIBLE",["DOMAIN_NOT_BOUND"]);assert c.assess_candidate(C)=="INCOMPATIBLE"
def test_wrong_actor_digest_replay(direct_deploy,direct_vm,direct_alice):
 c=boot(direct_deploy);d,x,r=web(direct_vm);ai(direct_vm,proof(d,x,r));c.assess_candidate(C);before=json.loads(c.get_candidate(C))
 with direct_vm.prank(direct_alice),direct_vm.expect_revert("PROJECT_OWNER_REQUIRED"):c.activate_candidate(C,before["attestation_digest"])
 with direct_vm.expect_revert("ATTESTATION_BINDING_MISMATCH"):c.activate_candidate(C,"f"*64)
 assert json.loads(c.get_candidate(C))==before;c.activate_candidate(C,before["attestation_digest"]);after=json.loads(c.get_candidate(C))
 with direct_vm.expect_revert("ATTESTATION_NOT_AVAILABLE"):c.activate_candidate(C,before["attestation_digest"])
 assert json.loads(c.get_candidate(C))==after
def test_runner_pin():assert open("contracts/fork_lens.py",encoding="utf-8").read().splitlines()[:2]==["# v0.2.16",'# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }']
def test_semantic_prompt_names_adversarial_failures():
 source=open("contracts/fork_lens.py",encoding="utf-8").read();assert "hard-codes a value" in source and "returns success unconditionally" in source and "tests merely codify the unsafe behavior" in source
