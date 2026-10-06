import {callVerifier,verificationDomain} from "../src/adapter";

const base={protocol:"relay",chainId:61999,message:"payload",signature:"0xsig"};
if(verificationDomain(base)!=="relay:61999")throw new Error("domain binding regression");
if(callVerifier(base).args.length!==3)throw new Error("new verifier signature not used");
try{verificationDomain({...base,chainId:0});throw new Error("invalid chain accepted")}catch(e){if(String(e).includes("invalid chain accepted"))throw e}
