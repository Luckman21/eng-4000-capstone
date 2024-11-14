import './globals.css';
export const metadata = {
    title: 'Pantheon Inventory Management',
    description: 'Discover the best cars in the world',
    
}


import { Providers } from './Providers';

export default function RootLayout({children}: { children: React.ReactNode }) {
  return (
    <html lang="en" className='dark'>
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}