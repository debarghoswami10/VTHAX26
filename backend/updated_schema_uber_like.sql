-- =====================================================
-- UBER-LIKE BOOKING SYSTEM - UPDATED SCHEMA
-- =====================================================
-- This schema supports a complete Uber/Uber Eats-like booking system
-- with customer details, service information, location tracking,
-- and full booking lifecycle management.

-- Users & Profiles (Enhanced)
create table if not exists profiles (
  id uuid references auth.users on delete cascade primary key,
  name text,
  role text check (role in ('customer','tasker')) default 'customer',
  skills text[],
  hourly_rate numeric,
  bio text,
  rating numeric default 0,
  created_at timestamp default now(),
  -- Additional Uber-like fields
  phone text,
  address text,
  city text,
  state text,
  zip_code text,
  latitude numeric,
  longitude numeric,
  is_available boolean default true,
  last_active timestamp default now()
);

-- Tasks (Service Requests)
create table if not exists tasks (
  id bigserial primary key,
  customer_id uuid references profiles(id),
  title text not null,
  description text,
  status text check (status in ('open','in-progress','completed')) default 'open',
  created_at timestamp default now(),
  -- Additional service details
  category text,
  estimated_duration integer, -- in minutes
  estimated_price numeric,
  priority text check (priority in ('low','normal','high','urgent')) default 'normal'
);

-- Bookings (Uber-like booking system)
create table if not exists bookings (
  id bigserial primary key,
  task_id bigint references tasks(id),
  customer_id uuid references profiles(id),
  tasker_id uuid references profiles(id),
  
  -- Core booking status (Uber-like lifecycle)
  status text check (status in ('pending','accepted','in-progress','completed','cancelled','declined')) default 'pending',
  created_at timestamp default now(),
  
  -- Customer details (like Uber Eats order details)
  customer_name text,
  customer_phone text,
  customer_address text,
  customer_email text,
  
  -- Service details (like Uber Eats restaurant/food details)
  service_name text,
  service_description text,
  service_category text,
  
  -- Provider details (like Uber driver details)
  provider_name text,
  provider_phone text,
  
  -- Booking details (like Uber trip details)
  booking_date date,
  booking_time time,
  estimated_duration integer, -- in minutes
  estimated_price numeric,
  final_price numeric,
  
  -- Location details (like Uber pickup/dropoff)
  pickup_address text,
  dropoff_address text,
  latitude numeric,
  longitude numeric,
  
  -- Status tracking (like Uber trip status with timestamps)
  status_updated_at timestamp default now(),
  accepted_at timestamp,
  started_at timestamp,
  completed_at timestamp,
  cancelled_at timestamp,
  
  -- Additional Uber-like features
  special_instructions text,
  priority text check (priority in ('low','normal','high','urgent')) default 'normal',
  payment_status text check (payment_status in ('pending','paid','refunded')) default 'pending',
  payment_method text
);

-- Reviews (Enhanced)
create table if not exists reviews (
  id bigserial primary key,
  booking_id bigint references bookings(id),
  customer_id uuid references profiles(id),
  tasker_id uuid references profiles(id),
  rating int not null check (rating >= 1 and rating <= 5),
  review_text text,
  created_at timestamp default now(),
  -- Additional review details
  service_rating int check (service_rating >= 1 and service_rating <= 5),
  communication_rating int check (communication_rating >= 1 and communication_rating <= 5),
  timeliness_rating int check (timeliness_rating >= 1 and timeliness_rating <= 5)
);

-- =====================================================
-- PERFORMANCE INDEXES
-- =====================================================
-- These indexes optimize query performance for the Uber-like system

-- Bookings table indexes
CREATE INDEX IF NOT EXISTS idx_bookings_customer_id ON bookings(customer_id);
CREATE INDEX IF NOT EXISTS idx_bookings_tasker_id ON bookings(tasker_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
CREATE INDEX IF NOT EXISTS idx_bookings_created_at ON bookings(created_at);
CREATE INDEX IF NOT EXISTS idx_bookings_booking_date ON bookings(booking_date);
CREATE INDEX IF NOT EXISTS idx_bookings_payment_status ON bookings(payment_status);
CREATE INDEX IF NOT EXISTS idx_bookings_priority ON bookings(priority);

-- Profiles table indexes
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);
CREATE INDEX IF NOT EXISTS idx_profiles_is_available ON profiles(is_available);
CREATE INDEX IF NOT EXISTS idx_profiles_city ON profiles(city);
CREATE INDEX IF NOT EXISTS idx_profiles_rating ON profiles(rating);

-- Tasks table indexes
CREATE INDEX IF NOT EXISTS idx_tasks_customer_id ON tasks(customer_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

-- Reviews table indexes
CREATE INDEX IF NOT EXISTS idx_reviews_booking_id ON reviews(booking_id);
CREATE INDEX IF NOT EXISTS idx_reviews_customer_id ON reviews(customer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_tasker_id ON reviews(tasker_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);

-- =====================================================
-- SAMPLE DATA FOR TESTING
-- =====================================================
-- This section provides sample data to test the Uber-like system

-- Sample profiles (customers and taskers)
INSERT INTO profiles (id, name, role, phone, city, state, is_available, rating) VALUES
  ('11111111-1111-1111-1111-111111111111', 'John Customer', 'customer', '+1-555-0101', 'New York', 'NY', true, 4.5),
  ('22222222-2222-2222-2222-222222222222', 'Jane Customer', 'customer', '+1-555-0102', 'Los Angeles', 'CA', true, 4.8),
  ('33333333-3333-3333-3333-333333333333', 'Mike Tasker', 'tasker', '+1-555-0201', 'New York', 'NY', true, 4.9),
  ('44444444-4444-4444-4444-444444444444', 'Sarah Tasker', 'tasker', '+1-555-0202', 'Los Angeles', 'CA', true, 4.7);

-- Sample tasks
INSERT INTO tasks (customer_id, title, description, category, estimated_duration, estimated_price, priority) VALUES
  ('11111111-1111-1111-1111-111111111111', 'Home Cleaning', 'Deep clean 3-bedroom apartment', 'cleaning', 120, 150.00, 'normal'),
  ('22222222-2222-2222-2222-222222222222', 'Car Wash', 'Full exterior and interior car wash', 'carcare', 60, 75.00, 'normal'),
  ('11111111-1111-1111-1111-111111111111', 'Haircut', 'Professional haircut and styling', 'beauty', 45, 60.00, 'normal');

-- Sample bookings (Uber-like format)
INSERT INTO bookings (
  task_id, customer_id, tasker_id, status,
  customer_name, customer_phone, customer_address, customer_email,
  service_name, service_category, service_description,
  provider_name, provider_phone,
  booking_date, booking_time, estimated_duration, estimated_price,
  pickup_address, dropoff_address,
  special_instructions, priority, payment_status, payment_method
) VALUES
  (1, '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 'pending',
   'John Customer', '+1-555-0101', '123 Main St, New York, NY 10001', 'john@email.com',
   'Home Cleaning', 'cleaning', 'Deep clean 3-bedroom apartment',
   'Mike Tasker', '+1-555-0201',
   '2024-01-15', '10:00:00', 120, 150.00,
   '123 Main St, New York, NY 10001', '123 Main St, New York, NY 10001',
   'Please use eco-friendly products', 'normal', 'pending', 'credit_card'),
   
  (2, '22222222-2222-2222-2222-222222222222', '44444444-4444-4444-4444-444444444444', 'accepted',
   'Jane Customer', '+1-555-0102', '456 Oak Ave, Los Angeles, CA 90210', 'jane@email.com',
   'Car Wash', 'carcare', 'Full exterior and interior car wash',
   'Sarah Tasker', '+1-555-0202',
   '2024-01-16', '14:30:00', 60, 75.00,
   '456 Oak Ave, Los Angeles, CA 90210', '456 Oak Ave, Los Angeles, CA 90210',
   'Car is a black Tesla Model 3', 'normal', 'paid', 'credit_card');

-- =====================================================
-- USEFUL QUERIES FOR UBER-LIKE SYSTEM
-- =====================================================

-- Get all pending bookings for taskers (like Uber driver app)
-- SELECT * FROM bookings WHERE status = 'pending' ORDER BY created_at DESC;

-- Get customer's booking history (like Uber customer app)
-- SELECT * FROM bookings WHERE customer_id = 'customer-uuid' ORDER BY created_at DESC;

-- Get tasker's assigned bookings (like Uber driver dashboard)
-- SELECT * FROM bookings WHERE tasker_id = 'tasker-uuid' ORDER BY booking_date, booking_time;

-- Get nearby available taskers (like Uber matching)
-- SELECT * FROM profiles WHERE role = 'tasker' AND is_available = true AND city = 'New York';

-- Get booking statistics
-- SELECT status, COUNT(*) FROM bookings GROUP BY status;

-- Get average ratings by tasker
-- SELECT tasker_id, AVG(rating) FROM reviews GROUP BY tasker_id;
