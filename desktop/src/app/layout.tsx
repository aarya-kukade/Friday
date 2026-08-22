import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets:  ['latin'],
  weight:   ['400', '500', '600', '700'],
  variable: '--font-inter',
  display:  'swap',
});

export const metadata: Metadata = {
  title:       'FRIDAY — Voice AI Assistant',
  description: 'FRIDAY is a professional AI voice assistant providing direct, real-time voice conversation with advanced AI.',
  keywords:    ['AI assistant', 'voice AI', 'FRIDAY', 'voice interface', 'AI operating system'],
  robots:      'noindex',
};

export const viewport: Viewport = {
  width:        'device-width',
  initialScale: 1,
  themeColor:   '#0F1419',
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${inter.variable} h-full`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
