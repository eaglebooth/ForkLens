import type {Metadata} from "next";
import "./globals.css";
export const metadata:Metadata={title:"ForkLens | Dependency upgrade gate",description:"Semantic compatibility review for exact Web3 dependency revisions"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
