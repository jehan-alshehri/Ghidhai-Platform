-- ============================================================
-- 🌐 قاعدة بيانات Ghidha’i Platform
-- الإصدار المحدث مع صلاحيات المستخدم (Admin / User)
-- ============================================================

-- جدول المستخدمين
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    gender ENUM('male', 'female'),
    blood_type ENUM(
        'A', 'B', 'O', 'AB',
        'A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'
    ),
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    activity_level ENUM('sedentary', 'light', 'moderate', 'active', 'very_active'),

    -- 🔹 نوع المستخدم: مدير أو مستخدم عادي
    role ENUM('admin', 'user') DEFAULT 'user',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================
-- جدول الأمراض المزمنة
CREATE TABLE IF NOT EXISTS chronic_diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_en VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    dietary_guidelines TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- جدول الحساسيات الغذائية
CREATE TABLE IF NOT EXISTS allergies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_en VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    common_sources TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- علاقة المستخدمين بالأمراض المزمنة
CREATE TABLE IF NOT EXISTS user_chronic_diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    disease_id INT NOT NULL,
    severity ENUM('mild', 'moderate', 'severe') DEFAULT 'moderate',
    diagnosis_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (disease_id) REFERENCES chronic_diseases(id) ON DELETE CASCADE,
    INDEX idx_user_disease (user_id, disease_id)
);

-- ============================================================
-- علاقة المستخدمين بالحساسيات
CREATE TABLE IF NOT EXISTS user_allergies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    allergy_id INT NOT NULL,
    reaction_severity ENUM('mild', 'moderate', 'severe') DEFAULT 'moderate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (allergy_id) REFERENCES allergies(id) ON DELETE CASCADE,
    INDEX idx_user_allergy (user_id, allergy_id)
);

-- ============================================================
-- جدول الأطعمة
CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_en VARCHAR(200) NOT NULL,
    name_ar VARCHAR(200),
    category VARCHAR(100),
    calories DECIMAL(8,2),
    protein DECIMAL(8,2),
    carbs DECIMAL(8,2),
    fat DECIMAL(8,2),
    fiber DECIMAL(8,2),
    sugar DECIMAL(8,2),
    sodium DECIMAL(8,2),
    calcium DECIMAL(8,2),
    iron DECIMAL(8,2),
    vitamin_c DECIMAL(8,2),
    gluten_free BOOLEAN DEFAULT FALSE,
    lactose_free BOOLEAN DEFAULT FALSE,
    suitable_for_diabetes BOOLEAN DEFAULT FALSE,
    suitable_for_hypertension BOOLEAN DEFAULT FALSE,
    suitable_blood_types JSON,
    health_benefits TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_calories (calories)
);

-- ============================================================
-- جدول تفضيلات المستخدم الغذائية
CREATE TABLE IF NOT EXISTS user_food_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    preferred_categories JSON,
    disliked_categories JSON,
    dietary_restrictions JSON,
    goals ENUM('weight_loss', 'weight_gain', 'maintenance', 'muscle_building', 'health_improvement'),
    target_calories INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================
-- جدول التوصيات
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack'),
    recommendation_score DECIMAL(5,4),
    reason TEXT,
    serving_size VARCHAR(100),
    estimated_calories DECIMAL(8,2),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_user_meal (user_id, meal_type),
    INDEX idx_score (recommendation_score)
);

-- ============================================================
-- جدول سجل الوجبات (التغذية اليومية)
CREATE TABLE IF NOT EXISTS nutrition_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack'),
    serving_size VARCHAR(100),
    consumed_calories DECIMAL(8,2),
    consumed_at DATE,
    rating ENUM('1', '2', '3', '4', '5'),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, consumed_at)
);

-- ============================================================
-- جدول جلسات محادثة المساعد الذكي
CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- جدول رسائل المحادثة
CREATE TABLE IF NOT EXISTS chat_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    message_type ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    INDEX idx_session (session_id)
);



