import mysql.connector
from config import Config
import os
import hashlib

def create_database():
    """إنشاء قاعدة البيانات والجداول"""
    try:
        print("⚙️ بدء إنشاء قاعدة البيانات...")

        # الاتصال بدون تحديد قاعدة بيانات
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()

        # إنشاء قاعدة البيانات إذا لم تكن موجودة
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        cursor.execute(f"USE {Config.MYSQL_DB}")

        # قراءة ملف schema.sql من المسار الصحيح
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f" لم يتم العثور على الملف: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as file:
            schema_sql = file.read()

        # تنفيذ أوامر SQL
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for statement in statements:
            cursor.execute(statement)

        conn.commit()
        print(" تم إنشاء قاعدة البيانات والجداول بنجاح!")

    except Exception as e:
        print(f" خطأ في إنشاء قاعدة البيانات: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def initialize_health_data():
    """تهيئة البيانات الصحية الأساسية"""
    try:
        print("🩺 تهيئة البيانات الصحية...")
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()

        # الأمراض المزمنة
        chronic_diseases = [
            ('Diabetes', 'مرض السكري', 'تجنب السكريات المضافة والتركيز على الألياف'),
            ('Hypertension', 'ارتفاع ضغط الدم', 'تقليل الصوديوم وزيادة البوتاسيوم'),
            ('Heart Disease', 'أمراض القلب', 'تقليل الدهون المشبعة وزيادة الأوميغا-3'),
            ('Celiac Disease', 'حساسية القمح', 'تجنب الجلوتين تماماً'),
            ('Lactose Intolerance', 'عدم تحمل اللاكتوز', 'تجنب منتجات الألبان'),
            ('Obesity', 'السمنة', 'مراقبة السعرات وزيادة النشاط البدني')
        ]
        cursor.executemany("""
            INSERT IGNORE INTO chronic_diseases (name_en, name_ar, dietary_guidelines)
            VALUES (%s, %s, %s)
        """, chronic_diseases)

        # الحساسيات
        allergies = [
            ('Gluten', 'جلوتين', 'القمح، الشعير، الشوفان'),
            ('Lactose', 'لاكتوز', 'الحليب، الجبن، الزبادي'),
            ('Nuts', 'مكسرات', 'اللوز، الجوز، الفول السوداني'),
            ('Seafood', 'مأكولات بحرية', 'الأسماك، المحار، الجمبري'),
            ('Eggs', 'بيض', 'البيض ومنتجاته'),
            ('Soy', 'صويا', 'فول الصويا والتوفو')
        ]
        cursor.executemany("""
            INSERT IGNORE INTO allergies (name_en, name_ar, common_sources)
            VALUES (%s, %s, %s)
        """, allergies)

        conn.commit()
        print(" تم تهيئة البيانات الصحية بنجاح!")

    except Exception as e:
        print(f" خطأ في تهيئة البيانات الصحية: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def create_admin_user():
    """إنشاء مستخدم إداري افتراضي"""
    try:
        print("👤 إنشاء المستخدم الإداري الافتراضي...")
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()

        # تحقق إن كان المدير موجود
        cursor.execute("SELECT id FROM users WHERE role='admin'")
        if cursor.fetchone():
            print(" المستخدم الإداري موجود مسبقًا، لن يتم إنشاؤه مرة أخرى.")
            return

        # إنشاء مدير جديد
        admin_username = "admin"
        admin_email = "admin@ghidhai.com"
        admin_password = "admin123"
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()

        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s, 'admin')
        """, (admin_username, admin_email, password_hash, "System", "Admin"))

        conn.commit()
        print(f" تم إنشاء المستخدم الإداري بنجاح!\ الدخول: {admin_email} | كلمة المرور: {admin_password}")

    except Exception as e:
        print(f" خطأ في إنشاء المستخدم الإداري: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print(" بدء إعداد قاعدة البيانات Ghidha’i...")
    create_database()
    initialize_health_data()
    create_admin_user()
    print(" الإعداد مكتمل بنجاح!")
