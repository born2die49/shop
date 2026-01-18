import Link from 'next/link';
import { ModeToggle } from './mode-toggle';

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-100 bg-gray-300/80 backdrop-blur-md dark:border-gray-800 dark:bg-gray-950/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Logo Section */}
        <div className="flex items-center">
          <Link href="/" className="text-2xl font-bold tracking-wider text-gray-900 dark:text-white uppercase">
            SHOP
          </Link>
        </div>

        {/* Center Navigation - Empty for now */}
        <nav className="hidden md:block">
           {/* Menu items will go here later */}
        </nav>

        {/* Right Side - Auth Buttons */}
        <div className="flex items-center gap-4">
          {/* Theme Toggle */}
          <ModeToggle />

          <Link 
            href="/login" 
            className="text-sm font-googleSans font-medium text-gray-700 hover:text-black dark:text-gray-300 dark:hover:text-white transition-colors"
          >
            Log in
          </Link>
          <Link 
            href="/register" 
            className="rounded-full bg-black px-5 py-2 text-sm font-googleSans font-medium text-white transition-colors hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200"
          >
            Register
          </Link>
        </div>

      </div>
    </header>
  );
}