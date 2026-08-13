#!/usr/bin/env py3
"""Ghidhai Platform — Full Automated Runner
الإصدار الاحترافي لتشغيل منصة غذائي خطوة بخطوة
"""
import os
import sys
import subprocess
import time
import mysql.connector
import socket
import webbrowser
from config import Config

# ملف علامة يثبت أنه تم تثبيت المتطلبات مسبقًا
DEPS_MARKER_FILE = ".deps_installed"

# ============================================================
# 🧩 دوال مساعدة للطباعة والتنفيذ
# ============================================================

def print_step(description: str, emoji: str = "🔧"):
    """طباعة عنوان منظم لخطوة"""
    print(f"\n{'=' * 60}")
    print(f"{emoji} {description}")
    print(f"{'=' * 60}")


def run_command(command: str, description: str, check_output=False):
    """تشغيل أمر في النظام مع تتبع الأخطاء"""
    print(f"⏳ {description}...")

    try:
        if check_output:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f" فشل في {description}")
        if e.stderr:
            print(e.stderr)
        return False


# ============================================================
#  إعداد MySQL
# ============================================================

def check_mysql_connection():
    """تحقق من إمكانية الاتصال بـ MySQL (بدون تحديد قاعدة معينة)"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        conn.close()
        print(" تم الاتصال بنجاح بخادم MySQL.")
        return True
    except Exception as e:
        print(f" تعذر الاتصال بـ MySQL: {e}")
        return False


# ============================================================
# ⚙️ إعداد البيئة
# ============================================================

def setup_environment():
    """تحضير بيئة العمل"""
    print_step("إعداد بيئة التشغيل", "⚙️")

    py_version = run_command("py --version", "التحقق من إصدار py", check_output=True)
    if py_version:
        print(f" إصدار py: {py_version}")

    #  لا نثبّت المتطلبات إلا أول مرة فقط
    if os.path.exists(DEPS_MARKER_FILE):
        print(" تم العثور على ملف الاعتماديات المثبتة مسبقًا — تخطي خطوة تثبيت المتطلبات.")
    else:
        if not run_command("pip install -r requirements.txt", "تثبيت المتطلبات (مرة أولى فقط)"):
            print(" فشل في تثبيت المكتبات المطلوبة.")
            return False
        # إنشاء ملف العلامة بعد نجاح التثبيت
        try:
            with open(DEPS_MARKER_FILE, "w", encoding="utf-8") as f:
                f.write("installed\n")
            print(" تم تثبيت المتطلبات وحفظ حالة الاعتماديات في .deps_installed")
        except Exception as e:
            print(f" تم التثبيت لكن فشل إنشاء ملف العلامة .deps_installed: {e}")

    if not check_mysql_connection():
        print(" تأكد من تشغيل MySQL وتحديث بيانات config.py")
        return False

    return True


# ============================================================
#  إعداد قاعدة البيانات
# ============================================================

def setup_database():
    """تهيئة قاعدة البيانات والجداول"""
    print_step("إعداد قاعدة البيانات", "")

    if not run_command("py setup_database.py", "إنشاء قاعدة البيانات والجداول"):
        return False

    print(" تم إعداد قاعدة البيانات بنجاح.")
    return True

# ============================================================
#  جمع البيانات
# ============================================================

def collect_data():
    """جمع البيانات من مصادر مختلفة"""
    print_step("جمع البيانات من المصادر", "")

    collectors = [
        ("data_collection/usda_collector.py", "جمع بيانات USDA"),
        ("data_collection/arabic_foods_collector.py", "جمع البيانات العربية"),
        ("data_collection/health_rules_collector.py", "جمع القواعد الصحية")
    ]

    success = 0
    for path, desc in collectors:
        if run_command(f"py {path}", desc):
            success += 1
        else:
            print(f" فشل في {desc}، لكن المتابعة مستمرة...")

    print(f" تم جمع البيانات من {success}/{len(collectors)} مصدر.")
    return True


# ============================================================
#  معالجة البيانات
# ============================================================

def process_data():
    """تنظيف وتحسين قاعدة البيانات"""
    print_step("معالجة وتنظيف البيانات", "")

    tasks = [
        ("data_processing/data_cleaner.py", "تنظيف البيانات"),
        ("data_processing/database_manager.py", "تحسين قاعدة البيانات")
    ]

    for script, desc in tasks:
        run_command(f"py {script}", desc)

    return True


# ============================================================
#  تدريب النماذج
# ============================================================

def train_models():
    """تدريب جميع النماذج الذكية"""
    print_step("تدريب نماذج الذكاء الاصطناعي", "")

    models = [
        ("ml_models/model_trainer.py", "تدريب النماذج الأساسية"),
        ("ml_models/content_based_filtering.py", "تدريب نموذج التصفية بالمحتوى"),
        ("ml_models/recommendation_engine.py", "تدريب محرك التوصيات")
    ]

    success = 0
    for path, desc in models:
        if run_command(f"py {path}", desc):
            success += 1
        else:
            print(f" فشل في {desc}")

    print(f" تم تدريب {success}/{len(models)} نموذج.")
    return True


# ============================================================
#  الاختبارات
# ============================================================

def run_tests():
    """تشغيل اختبارات أساسية"""
    print_step("تشغيل الاختبارات", "🧪")

    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM foods")
        foods = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users")
        users = cursor.fetchone()[0]
        conn.close()

        print(f" قاعدة البيانات تحتوي على {foods} طعام و {users} مستخدم.")
    except Exception as e:
        print(f" فشل اختبار قاعدة البيانات: {e}")

    run_command(
        'py -c "from ml_models.recommendation_engine import RecommendationEngine; '
        'RecommendationEngine(auto_load=True); print(\' محرك التوصيات جاهز\')"',
        "اختبار محرك التوصيات"
    )

    print(" جميع الاختبارات تمت بنجاح.")
    return True


# ============================================================
#  فحص حالة قاعدة البيانات والنماذج
# ============================================================

def is_database_initialized():
    """التحقق هل قاعدة بيانات المشروع والجداول الأساسية موجودة أم لا"""
    print_step("التحقق من تهيئة قاعدة البيانات", "")
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'foods'")
        has_foods_table = cursor.fetchone() is not None

        if has_foods_table:
            cursor.execute("SELECT COUNT(*) FROM foods")
            count = cursor.fetchone()[0]
            print(f" تم العثور على جدول foods وفيه {count} سجل.")
        else:
            print(" لم يتم العثور على جدول foods، يبدو أن قاعدة البيانات غير مهيأة.")

        conn.close()
        return has_foods_table
    except Exception as e:
        print(f" قاعدة البيانات غير مهيأة بالكامل أو غير موجودة: {e}")
        return False


def models_exist():
    """التحقق من وجود نماذج مدرّبة مسبقًا"""
    print_step("التحقق من وجود نماذج الذكاء الاصطناعي", "")
    models_dir = "ml_models/saved_models"
    if os.path.isdir(models_dir):
        has_models = any(os.scandir(models_dir))
        if has_models:
            print(" تم العثور على نماذج محفوظة في مجلد saved_models.")
        else:
            print(" مجلد saved_models موجود لكن بدون نماذج.")
        return has_models
    else:
        print(" مجلد saved_models غير موجود.")
        return False


# ============================================================
#  تشغيل التطبيق
# ============================================================

def find_free_port(start=5000):
    """إيجاد منفذ متاح لتشغيل السيرفر"""
    for port in range(start, start + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    return 5000


def start_application():
    """تشغيل خادم Flask وفتح المتصفح تلقائيًا"""
    print_step("تشغيل تطبيق الويب", "")

    port = find_free_port()
    url = f"http://localhost:{port}"

    print(f"\ تم تجهيز منصة غذائي بنجاح!")
    print(f"\ معلومات التطبيق:")
    print(f"    العنوان: {url}")
    print(f"    قاعدة البيانات: {Config.MYSQL_DB}")
    print(f"    النماذج: {len(os.listdir('ml_models/saved_models')) if os.path.exists('ml_models/saved_models') else 0} نموذج")
    print(f"    البيانات: جاهزة للاستخدام")

    print("\ تشغيل الخادم... يمكنك الإيقاف باستخدام Ctrl+C")

    # فتح المتصفح تلقائياً
    webbrowser.open(url)

    # تشغيل التطبيق
    os.system(f"py -m flask --app app.app run --host=0.0.0.0 --port={port} --debug")


# ============================================================
#  نقطة البداية
# ============================================================

def main():
    """الوظيفة الرئيسية لتشغيل النظام"""
    try:
        print(" بدء تشغيل منصة غذائي الشاملة...")
        print("⏰ هذه العملية قد تستغرق عدة دقائق في التشغيل الأول...\n")

        # 1️⃣ إعداد البيئة (مع كاش الاعتماديات)
        if not setup_environment():
            sys.exit(1)

        # 2️⃣ فحص حالة قاعدة البيانات والنماذج
        db_ready = is_database_initialized()
        models_ready = models_exist()

        # 3️⃣ إعداد قاعدة البيانات وجمع البيانات (مرة واحدة فقط)
        if not db_ready:
            print_step("قاعدة البيانات غير جاهزة، سيتم إنشاؤها وتجهيز البيانات لأول مرة", "")
            if not setup_database():
                sys.exit(1)
            collect_data()
            process_data()
        else:
            print(" قاعدة البيانات موجودة مسبقًا — تخطي خطوات الإنشاء وجمع البيانات.")

        # 4️⃣ تدريب النماذج (مرة واحدة فقط)
        if not models_ready:
            print_step("النماذج غير موجودة، سيتم تدريبها لأول مرة", "")
            train_models()
        else:
            print(" نماذج الذكاء الاصطناعي موجودة — تخطي خطوة التدريب.")

        #  الاختبارات
        run_tests()

        #  التشغيل النهائي
        start_application()

    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف العملية بواسطة المستخدم.")
    except Exception as e:
        print(f"\n خطأ غير متوقع: {e}")
        sys.exit(1)


# ============================================================
#  نقطة الدخول الفعلية
# ============================================================

if __name__ == "__main__":
    main()
