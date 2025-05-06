# Приложение для обработки моделей

Приложение на Python предназначено для обработки конфигураций моделей, парсинга XML и JSON файлов и генерации структурированных выходных данных.

## Содержание
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Конфигурация](#конфигурация)
- [Расширение проекта](#расширение-проекта)
- [Структура проекта](#структура-проекта)
- [UML диаграмма](#uml-диаграмма-классов)

## Установка

1. **Клонирование репозитория**:
   ```bash
   git clone <repository-url>
   cd project
   ```

## Запуск проекта

1. **Запуск по умолчанию**:
   Точка входа — `main.py`. Для запуска приложения с настройками по умолчанию:
   ```bash
   python main.py
   ```

   Это выполнит:
   - Чтение модели из `input/impulse_test_input.xml`
   - Парсинг конфигурационных файлов из `input/config.json` и `input/patched_config.json`
   - Генерацию выходных файлов в директории `out/`:
     - `out/config.xml` (XML-конфигурация)
     - `out/meta.json` (JSON-метаданные)
     - `out/delta.json` (различия в конфигурациях)
     - `out/res_patched_config.json` (исправленная конфигурация)

2. **Пользовательская конфигурация**:
   Вы можете настроить приложение, изменив объект `AppConfiguration` в `main.py` или передав пользовательскую конфигурацию программно. См. раздел [Конфигурация](#конфигурация) для деталей.

## Конфигурация

Приложение настраивается через класс `AppConfiguration` в `src/config/AppConfiguration.py`. Настройку можно выполнить следующим образом:

1. **Изменение `main.py`**:
   Обновите экземпляр `AppConfiguration` в `main.py`:
   ```python
   from src.config.configuration import AppConfiguration
   from src.application import Application

   config = AppConfiguration(
       input_model="custom/path/model.xml",
       input_config_paths=["custom/config1.json", "custom/config2.json"],
       output_dir="custom_output",
       output_paths={
           "XmlConfigOutputGenerator": "custom_output/custom_config.xml",
           "MetaJsonOutputGenerator": "custom_output/custom_meta.json"
       },
       output_config_paths=["custom_output/custom_delta.json", "custom_output/custom_patched.json"]
   )
   app = Application(config=config)
   app.run()
   ```

2. **Настройка окружения**:
   Убедитесь, что входные файлы (`input_model` и `input_config_paths`) существуют и доступны. Выходная директория будет создана автоматически, если она не существует.

### Параметры конфигурации
- `input_model`: Путь к XML-файлу модели (по умолчанию: `input/impulse_test_input.xml`)
- `input_config_paths`: Список JSON-файлов конфигурации для сравнения (по умолчанию: `["input/config.json", "input/patched_config.json"]`)
- `output_dir`: Директория для выходных файлов (по умолчанию: `out`)
- `output_paths`: Словарь, связывающий генераторы вывода с путями к выходным файлам
- `output_config_paths`: Список путей для файлов дельт и пропатченных конфигураций

## Расширение проекта

Проект разработан с учетом расширяемости, используя шаблоны проектирования для упрощения добавления новой функциональности. Примеры расширения возможностей проекта:

### Добавление нового парсера
Чтобы поддержать новый формат конфигурационных файлов (e.g. YAML):
1. Создайте новый класс парсера в `src/parser/parser.py`, наследующий от `ConfigParser`:
   ```python
   class YamlConfigParser(ConfigParser):
       def parse(self, file_path: str) -> Dict:
           import yaml
           with open(file_path, 'r') as f:
               return yaml.safe_load(f)
   ```
2. Зарегистрируйте парсер в `ConfigParserFactory`:
   ```python
   class ConfigParserFactory:
       def __init__(self):
           self.parsers = {
               ".xml": XmlConfigParser(),
               ".json": JsonConfigParser(),
               ".yaml": YamlConfigParser()
           }
   ```

### Добавление нового генератора вывода
Чтобы добавить новый формат вывода (например, CSV):
1. Создайте новый класс визитора в `src/model/visitor.py`, реализующий `ModelVisitor`:
   ```python
   class CsvVisitor sarc/model/visitor.py`, реализующий `ModelVisitor`:
   ```python
   class CsvVisitor(ModelVisitor):
       def __init__(self):
           self.csv_data = []
       
       def visit_class(self, class_info: ClassInfo) -> None:
           self.csv_data.append([class_info.name``

       def visit_attribute(self, attribute: Attribute) -> None:
           self.csv_data.append(["", "", "", attribute.name, attribute.type])
       
       def visit_relation(self, relation: Relation) -> None:
           pass
       
       def generate(self, model: Dict) -> List:
           for class_info in model["classes"].values():
               class_info.accept(self)
           return self.csv_data
   ```
2. Создайте новый генератор в `src/output/generator.py`:
   ```python
   class CsvOutputGenerator(OutputGenerator):
       def __init__(self, visitor: ModelVisitor = None):
           self.visitor = visitor or CsvVisitor()
       
       def generate(self, model: Dict, config: AppConfiguration) -> None:
           import csv
           csv_data = self.visitor.generate(model)
           with open(config.output_paths[self.key()], "w", newline="") as f:
               writer = csv.writer(f)
               writer.writerows(csv_data)
       
       @classmethod
       def key(cls) -> str:
           return "CsvOutputGenerator"
   ```
3. Добавьте генератор в `Application` в `main.py`:
   ```python
   app = Application(
       config=config,
       output_generators=[XmlConfigOutputGenerator(), MetaJsonOutputGenerator(), CsvOutputGenerator()]
   )
   ```

### Добавление нового процессора конфигураций
Чтобы обрабатывать конфигурации по-другому (например, сравнение на основе XML):
1. Создайте новый процессор в `src/processor/config_processor.py`:
   ```python
   class XmlConfigProcessor(ConfigProcessor):
       def process(self, config: AppConfiguration, comparator: ConfigComparator) -> None:
           # Реализуйте логику для XML
           pass
   ```
2. Используйте его в `main.py`:
   ```python
   app = Application(config=config, config_processor=XmlConfigProcessor())
   ```

## Структура проекта

```
project/
├── src/
│   ├── config/              # Классы конфигурации
│   ├── model/               # Элементы модели, шаблоны Builder и Visitor
│   ├── parser/              # Парсеры для XML и JSON файлов
│   ├── processor/           # Логика обработки моделей и конфигураций
│   ├── output/              # Логика генерации выходных данных
│   └── application.py       # Запуск приложения
├── main.py                  # Точка входа
└── README.md                # Документация проекта
```

## UML диаграмма классов

В yadro.drawio можно ознакомиться с UML диаграммой данного проекта.
