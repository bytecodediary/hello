export interface PropertyImage {
  id: number;
  image: string;
  image_alt: string;
}

export interface PropertyFeature {
  feature_name: string;
  feature_value: number;
}

export interface PropertyOwner {
  id: number;
  user: string;
  property_details: string | null;
  phone_number: string | null;
  properties?: number;
}

export interface PropertyRecord {
  slug: string;
  title: string;
  description: string;
  price: number;
  city: string;
  address: string;
  status: "sold" | "pending" | "available";
  listed_at: string;
  updated_at: string;
  images?: PropertyImage[];
  features?: PropertyFeature[];
  owners?: PropertyOwner[];
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiErrorResponse {
  detail?: string;
  [key: string]: unknown;
}

export interface CartItemRecord {
  slug: string;
  property: number;
  property_name: string;
  property_price: number;
  quantity: number;
  line_total: number;
}

export interface CartRecord {
  slug: string;
  total_price: number;
  items: CartItemRecord[];
}

export interface OrderItemRecord {
  slug: string;
  property: number;
  property_name: string;
  price_each: number;
  quantity: number;
  line_total: number;
}

export interface OrderRecord {
  slug: string;
  status: string;
  created_at: string;
  updated_at: string;
  items: OrderItemRecord[];
  total: number;
}

export interface PaymentSummary {
  id: number;
  price: string;
  payment_mode: string;
  description: string;
  added_at: string;
}

export interface TransactionRecord {
  id: number;
  amount: number;
  date_paid: string;
  transaction_desc: string;
  status: string;
  transaction_type: string;
  payment: number;
  payment_details: PaymentSummary;
}

export interface PaymentRecord extends PaymentSummary {
  updated_at: string;
  transactions: TransactionRecord[];
}

export interface NotificationRecord {
  id: number;
  message: string;
  user: string;
  received_at: string;
  is_read: boolean;
}

export interface AuthCheckResponse {
  authenticated: boolean;
  username?: string;
  email?: string;
}

export interface CustomUserRecord {
  id: string;
  username: string;
  first_name: string;
  email: string;
}

export interface TenantProfileRecord {
  user: CustomUserRecord;
  email: string;
  phone_number: string;
  lease_agreement: string;
  rent_status: number | null;
  rent_status_summary: PaymentSummary | null;
  has_paid: boolean;
}
