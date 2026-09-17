-- ==============================================================================
-- YouthFit AI PostgreSQL Schema Initialization Script
-- ==============================================================================

-- 1. Create policies table
CREATE TABLE IF NOT EXISTS policies (
    policy_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    category_large VARCHAR(100),
    category_mid VARCHAR(100),
    keyword TEXT,
    min_age INTEGER,
    max_age INTEGER,
    age_limit_yn VARCHAR(10),
    support_content TEXT,
    explanation TEXT,
    required_docs TEXT,
    apply_method TEXT,
    apply_url TEXT,
    apply_period TEXT,
    biz_start_date VARCHAR(50),
    biz_end_date VARCHAR(50),
    supervising_inst VARCHAR(255),
    operating_inst VARCHAR(255),
    zip_codes TEXT,
    raw_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create performance indexes
-- Age range index for lightning-fast eligibility filtering
CREATE INDEX IF NOT EXISTS idx_policies_age ON policies(min_age, max_age);

-- Category index for domain-specific filtering (주거, 일자리, 금융 등)
CREATE INDEX IF NOT EXISTS idx_policies_category ON policies(category_large, category_mid);

-- Policy name index for keyword search
CREATE INDEX IF NOT EXISTS idx_policies_name ON policies(name);

-- GIN index for high-performance JSONB querying into raw API response data
CREATE INDEX IF NOT EXISTS idx_policies_raw_json ON policies USING gin(raw_json);
