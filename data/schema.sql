-- NexusHub Relational Database Schema with FTS5 Full-Text Search
CREATE TABLE IF NOT EXISTS repositories (
    id TEXT PRIMARY KEY,
    repo_name TEXT NOT NULL,
    title TEXT NOT NULL,
    function_title TEXT,
    title_en TEXT,
    function_title_en TEXT,
    description TEXT,
    description_en TEXT,
    main_category TEXT NOT NULL,
    sub_category TEXT,
    thumbnail_url TEXT,
    video_url TEXT,
    video_demo TEXT,
    has_video INTEGER DEFAULT 0,
    stars INTEGER DEFAULT 0,
    year INTEGER DEFAULT 2024,
    url TEXT NOT NULL,
    creator TEXT,
    tags TEXT, -- JSON array of tags
    is_pinned INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning fast category, vintage and sorting queries
CREATE INDEX IF NOT EXISTS idx_repo_main_cat ON repositories(main_category);
CREATE INDEX IF NOT EXISTS idx_repo_sub_cat ON repositories(sub_category);
CREATE INDEX IF NOT EXISTS idx_repo_stars ON repositories(stars);
CREATE INDEX IF NOT EXISTS idx_repo_year ON repositories(year);
CREATE INDEX IF NOT EXISTS idx_repo_has_video ON repositories(has_video);
CREATE INDEX IF NOT EXISTS idx_repo_pinned ON repositories(is_pinned);

-- SQLite FTS5 Virtual Table for Ultra-Fast Full-Text Multilingual Search
CREATE VIRTUAL TABLE IF NOT EXISTS repositories_fts USING fts5(
    id UNINDEXED,
    repo_name,
    title,
    function_title,
    title_en,
    description,
    description_en,
    tags,
    content='repositories',
    content_rowid='rowid'
);

-- Triggers to keep FTS index synchronized with the main table
CREATE TRIGGER IF NOT EXISTS trg_repo_ai AFTER INSERT ON repositories BEGIN
    INSERT INTO repositories_fts(rowid, id, repo_name, title, function_title, title_en, description, description_en, tags)
    VALUES (new.rowid, new.id, new.repo_name, new.title, new.function_title, new.title_en, new.description, new.description_en, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS trg_repo_ad AFTER DELETE ON repositories BEGIN
    INSERT INTO repositories_fts(repositories_fts, rowid, id, repo_name, title, function_title, title_en, description, description_en, tags)
    VALUES ('delete', old.rowid, old.id, old.repo_name, old.title, old.function_title, old.title_en, old.description, old.description_en, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS trg_repo_au AFTER UPDATE ON repositories BEGIN
    INSERT INTO repositories_fts(repositories_fts, rowid, id, repo_name, title, function_title, title_en, description, description_en, tags)
    VALUES ('delete', old.rowid, old.id, old.repo_name, old.title, old.function_title, old.title_en, old.description, old.description_en, old.tags);
    INSERT INTO repositories_fts(rowid, id, repo_name, title, function_title, title_en, description, description_en, tags)
    VALUES (new.rowid, new.id, new.repo_name, new.title, new.function_title, new.title_en, new.description, new.description_en, new.tags);
END;
