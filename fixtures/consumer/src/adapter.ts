export type VerifyInput = { protocol: string; chainId: number; message: string; signature: string };

export function verificationDomain(input: VerifyInput): string {
  if (!input.protocol.trim() || !Number.isInteger(input.chainId) || input.chainId < 1) throw new Error("INVALID_DOMAIN");
  return `${input.protocol}:${input.chainId}`;
}

export function callVerifier(input: VerifyInput) {
  return { method: "verify", args: [verificationDomain(input), input.message, input.signature] };
}
