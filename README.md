# Sky: Children of the Light — Toolkit (Modding Utility)

[RU] 
Профессиональная модульная утилита для реверс-инжиниринга, извлечения ассетов, модификации и патчинга игры *Sky: Children of the Light*. Инструмент разработан на базе PyQt6, обладает высокойжностью, полностью автономной архитектурой (один `.exe` файл) и продвинутым функционалом для работы с внутренними форматами игры.

[EN]
A high-performance, modular asset editor, extraction utility, and reverse-engineering toolkit for *Sky: Children of the Light*. Built on PyQt6, features a modern dark UI, zero external dependencies, and dedicated tools for handling proprietary game formats.

---

## 🛠 Функционал / Features

### 🇷🇺 Русский:
* **Textures (KTX) Manager (Двусторонняя конвертация):** Полная поддержка игровых KTX-текстур с «приколами» шифрования, которые не открываются обычным софтом. Позволяет как декодировать исходные текстуры в стандартные форматы для редактирования, так и кодировать их обратно. Игра без проблем принимает измененные файлы.
* **Localization Editor (Умный редактор строк):** Специализированный текстовый редактор для работы с файлами локализации. Включает в себя нумерацию строк, подсветку синтаксиса, а также полный набор необходимых инструментов разработчика: быстрый поиск, копирование/вставка, историю изменений (откат назад/вперед) и быстрое сохранение.
* **Auto-Patcher (Менеджер связок):** Инструмент автоматизации патчинга. Вы указываете исходный файл и файл для замены (создавая связку), а программа запоминает эти конфигурации. Для применения всех модификаций и инъекции файлов в игру достаточно нажать всего одну кнопку — «ПАТЧИТЬ».

### 🇬🇧 English:
* **Textures (KTX) Manager (Two-Way Conversion):** Full support for the game's proprietary KTX texture files that standard software fails to process. Features dual-mode execution: decodes raw textures into editable formats and encodes them back into compliant game assets. Fully compatible with the game client.
* **Localization Editor (Smart Line Editor):** A dedicated text editor designed specifically for editing game localization strings. Equipped with line numbering, syntax highlighting, and an essential toolset: rapid search, copy/paste, robust undo/redo history, and instant saving.
* **Auto-Patcher (Asset Injection Manager):** Advanced automation tool for managing file replacements. Users define a "source-to-target" pair, which the program saves locally. All modifications and file injections into the game directory are executed with a single click of the "PATCH" button.

---

## 🚀 Как запустить / How to Run

### [RU] Для пользователей:
Перейдите в раздел **Releases** на странице репозитория, скачайте актуальный скомпилированный файл `Sky_MOD_kit.exe` и запустите его. Программа полностью автономна и не требует настройки окружения.

### [EN] For Users:
Navigate to the **Releases** section, download the standalone `Sky_MOD_kit.exe` binary, and run it. The application is completely portable and requires no environmental setup.

---

## 💻 Сборка из исходников / Build from Source

```bash
# Установка необходимых библиотек / Install dependencies
pip install PyQt6 pyinstaller

# Сборка проекта в один полностью независимый EXE / Build standalone single-file EXE
pyinstaller --noconfirm --onefile --windowed --add-data "tabs;tabs" --add-data "style.py;." --add-data "editor_widgets.py;." --icon=icon.ico main.py
```

---

## 📜 Лицензия / License
Этот проект распространяется под свободной лицензией **MIT License**. Вы можете модифицировать, распространять и использовать этот код в любых целях.
Distributed under the **MIT License**. See `LICENSE` for more information.
## 🗺 Дорожная карта / Roadmap (In Development)

### 🇷🇺 Что планируется добавить в ближайших обновлениях:
* **Локализация интерфейса:** Добавление полноценной смены языка (RU/EN) прямо внутри настроек лаунчера.
* **Интерактивные гайды:** Подробное руководство по использованию всех инструментов (KTX, локализация, патчер) на русском и английском языках прямо внутри программы.
* **Поддержка мобильных платформ:** Расширение менеджера текстур для работы с мобильными архивами текстур (Android/iOS кэш игры).
* **Audio (.bank) Player:** (В разработке) Встроенный аудио-плеер для скрытного декодирования и прослушивания игровых аудио-банков FMOD Studio во временной папке.

### 🇬🇧 Planned Features & Future Updates:
* **In-App Localization:** Native UI language switching (RU/EN) accessible directly within the toolkit settings.
* **Comprehensive Guides:** Step-by-step usage manuals for all features (KTX, Localization, Patcher) provided in both languages inside the app.
* **Mobile Asset Support:** Expanding the texture tool to support mobile archive extraction and packing (Android/iOS game cache).
* **Audio (.bank) Player:** (In Progress) Built-in audio player capable of background decoding and listening to FMOD Studio audio banks using temporary directories.

