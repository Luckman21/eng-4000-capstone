
import './globals.css';
export const metadata = {
    title: 'Pantheon Inventory Management',
    
}


import { Providers } from './Providers';

export default function RootLayout({children}: { children: React.ReactNode }) {
  return (
    <html lang="en" className='dark'>
      <head>
        <title>{metadata.title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/svg+xml" href="/logo.svg" />
      </head>
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}