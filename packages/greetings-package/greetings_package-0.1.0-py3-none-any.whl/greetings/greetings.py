def say_hello(language="english"):
    greetings = {
        "english": "Hello",
        "spanish": "Hola",
        "french": "Bonjour",
        "german": "Hallo",
        "japanese": "こんにちは (Konnichiwa)"
    }
    return greetings.get(language.lower(), "Hello")


def say_goodbye(language="english"):
    farewells = {
        "english": "Goodbye",
        "spanish": "Adiós",
        "french": "Au revoir",
        "german": "Tschüss",
        "japanese": "さようなら (Sayōnara)"
    }
    return farewells.get(language.lower(), "Goodbye")
