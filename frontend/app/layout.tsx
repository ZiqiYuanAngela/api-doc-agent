import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "API Documentation Agent",
  description:
    "An AI-powered tool for exploring and validating OpenAPI specifications.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}