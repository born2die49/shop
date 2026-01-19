import { Home, Store, Layers, ShoppingCart, User, Package } from "lucide-react";
import { NavLink } from "@/types";

export const paymentMethods = [
	{ value: "cod", label: "Cash on Delivery" },
	{ value: "bkash", label: "bKash" },
];

export const genderOptions = [
	{ value: "MALE", label: "Male" },
	{ value: "FEMALE", label: "Female" },
	{ value: "OTHER", label: "Other" },
];

// Matches your Django Profile Model Divisions
export const bdDivisions = [
	{ value: "DHAKA", label: "Dhaka" },
	{ value: "CHATTOGRAM", label: "Chattogram" },
	{ value: "KHULNA", label: "Khulna" },
	{ value: "RAJSHAHI", label: "Rajshahi" },
	{ value: "BARISHAL", label: "Barishal" },
	{ value: "SYLHET", label: "Sylhet" },
	{ value: "RANGPUR", label: "Rangpur" },
	{ value: "MYMENSINGH", label: "Mymensingh" },
];

export const productSortOptions = [
	{ value: "-created_at", label: "Newest" },
	{ value: "price", label: "Price: Low to High" },
	{ value: "-price", label: "Price: High to Low" },
];

export const navLinks: NavLink [] = [
	{
		path: "/",
		label: "Home",
		icon: Home,
	},
	{
		path: "/products",
		label: "Shop",
		icon: Store,
	},
	{
		path: "/categories",
		label: "Categories",
		icon: Layers,
	},
	{
		path: "/cart",
		label: "Cart",
		icon: ShoppingCart,
	},
	{
		path: "/profile",
		label: "My Profile",
		icon: User,
	},
	{
		path: "/orders",
		label: "My Orders",
		icon: Package,
	},
];
