import Link from 'next/link'
import { Frown } from 'lucide-react'

export default function NotFound() {
  return (
    <main className="flex h-screen flex-col items-center justify-center px-6 py-6 dark:bg-gray-950 sm:py-24 lg:px-8 bg-gray-200">
      <div className="flex flex-col items-center text-center">
        <Frown className="h-32 w-32 text-indigo-600 dark:text-indigo-500" />
        
        <h1 className="mt-4 text-4xl font-googleSans font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl">
          Page not found!
        </h1>
        
        <p className="mt-6 text-base font-roboto leading-7 text-gray-700 dark:text-gray-400 sm:text-2xl">
          Sorry, we did not find the page you are looking for.
        </p>
        
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Link 
            href="/"
            className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-googleSans font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-colors"  
          >
            Go back home
          </Link>
        </div>
      </div>
    </main>
  )
}