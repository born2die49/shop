"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
	Menu,
	Home,
	ShoppingBag,
	Layers,
	ShoppingCart,
	User,
	Package,
} from "lucide-react"; // Import specific icons
import {
	Sheet,
	SheetContent,
	SheetTrigger,
	SheetClose,
	SheetHeader,
	SheetTitle,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { navLinks } from "@/constants";
import { cn } from "@/lib/utils";

// Map labels to icons
const iconMap: Record<string, React.ElementType> = {
	Home: Home,
	Shop: ShoppingBag,
	Categories: Layers,
	Cart: ShoppingCart,
	"My Profile": User,
	"My Orders": Package,
};

export function MobileMenu() {
	const pathname = usePathname();

	// Placeholder auth state
	const isAuthenticated = false;

	const protectedRoutes = ["/profile", "/orders"];

	const filteredLinks = navLinks.filter((link) => {
		if (!isAuthenticated && protectedRoutes.includes(link.path)) {
			return false;
		}
		return true;
	});

	return (
		<Sheet>
			<SheetTrigger asChild>
				<Button
					variant="ghost"
					size="icon"
					className="md:hidden text-gray-700 dark:text-gray-200"
				>
					<Menu className="h-6 w-6" />
					<span className="sr-only">Toggle menu</span>
				</Button>
			</SheetTrigger>

			<SheetContent
				side="left"
				className="w-75 sm:w-87.5 bg-white dark:bg-gray-950 border-r-gray-200 dark:border-r-gray-800 flex flex-col h-full"
			>
				<SheetHeader className="mb-8 text-left">
					<SheetTitle className="font-googleSans font-bold text-xl uppercase tracking-wider pl-4 border-l-4 border-black dark:border-white">
						Menu
					</SheetTitle>
				</SheetHeader>

				<nav className="flex flex-col space-y-2">
					{filteredLinks.map((link) => {
						const isActive = pathname === link.path;
						const IconComponent = iconMap[link.label] || Home; // Fallback icon

						return (
							<SheetClose asChild key={link.path}>
								<Link
									href={link.path}
									className={cn(
										"flex items-center gap-4 rounded-lg px-4 py-3 text-sm font-medium transition-all font-googleSans",
										isActive
											? "bg-gray-100 text-black dark:bg-gray-800 dark:text-white shadow-sm" // Modern active style
											: "text-gray-600 hover:bg-gray-50 hover:text-black dark:text-gray-400 dark:hover:bg-gray-900 dark:hover:text-gray-200",
									)}
								>
									<IconComponent
										className={cn(
											"h-5 w-5",
											isActive ? "stroke-2" : "stroke-1",
										)}
									/>
									<span className="text-base">{link.label}</span>
								</Link>
							</SheetClose>
						);
					})}
				</nav>

				{ /* Auth section */}
				{!isAuthenticated && (
          <div className="mt-auto flex flex-col gap-3 pb-8">
             <SheetClose asChild>
                <Link href="/login">
                  <Button variant="outline" className="w-full font-googleSans rounded-full border-gray-300 dark:border-gray-700">
                    Log in
                  </Button>
                </Link>
             </SheetClose>
             <SheetClose asChild>
                <Link href="/register">
                  <Button className="w-full font-googleSans rounded-full font-bold">
                    Register
                  </Button>
                </Link>
             </SheetClose>
          </div>
        )}
			</SheetContent>
		</Sheet>
	);
}
