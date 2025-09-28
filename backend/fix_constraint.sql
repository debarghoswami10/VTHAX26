-- Fix booking status constraint to support Uber-like statuses
ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_status_check;
ALTER TABLE bookings ADD CONSTRAINT bookings_status_check CHECK (status IN ('pending','accepted','in-progress','completed','cancelled','declined'));
