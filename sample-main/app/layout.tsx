import {Inter} from 'next/font/google';
import type {Metadata} from 'next';

const inter = Inter({subsets: ['latin']});

export const metadata: Metadata = {
  title: 'Unimelb Handbook Chatbot',
  description: 'Demo Chatbot for the Unimelb Handbook'
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
