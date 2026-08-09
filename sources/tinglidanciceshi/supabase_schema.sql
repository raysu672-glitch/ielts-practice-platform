-- 藕叶英语学习追踪系统数据库结构

-- 1. 教师配置表
CREATE TABLE IF NOT EXISTS teacher_config (
    id INTEGER PRIMARY KEY DEFAULT 1,
    access_password TEXT NOT NULL DEFAULT 'sjdh4405',
    school_name TEXT DEFAULT '藕叶英语',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认配置
INSERT INTO teacher_config (id, access_password, school_name) 
VALUES (1, 'sjdh4405', '藕叶英语')
ON CONFLICT (id) DO NOTHING;

-- 2. 学生表
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    default_password TEXT DEFAULT '123456',
    is_password_changed BOOLEAN DEFAULT FALSE,
    target_score NUMERIC(2,1) DEFAULT 6.5 CHECK (target_score IN (6, 6.5, 7)),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. 模块达标标准表
CREATE TABLE IF NOT EXISTS pass_standards (
    id SERIAL PRIMARY KEY,
    module_type TEXT UNIQUE NOT NULL,
    module_name TEXT NOT NULL,
    score_6 NUMERIC(5,2) DEFAULT 70,
    score_6_5 NUMERIC(5,2) DEFAULT 80,
    score_7 NUMERIC(5,2) DEFAULT 95,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认的听力1000词标准
INSERT INTO pass_standards (module_type, module_name, score_6, score_6_5, score_7) VALUES
('dictation', '听力1000词', 70, 80, 90)
ON CONFLICT (module_type) DO UPDATE SET
    module_name = EXCLUDED.module_name,
    score_6 = EXCLUDED.score_6,
    score_6_5 = EXCLUDED.score_6_5,
    score_7 = EXCLUDED.score_7,
    updated_at = CURRENT_TIMESTAMP;

-- 4. 测试记录表
CREATE TABLE IF NOT EXISTS test_records (
    id SERIAL PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students(student_id),
    test_type TEXT NOT NULL CHECK (test_type IN ('random', 'wrong_words')),
    score NUMERIC(5,2) NOT NULL,
    correct_count INTEGER NOT NULL,
    total_count INTEGER NOT NULL,
    is_passed BOOLEAN NOT NULL,
    pass_threshold NUMERIC(5,2) NOT NULL,
    details JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4.1 测试记录兼容扩展：支持所有模块分类、模块名称和测试用时
ALTER TABLE test_records ADD COLUMN IF NOT EXISTS module_type TEXT DEFAULT 'dictation';
ALTER TABLE test_records ADD COLUMN IF NOT EXISTS module_name TEXT DEFAULT '听力1000词';
ALTER TABLE test_records ADD COLUMN IF NOT EXISTS duration_seconds INTEGER DEFAULT 0;
ALTER TABLE test_records ADD COLUMN IF NOT EXISTS started_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE test_records ADD COLUMN IF NOT EXISTS ended_at TIMESTAMP WITH TIME ZONE;

-- 如果是新建项目，放宽 test_type 的模块扩展约束；已有旧约束请在 Supabase SQL 编辑器中执行本段。
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'test_records_test_type_check'
    ) THEN
        ALTER TABLE test_records DROP CONSTRAINT test_records_test_type_check;
    END IF;
END $$;

ALTER TABLE test_records
ADD CONSTRAINT test_records_test_type_check
CHECK (test_type IN ('random', 'wrong_words', 'module_test', 'history_wrong_words'));

-- 4.2 学习会话表：记录本次学习时长、模块时长、测试时长和每日汇总基础数据
CREATE TABLE IF NOT EXISTS study_sessions (
    id SERIAL PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students(student_id),
    module_type TEXT NOT NULL,
    module_name TEXT,
    session_kind TEXT DEFAULT 'study' CHECK (session_kind IN ('study', 'test')),
    words_tested INTEGER DEFAULT 0,
    initial_correct INTEGER DEFAULT 0,
    initial_wrong INTEGER DEFAULT 0,
    groups_completed INTEGER DEFAULT 0,
    score_percent NUMERIC(5,2),
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    details JSONB DEFAULT '[]',
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4.2.1 学习会话兼容扩展：旧库已存在 study_sessions 时补齐新字段
ALTER TABLE study_sessions ADD COLUMN IF NOT EXISTS module_name TEXT;
ALTER TABLE study_sessions ADD COLUMN IF NOT EXISTS session_kind TEXT DEFAULT 'study';
ALTER TABLE study_sessions ADD COLUMN IF NOT EXISTS score_percent NUMERIC(5,2);
ALTER TABLE study_sessions ADD COLUMN IF NOT EXISTS details JSONB DEFAULT '[]';
ALTER TABLE study_sessions ADD COLUMN IF NOT EXISTS started_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE study_sessions ADD COLUMN IF NOT EXISTS ended_at TIMESTAMP WITH TIME ZONE;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'study_sessions_session_kind_check'
    ) THEN
        ALTER TABLE study_sessions DROP CONSTRAINT study_sessions_session_kind_check;
    END IF;
END $$;

ALTER TABLE study_sessions
ADD CONSTRAINT study_sessions_session_kind_check
CHECK (session_kind IN ('study', 'test'));

-- 4.3 单词掌握表：听力单词学习流程使用
CREATE TABLE IF NOT EXISTS word_mastery (
    id SERIAL PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students(student_id),
    word TEXT NOT NULL,
    status TEXT DEFAULT 'learning' CHECK (status IN ('new', 'learning', 'mastered')),
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    last_result BOOLEAN,
    last_practiced_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, word)
);

-- 5. 错题本表
CREATE TABLE IF NOT EXISTS wrong_words (
    id SERIAL PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students(student_id),
    module_type TEXT NOT NULL DEFAULT 'dictation',
    word TEXT NOT NULL,
    wrong_count INTEGER DEFAULT 1,
    correct_streak INTEGER DEFAULT 0,
    last_tested TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_mastered BOOLEAN DEFAULT FALSE,
    UNIQUE(student_id, module_type, word)
);

-- 6. 创建索引
CREATE INDEX IF NOT EXISTS idx_test_records_student_id ON test_records(student_id);
CREATE INDEX IF NOT EXISTS idx_test_records_created_at ON test_records(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_test_records_module_type ON test_records(module_type);
CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);
CREATE INDEX IF NOT EXISTS idx_wrong_words_is_mastered ON wrong_words(is_mastered);
CREATE INDEX IF NOT EXISTS idx_study_sessions_student_id ON study_sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_study_sessions_module_type ON study_sessions(module_type);
CREATE INDEX IF NOT EXISTS idx_study_sessions_created_at ON study_sessions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_word_mastery_student_id ON word_mastery(student_id);

-- 7. 启用 Row Level Security (RLS)
ALTER TABLE teacher_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE pass_standards ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE wrong_words ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE word_mastery ENABLE ROW LEVEL SECURITY;

-- 8. RLS 策略（允许所有操作，因为前端会用 service_role key）
-- 注意：生产环境应该更严格
DROP POLICY IF EXISTS "Allow all operations on teacher_config" ON teacher_config;
DROP POLICY IF EXISTS "Allow all operations on students" ON students;
DROP POLICY IF EXISTS "Allow all operations on pass_standards" ON pass_standards;
DROP POLICY IF EXISTS "Allow all operations on test_records" ON test_records;
DROP POLICY IF EXISTS "Allow all operations on wrong_words" ON wrong_words;
DROP POLICY IF EXISTS "Allow all operations on study_sessions" ON study_sessions;
DROP POLICY IF EXISTS "Allow all operations on word_mastery" ON word_mastery;

CREATE POLICY "Allow all operations on teacher_config" ON teacher_config FOR ALL USING (true);
CREATE POLICY "Allow all operations on students" ON students FOR ALL USING (true);
CREATE POLICY "Allow all operations on pass_standards" ON pass_standards FOR ALL USING (true);
CREATE POLICY "Allow all operations on test_records" ON test_records FOR ALL USING (true);
CREATE POLICY "Allow all operations on wrong_words" ON wrong_words FOR ALL USING (true);
CREATE POLICY "Allow all operations on study_sessions" ON study_sessions FOR ALL USING (true);
CREATE POLICY "Allow all operations on word_mastery" ON word_mastery FOR ALL USING (true);

-- 9. 全模块默认达标线
INSERT INTO pass_standards (module_type, module_name, score_6, score_6_5, score_7) VALUES
('listening_basic', '听力基础词汇', 70, 80, 90),
('reading_synonym', '阅读同义替换', 70, 80, 90),
('writing_phrase', '写作词伙', 50, 70, 90),
('sentence', '长难句分析', 60, 80, 80),
('listening_synonym', '听力同义替换', 70, 80, 90),
('writing_translate', '写作句子翻译', 50, 70, 90),
('listening_p4_speed', '听力P4跟读倍速', 70, 80, 90),
('dictation_learn', '听力单词学习', 70, 80, 90)
ON CONFLICT (module_type) DO UPDATE SET
    module_name = EXCLUDED.module_name,
    score_6 = EXCLUDED.score_6,
    score_6_5 = EXCLUDED.score_6_5,
    score_7 = EXCLUDED.score_7,
    updated_at = CURRENT_TIMESTAMP;

-- 10. 每天每个模块学习时长
CREATE OR REPLACE VIEW daily_module_study_time AS
SELECT
    student_id,
    DATE(created_at AT TIME ZONE 'Asia/Shanghai') AS study_date,
    module_type,
    COALESCE(module_name, module_type) AS module_name,
    SUM(duration_seconds) AS duration_seconds,
    COUNT(*) AS session_count
FROM study_sessions
GROUP BY student_id, DATE(created_at AT TIME ZONE 'Asia/Shanghai'), module_type, COALESCE(module_name, module_type);

-- 11. 每天总学习时长
CREATE OR REPLACE VIEW daily_total_study_time AS
SELECT
    student_id,
    DATE(created_at AT TIME ZONE 'Asia/Shanghai') AS study_date,
    SUM(duration_seconds) AS duration_seconds,
    COUNT(*) AS session_count
FROM study_sessions
GROUP BY student_id, DATE(created_at AT TIME ZONE 'Asia/Shanghai');

-- 12. 每个学生每个模块测试汇总
CREATE OR REPLACE VIEW student_module_test_summary AS
SELECT
    student_id,
    module_type,
    COALESCE(module_name, module_type) AS module_name,
    COUNT(*) AS test_count,
    MAX(score) AS best_score,
    AVG(score) AS avg_score,
    SUM(CASE WHEN is_passed THEN 1 ELSE 0 END) AS passed_count,
    MAX(created_at) AS last_test_at
FROM test_records
GROUP BY student_id, module_type, COALESCE(module_name, module_type);
