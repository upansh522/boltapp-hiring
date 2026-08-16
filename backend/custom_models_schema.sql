-- Custom Model Schema for boltapp-hiring
-- Generated: 2026-08-16
-- Contains only custom Django models (not Django auth tables)

-- ============================================================
-- users_user table
-- Custom User model with email as unique identifier
-- ============================================================

CREATE TABLE "users_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password" varchar(128) NOT NULL,
    "last_login" datetime(6) NULL,
    "is_superuser" bool NOT NULL,
    "username" varchar(150) NOT NULL UNIQUE,
    "first_name" varchar(150) NOT NULL,
    "last_name" varchar(150) NOT NULL,
    "email" varchar(254) NOT NULL UNIQUE,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "date_joined" datetime(6) NOT NULL,
    "login_code" varchar(120) NULL,
    "created_at" datetime(6) NOT NULL,
    "updated_at" datetime(6) NOT NULL,
    CONSTRAINT "users_user_email_uniq" UNIQUE ("email")
);

-- Comment: Custom User model - email is the unique identifier
-- USERNAME_FIELD = 'email', REQUIRED_FIELDS = ['first_name', 'last_name']

-- ============================================================
-- checkout_checkout table
-- Checkout model for authenticated and guest checkouts
-- ============================================================

CREATE TABLE "checkout_checkout" (
    "id" uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    "user" integer NULL REFERENCES "users_user" ("id") ON DELETE CASCADE,
    "email" varchar(254) NOT NULL,
    "phone" varchar(20) NOT NULL,
    "shipping_address" text NOT NULL,
    "idempotency_key" uuid NULL UNIQUE,
    "created_at" datetime(6) NOT NULL,
    CONSTRAINT "checkout_checkout_idempotency_key_uniq" UNIQUE ("idempotency_key")
);

-- Comment: Checkout model fields:
-- - user: ForeignKey to users_user (nullable, cascade delete)
-- - email: Customer email address
-- - phone: Customer phone number
-- - shipping_address: Full shipping address text
-- - idempotency_key: Unique UUID for request deduplication
-- - created_at: Timestamp of checkout creation

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX "checkout_checkout_user_idx" ON "checkout_checkout" ("user");
CREATE INDEX "checkout_checkout_email_idx" ON "checkout_checkout" ("email");
CREATE INDEX "checkout_checkout_created_at_idx" ON "checkout_checkout" ("created_at");

-- ============================================================
-- Schema Summary
-- ============================================================

-- Tables created:
-- 1. users_user  - Custom User model (extends AbstractUser, email=USERNAME_FIELD)
-- 2. checkout_checkout - Checkout system with user FK, contact info, idempotency

-- Relationships:
--   checkout_checkout.user -> users_user.id (CASCADE on delete)

-- Authentication:
--   This schema supports Django's built-in auth system via the custom User model.
--   Uses email as the unique login identifier (USERNAME_FIELD = 'email').