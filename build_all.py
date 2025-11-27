import os
import sys
import subprocess
import platform


def build_android():
    """Сборка для Android"""
    print("🔨 Сборка для Android...")
    try:
        subprocess.run(["buildozer", "android", "debug"], check=True)
        print("✅ APK собран успешно!")
    except Exception as e:
        print(f"❌ Ошибка сборки Android: {e}")


def build_windows():
    """Сборка для Windows"""
    print("🔨 Сборка для Windows...")
    try:
        subprocess.run([
            "pyinstaller", "--onefile", "--windowed",
            "--name", "CosmicClickerPro",
            "--icon", "assets/icon.ico",
            "cosmic_clicker_crossplatform.py"
        ], check=True)
        print("✅ Windows exe собран успешно!")
    except Exception as e:
        print(f"❌ Ошибка сборки Windows: {e}")


def build_web():
    """Подготовка веб-версии"""
    print("🔨 Подготовка веб-версии...")
    try:
        # Создаем HTML обертку
        with open("web_version/index.html", "w", encoding="utf-8") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Cosmic Clicker Pro - Web Version</title>
    <style>
        body { 
            margin: 0; padding: 0; 
            background: #0f0f23; 
            color: white; 
            font-family: Arial; 
        }
        #container { 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .game-frame {
            width: 100%;
            height: 800px;
            border: 2px solid #4cc9f0;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div id="container">
        <h1>💰 Cosmic Clicker Pro</h1>
        <p>Веб-версия игры (требуется Python в браузере)</p>
        <div id="game-content">
            <!-- Игра будет загружена здесь -->
        </div>
    </div>
</body>
</html>
            """)
        print("✅ Веб-версия подготовлена!")
    except Exception as e:
        print(f"❌ Ошибка подготовки веб-версии: {e}")


def main():
    """Главная функция сборки"""
    print("🚀 Запуск сборки Cosmic Clicker Pro для всех платформ!")

    # Создаем папки
    os.makedirs("build", exist_ok=True)
    os.makedirs("web_version", exist_ok=True)

    # Сборка в зависимости от платформы
    current_platform = platform.system()

    if current_platform == "Windows":
        build_windows()
    elif current_platform == "Linux":
        build_android()  # На Linux можно собрать Android
    elif current_platform == "Darwin":
        print("🍎 Для сборки iOS требуется MacOS с Xcode")

    # Веб-версия собирается на любой платформе
    build_web()

    print("🎉 Сборка завершена!")


if __name__ == "__main__":
    main()