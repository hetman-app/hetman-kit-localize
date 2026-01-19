<img src="https://hetman.app/svg/logo/full-white-text.svg" alt="Hetman Logo" width="200" height="38" />

**Hetman Kit Localize** provides thread-safe locale management using context variables. It enables concurrent execution with different locale settings per context.

## Installation

```bash
pip install hetman-kit-localize
```

## Why use this?

Managing locale settings in concurrent applications can be challenging. **Hetman Kit Localize** allows you to:

1.  **Thread-Safe Locale Management**: Use context variables to ensure each execution context has its own locale.
2.  **Simple API**: Easy-to-use class methods for getting and setting locales.
3.  **Base Locale Support**: Define a default locale that serves as a fallback.
4.  **Concurrent Execution**: Perfect for async applications where different requests need different locales.

## Usage Example

### Setting Up Locales

Set the base locale once during application initialization:

```python
from hetman_kit_localize import Localize

# Set the base (default) locale
Localize.set_base_locale("en")
```

### Getting and Setting Locales

```python
from hetman_kit_localize import Localize

# Set up the base locale first
Localize.set_base_locale("en")

# Get the current locale (returns base locale if not set)
print(Localize.get_locale())  # Output: en

# Set a different locale for the current context
Localize.set_locale("pl")
print(Localize.get_locale())  # Output: pl

# Get the base locale
print(Localize.get_base_locale())  # Output: en
```

### Context-Aware Example

The locale management is context-aware, making it perfect for web applications where each request might need a different locale:

```python
from hetman_kit_localize import Localize
import asyncio


async def handle_request(locale: str):
    # Each request can have its own locale
    Localize.set_locale(locale)

    # This will return the locale for this specific context
    current = Localize.get_locale()
    print(f"Handling request with locale: {current}")


# Set the base locale
Localize.set_base_locale("en")


async def main():
    await asyncio.gather(
        handle_request("pl"),
        handle_request("en"),
        handle_request("de"),
    )


# Simulate concurrent requests with different locales
asyncio.run(main())
```

### Resolving Translations

The `resolve_translation()` method helps you retrieve the correct translation from a dictionary based on the current locale:

```python
from hetman_kit_localize import Localize

# Set up locales
Localize.set_base_locale("en")

# Define translations
messages = {
    "en": "Hello, World!",
    "pl": "Witaj, Świecie!",
    "de": "Hallo, Welt!"
}

# Get translation for current locale (falls back to base locale)
Localize.set_locale("pl")
print(Localize.resolve_translation(messages))  # Output: Witaj, Świecie!

Localize.set_locale("de")
print(Localize.resolve_translation(messages))  # Output: Hallo, Welt!

# If locale is not found, falls back to base locale
Localize.set_locale("fr")
print(Localize.resolve_translation(messages))  # Output: Hello, World!

# Use strict=False to return None instead of raising KeyError when neither locale nor base locale exists
partial_messages = {"pl": "Witaj!"}
Localize.set_locale("en")
print(Localize.resolve_translation(partial_messages, strict=False))  # Output: None
```

## Core Features

-   **Thread-Safe**: Uses Python's `contextvars` for safe concurrent locale management.
-   **Simple API**: Just four class methods: `set_base_locale()`, `get_base_locale()`, `set_locale()`, `get_locale()`.
-   **Context Variables**: Each execution context maintains its own locale state.

## Why "Kit"?

This package is called **Hetman Kit Localize** because it's designed to be a building block ("kit") for your own i18n solutions. Other classes can inherit from `Localize` to easily add locale management to their functionality:

```python
from hetman_kit_localize import Localize

class MyI18nClass(Localize):
    MESSAGES = {
        "welcome": {
            "en": "Welcome!",
            "pl": "Witaj!",
            "de": "Willkommen!"
        },
        "goodbye": {
            "en": "Goodbye!",
            "pl": "Do widzenia!",
            "de": "Auf Wiedersehen!"
        }
    }
    
    @classmethod
    def get_message(cls, key: str) -> str:
        # Use resolve_translation to get the right message
        return cls.resolve_translation(cls.MESSAGES[key])

# Inherits all locale management methods
MyI18nClass.set_base_locale("en")
MyI18nClass.set_locale("pl")
print(MyI18nClass.get_locale())  # Output: pl
print(MyI18nClass.get_message("welcome"))  # Output: Witaj!

MyI18nClass.set_locale("de")
print(MyI18nClass.get_message("goodbye"))  # Output: Auf Wiedersehen!
```

By inheriting from `Localize`, your classes automatically get thread-safe locale management without any additional setup!