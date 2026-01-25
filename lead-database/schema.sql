-- Lead Database Schema for Supabase
-- Optimized for free tier, handles 200k+ leads with flexible schema

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main leads table
CREATE TABLE leads (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Core fields (standardized across all sources)
    email TEXT UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    full_name TEXT,
    title TEXT,
    company_name TEXT,
    company_website TEXT,
    
    -- Contact information
    mobile_number TEXT,
    personal_email TEXT,
    linkedin_url TEXT,
    
    -- Professional details
    industry TEXT,
    headline TEXT,
    seniority TEXT,
    department TEXT,
    
    -- Location
    city TEXT,
    state TEXT,
    country TEXT,
    
    -- Company details
    company_linkedin TEXT,
    company_employees_count INTEGER,
    company_annual_revenue BIGINT,
    company_total_funding BIGINT,
    company_founded_year INTEGER,
    
    -- Flexible storage for all other fields
    -- This JSONB column stores ANY extra data from CSV files
    extra_data JSONB DEFAULT '{}'::jsonb,
    
    -- Metadata tracking
    source_file TEXT NOT NULL,
    source_type TEXT, -- 'apollo', 'zoominfo', 'crunchbase', etc.
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Validation status
    email_validation_status TEXT,
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Indexes for performance (critical for 200k+ records)
CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_company_name ON leads(company_name);
CREATE INDEX idx_leads_title ON leads(title);
CREATE INDEX idx_leads_industry ON leads(industry);
CREATE INDEX idx_leads_country ON leads(country);
CREATE INDEX idx_leads_source_file ON leads(source_file);
CREATE INDEX idx_leads_uploaded_at ON leads(uploaded_at DESC);

-- GIN index for JSONB extra_data (enables fast queries on flexible fields)
CREATE INDEX idx_leads_extra_data ON leads USING GIN(extra_data);

-- Full-text search index for company and name searches
CREATE INDEX idx_leads_company_search ON leads USING GIN(to_tsvector('english', COALESCE(company_name, '')));
CREATE INDEX idx_leads_name_search ON leads USING GIN(to_tsvector('english', COALESCE(full_name, '') || ' ' || COALESCE(first_name, '') || ' ' || COALESCE(last_name, '')));

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON leads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Upload statistics table (track import jobs)
CREATE TABLE upload_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_file TEXT NOT NULL,
    total_rows INTEGER NOT NULL,
    inserted INTEGER DEFAULT 0,
    updated INTEGER DEFAULT 0,
    skipped INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'in_progress', -- 'in_progress', 'completed', 'failed'
    error_log JSONB DEFAULT '[]'::jsonb
);

CREATE INDEX idx_upload_stats_started ON upload_stats(started_at DESC);
CREATE INDEX idx_upload_stats_source ON upload_stats(source_file);

-- View for quick stats
CREATE OR REPLACE VIEW lead_stats AS
SELECT 
    COUNT(*) as total_leads,
    COUNT(DISTINCT company_name) as total_companies,
    COUNT(DISTINCT country) as total_countries,
    COUNT(DISTINCT source_file) as total_sources,
    COUNT(*) FILTER (WHERE uploaded_at > NOW() - INTERVAL '7 days') as leads_last_7_days,
    COUNT(*) FILTER (WHERE uploaded_at > NOW() - INTERVAL '30 days') as leads_last_30_days
FROM leads;

-- View for source file breakdown
CREATE OR REPLACE VIEW leads_by_source AS
SELECT 
    source_file,
    source_type,
    COUNT(*) as lead_count,
    MIN(uploaded_at) as first_upload,
    MAX(uploaded_at) as last_upload
FROM leads
GROUP BY source_file, source_type
ORDER BY lead_count DESC;

COMMENT ON TABLE leads IS 'Main leads table with flexible schema for multi-source lead data';
COMMENT ON COLUMN leads.extra_data IS 'JSONB column storing all non-standard CSV columns. Query like: extra_data->>''Column Name''';
COMMENT ON COLUMN leads.email IS 'Unique identifier - primary deduplication key';
