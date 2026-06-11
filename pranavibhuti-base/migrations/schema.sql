-- ═══════════════════════════════════════════════════════════════════
--  PRANAVIBHUTI — Complete Database Schema
--  Reference SQL (tables also auto-created by SQLAlchemy on startup)
--  Owner: Member 8 (Database lead)
-- ═══════════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS pranavibhuti;

-- ── Roles ENUM ────────────────────────────────────────────────────────────────
DO $$ BEGIN
  CREATE TYPE user_role AS ENUM ('patient', 'doctor', 'admin');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE appointment_status AS ENUM ('pending','confirmed','cancelled','completed','rescheduled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE order_status AS ENUM ('placed','confirmed','packed','shipped','delivered','cancelled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE lab_booking_status AS ENUM ('booked','sample_collected','processing','completed','cancelled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE notification_type AS ENUM ('sms','email','push');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE notification_status AS ENUM ('queued','sent','failed','stub_logged');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE document_type AS ENUM ('prescription','lab_report','vaccination','consultation_record','scan','other');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ── Users (Auth team — Member 4) ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,
    full_name        VARCHAR(150) NOT NULL,
    email            VARCHAR(255) UNIQUE NOT NULL,
    phone            VARCHAR(20) UNIQUE NOT NULL,
    hashed_password  VARCHAR(255) NOT NULL,
    role             user_role NOT NULL DEFAULT 'patient',
    is_active        BOOLEAN DEFAULT TRUE,
    is_verified      BOOLEAN DEFAULT FALSE,
    otp_code         VARCHAR(6),
    otp_expires_at   VARCHAR(50),
    created_at       TIMESTAMP DEFAULT NOW(),
    updated_at       TIMESTAMP DEFAULT NOW()
);

-- ── Doctors (Sreeja) ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doctors (
    id               SERIAL PRIMARY KEY,
    user_id          INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name             VARCHAR(150) NOT NULL,
    email            VARCHAR(255) UNIQUE NOT NULL,
    phone            VARCHAR(20) NOT NULL,
    specialization   VARCHAR(100) NOT NULL,
    qualification    VARCHAR(200) NOT NULL,
    hospital_name    VARCHAR(200),
    hospital_address TEXT,
    experience_years INTEGER DEFAULT 0,
    consultation_fee DECIMAL(10,2) DEFAULT 0,
    bio              TEXT,
    profile_picture  VARCHAR(500),
    rating           DECIMAL(3,2) DEFAULT 0.0,
    total_reviews    INTEGER DEFAULT 0,
    is_active        BOOLEAN DEFAULT TRUE,
    is_verified      BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMP DEFAULT NOW(),
    updated_at       TIMESTAMP DEFAULT NOW()
);

-- ── Doctor Slots (Sreeja) ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doctor_slots (
    id         SERIAL PRIMARY KEY,
    doctor_id  INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    slot_date  DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time   TIME NOT NULL,
    is_booked  BOOLEAN DEFAULT FALSE,
    is_blocked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (doctor_id, slot_date, start_time)
);

-- ── Appointments (Sreeja) ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS appointments (
    id            SERIAL PRIMARY KEY,
    patient_id    INTEGER NOT NULL REFERENCES users(id),
    doctor_id     INTEGER NOT NULL REFERENCES doctors(id),
    slot_id       INTEGER NOT NULL REFERENCES doctor_slots(id),
    status        appointment_status DEFAULT 'pending',
    reason        TEXT,
    notes         TEXT,
    booked_at     TIMESTAMP DEFAULT NOW(),
    cancelled_at  TIMESTAMP,
    cancel_reason VARCHAR(500),
    completed_at  TIMESTAMP
);

-- ── Medicines (Vaishnavi) ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS medicines (
    id                      SERIAL PRIMARY KEY,
    name                    VARCHAR(200) NOT NULL,
    generic_name            VARCHAR(200),
    brand                   VARCHAR(150),
    category                VARCHAR(100),
    description             TEXT,
    price                   DECIMAL(10,2) NOT NULL,
    stock_quantity          INTEGER DEFAULT 0,
    requires_prescription   BOOLEAN DEFAULT FALSE,
    image_url               VARCHAR(500),
    is_active               BOOLEAN DEFAULT TRUE,
    created_at              TIMESTAMP DEFAULT NOW(),
    updated_at              TIMESTAMP DEFAULT NOW()
);

-- ── Medicine Orders (Vaishnavi) ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS medicine_orders (
    id               SERIAL PRIMARY KEY,
    patient_id       INTEGER NOT NULL REFERENCES users(id),
    status           order_status DEFAULT 'placed',
    total_amount     DECIMAL(10,2) NOT NULL,
    delivery_address TEXT,
    prescription_url VARCHAR(500),
    payment_id       VARCHAR(200),
    created_at       TIMESTAMP DEFAULT NOW(),
    updated_at       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS medicine_order_items (
    id          SERIAL PRIMARY KEY,
    order_id    INTEGER NOT NULL REFERENCES medicine_orders(id) ON DELETE CASCADE,
    medicine_id INTEGER NOT NULL REFERENCES medicines(id),
    quantity    INTEGER NOT NULL,
    unit_price  DECIMAL(10,2) NOT NULL
);

-- ── Lab Tests (Vaishnavi) ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lab_tests (
    id                        SERIAL PRIMARY KEY,
    name                      VARCHAR(200) NOT NULL,
    category                  VARCHAR(100),
    description               TEXT,
    price                     DECIMAL(10,2) NOT NULL,
    turnaround_hours          INTEGER DEFAULT 24,
    home_collection_available BOOLEAN DEFAULT TRUE,
    is_active                 BOOLEAN DEFAULT TRUE,
    created_at                TIMESTAMP DEFAULT NOW(),
    updated_at                TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lab_bookings (
    id                 SERIAL PRIMARY KEY,
    patient_id         INTEGER NOT NULL REFERENCES users(id),
    test_id            INTEGER NOT NULL REFERENCES lab_tests(id),
    status             lab_booking_status DEFAULT 'booked',
    collection_date    DATE NOT NULL,
    home_collection    BOOLEAN DEFAULT FALSE,
    collection_address TEXT,
    amount             DECIMAL(10,2) NOT NULL,
    report_url         VARCHAR(500),
    payment_id         VARCHAR(200),
    created_at         TIMESTAMP DEFAULT NOW(),
    updated_at         TIMESTAMP DEFAULT NOW()
);

-- ── Notifications (Sreeja) ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notification_logs (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    type         notification_type NOT NULL,
    recipient    VARCHAR(255) NOT NULL,
    subject      VARCHAR(300),
    message      TEXT NOT NULL,
    status       notification_status DEFAULT 'stub_logged',
    error_detail TEXT,
    sent_at      TIMESTAMP,
    created_at   TIMESTAMP DEFAULT NOW()
);

-- ── Health Locker (Phase 3) ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS health_records (
    id            SERIAL PRIMARY KEY,
    patient_id    INTEGER NOT NULL REFERENCES users(id),
    document_type document_type NOT NULL,
    title         VARCHAR(300) NOT NULL,
    description   TEXT,
    file_url      VARCHAR(500) NOT NULL,
    file_name     VARCHAR(300),
    file_size_kb  INTEGER,
    is_shared     BOOLEAN DEFAULT FALSE,
    shared_with   INTEGER REFERENCES doctors(id),
    created_at    TIMESTAMP DEFAULT NOW(),
    updated_at    TIMESTAMP DEFAULT NOW()
);

-- ── Indexes (performance) ─────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_appointments_patient   ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor    ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_slots_doctor_date      ON doctor_slots(doctor_id, slot_date);
CREATE INDEX IF NOT EXISTS idx_medicine_orders_patient ON medicine_orders(patient_id);
CREATE INDEX IF NOT EXISTS idx_lab_bookings_patient   ON lab_bookings(patient_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user     ON notification_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_health_records_patient ON health_records(patient_id);
