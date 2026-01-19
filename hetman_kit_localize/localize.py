from contextvars import ContextVar
from typing import Any, ClassVar


class Localize:
    """    
    This class provides thread-safe locale management using context variables,
    allowing for concurrent execution with different locale settings per context.
    It maintains both a base locale (default) and a current locale (per-context).
    
    Attributes:
        _base_locale: The default locale used when no context-specific locale is set.
        _current_locale: A context variable that holds the current locale for each context.
    """
    _base_locale: ClassVar[str]

    _current_locale: ClassVar[ContextVar[str]
                             ] = ContextVar("hetman_kit_localize.locale")

    @classmethod
    def resolve_translation(
        cls, data: dict[str, Any], strict: bool = True
    ) -> Any:
        """
        Resolves a translation based on the current locale.
        
        Args:
            data: A dictionary containing translations for different locales.
            strict: If True, raises a KeyError if the locale and base locale are not found. If False, returns None.
            
        Returns:
            The translation for the current locale, or None (if strict is False) if the locale is not found.
        """
        locale: str = cls.get_locale()

        base_locale: str = cls.get_base_locale()

        if strict:
            return data.get(locale, data[base_locale])

        return data.get(locale, data.get(base_locale))

    @classmethod
    def get_locale(cls) -> str:
        """
        Retrieves the current locale for the active context.
        
        If no locale has been set for the current context, returns the base locale.
        
        Returns:
            The current locale string for the active context, or the base locale
            if no context-specific locale has been set.
        """
        return cls._current_locale.get(cls.get_base_locale())

    @classmethod
    def set_locale(cls, locale: str) -> None:
        """
        Sets the locale for the current context.
        
        This method sets a context-specific locale that will be used for the
        current execution context. Different contexts can have different locales.
        
        Args:
            locale: The locale string to set (e.g., 'en', 'pl').
        """
        cls._current_locale.set(locale)

    @classmethod
    def get_base_locale(cls) -> str:
        """
        Retrieves the base (default) locale.
        
        The base locale is used as the default when no context-specific locale
        has been set.
        
        Returns:
            The base locale string.
            
        Raises:
            RuntimeError: If the base locale has not been set using set_base_locale().
        """
        if not hasattr(cls, "_base_locale"):
            raise RuntimeError(
                "Base locale is not set. Use .set_base_locale() to define the base locale."
            )

        return cls._base_locale

    @classmethod
    def set_base_locale(cls, base_locale: str) -> None:
        """Sets the base (default) locale for the application.
        
        This should typically be called once during application initialization.
        The base locale is used as the fallback when no context-specific locale
        has been set.
        
        Args:
            base_locale: The base locale string to set (e.g., 'en_US', 'pl_PL').
        """
        cls._base_locale = base_locale
