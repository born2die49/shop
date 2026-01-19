import { LucideIcon } from "lucide-react";

// --- GENERIC TYPES ---

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface QueryParams {
  page?: number;
  search?: string;
  ordering?: string;
}

// --- AUTH & USER TYPES ---

export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
}

export interface UserProfile {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  phone_number: string;
  avatar: string | null;
  gender: string;
  country: string;
  city: string;
  address_line_1?: string;
  address_line_2?: string;
  date_joined: string;
  trust_score: number;
}

export interface LoginResponse {
  message: string;
  role?: "customer" | "staff";
}

export interface SocialAuthResponse {
  message: string;
}

// --- PRODUCT & CATEGORY TYPES ---

export interface Category {
  id: string;
  name: string;
  slug: string;
  image: string | null;
}

export interface Product {
  id: string;
  name: string;
  slug: string;
  description: string;
  price: number; // Decimal comes as string or number depending on config, usually number in JS
  old_price: number | null;
  image: string;
  quantity: number;
  category_slug: string;
  category_name: string;
  is_active: boolean;
}

export interface NavLink {
	path: string;
	label: string;
	icon: LucideIcon;
}

// API Responses for Products
export type CategoryListResponse = PaginatedResponse<Category>
export type ProductListResponse = PaginatedResponse<Product>

export interface ProductQuery extends QueryParams {
  category?: string; // slug
  price_min?: number;
  price_max?: number;
}

// --- CART TYPES (Client Side) ---

export interface CartItem {
  id: string; // Product ID
  slug: string;
  name: string;
  price: number;
  image: string;
  quantity: number; // Selected Qty
  stock: number; // Max available
}

export interface CartState {
  cartItems: CartItem[];
  totalAmount: number;
  totalQuantity: number;
}

// --- ORDER & CHECKOUT TYPES ---

export type PaymentMethod = "cod" | "bkash";

export interface OrderItem {
  product: string; // Product ID or Name
  product_name: string;
  product_image: string;
  price: number;
  quantity: number;
  sub_total: number;
}

export interface Order {
  id: string; // UUID
  order_number: string;
  user: string; // User ID or Username
  full_name: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  country: string;
  phone_number: string;
  payment_method: PaymentMethod;
  shipping_price: number;
  total_amount: number;
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  is_paid: boolean;
  order_items: OrderItem[];
  created_at: string;
}

export interface CreateOrderPayload {
  address_line_1: string;
  address_line_2?: string;
  city: string;
  phone_number: string;
  payment_method: PaymentMethod;
  order_items: {
    product: string; // Product ID
    quantity: number;
  }[];
}

export type OrderListResponse = PaginatedResponse<Order>