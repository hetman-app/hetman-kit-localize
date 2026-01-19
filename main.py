from codetable import Codetable, msg, i18n

i18n.set_base_locale("en")  # Bardzo ważne, inaczej będzie błąd przy i18n()


class UserError(Codetable):
    NAMESPACE = "user"

    NOT_FOUND = msg("User not found.")

    ALREADY_EXISTS = i18n(
        en="User already exists.",
        pl="Użytkownik już istnieje.",
    )


print(UserError.NOT_FOUND)
print(UserError.ALREADY_EXISTS)

i18n.set_locale("pl")

print(UserError.ALREADY_EXISTS)

Codetable.key_map = {"code": "error_code", "value": "message"}

print(UserError.ALREADY_EXISTS)


class UserSuccess(Codetable):
    NAMESPACE = "user"

    CREATED = msg("User created successfully.")

    UPDATED = i18n(
        en="User updated successfully.",
        pl="Użytkownik został zaktualizowany pomyślnie.",
    )


print(UserSuccess.CREATED)
print(UserSuccess.UPDATED)
