"use client" // Add this at the top because we need usePathname

import Link from 'next/link';
import { usePathname } from 'next/navigation'; // Import hook
import { ModeToggle } from './mode-toggle';
import { MobileMenu } from './MobileMenu';
import { navLinks } from '@/constants';
import { cn } from '@/lib/utils'; // Import cn utility

export default function Navbar() {
  const pathname = usePathname(); // Get current path

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-100 bg-gray-300/80 backdrop-blur-md dark:border-gray-800 dark:bg-gray-950/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Left Side: Mobile Menu & Logo */}
        <div className="flex items-center gap-2">
          <MobileMenu />
          
          <Link href="/" className="text-2xl font-bold tracking-wider text-gray-900 dark:text-white uppercase font-googleSans">
            SHOP
          </Link>
        </div>

        {/* Center Navigation - Desktop */}
        <nav className="hidden md:flex gap-8 h-full"> 
           {navLinks.slice(0, 3).map((link) => {
             const isActive = pathname === link.path;
             return (
               <Link 
                  key={link.path} 
                  href={link.path}
                  className={cn(
                    "flex items-center text-sm font-medium transition-all font-googleSans border-b-2 h-full",
                    isActive 
                      ? "border-black text-black dark:border-white dark:text-white" 
                      : "border-transparent text-gray-600 hover:text-black hover:border-gray-300 dark:text-gray-300 dark:hover:text-white dark:hover:border-gray-600"
                  )}
               >
                  {link.label}
               </Link>
             )
           })}
        </nav>

        {/* Right Side - Auth Buttons */}
        <div className="flex items-center gap-4">
          <ModeToggle />
          
          <Link 
            href="/login" 
            className="hidden sm:block text-sm font-googleSans font-medium text-gray-700 hover:text-black dark:text-gray-300 dark:hover:text-white transition-colors"
          >
            Log in
          </Link>
          <Link 
            href="/register" 
            className="hidden sm:block rounded-full bg-black px-5 py-2 text-sm font-googleSans font-medium text-white transition-colors hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200"
          >
            Register
          </Link>
        </div>

      </div>
    </header>
  );
}