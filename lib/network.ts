import { studionet } from "genlayer-js/chains";
export const chain = studionet;
export const defaultContract = () =>
  process.env.NEXT_PUBLIC_CONTRACT_ADDRESS || "0xbA4A7b2A758993E1934657CB505dC2a7a97df091";
export const txExplorer = (hash:string) => `${process.env.NEXT_PUBLIC_EXPLORER_TX_BASE || "https://explorer-studio.genlayer.com/tx/"}${hash}`;
export const addressExplorer = (address:string) => `https://explorer-studio.genlayer.com/address/${address}`;
