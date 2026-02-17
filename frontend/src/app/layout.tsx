import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ORGAN-DPP",
  description: "Molecular generation with Diversity-Promoting Priors",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
