import timeit
from pathlib import Path


def boyer_moore(text, pattern):
    if not pattern:
        return 0

    last = {char: index for index, char in enumerate(pattern)}
    shift = 0

    while shift <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return shift

        shift += max(1, j - last.get(text[shift + j], -1))

    return -1


def kmp(text, pattern):
    if not pattern:
        return 0

    # Побудова префіксної таблиці
    lps = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        lps[i] = j

    # Пошук підрядка
    j = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            return i - j + 1

    return -1


def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    base = 256
    modulus = 1_000_000_007
    high = pow(base, m - 1, modulus)

    pattern_hash = 0
    text_hash = 0

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % modulus
        text_hash = (text_hash * base + ord(text[i])) % modulus

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (
                (text_hash - ord(text[i]) * high) * base
                + ord(text[i + m])
            ) % modulus

    return -1


def main():
    folder = Path(__file__).resolve().parent

    files = [
        ("стаття 1.txt", "cp1251"),
        ("стаття 2 (1).txt", "utf-8-sig"),
    ]

    algorithms = {
        "Boyer-Moore": boyer_moore,
        "KMP": kmp,
        "Rabin-Karp": rabin_karp,
    }

    repetitions = 100

    for filename, encoding in files:
        text = (folder / filename).read_text(encoding=encoding)

        middle = len(text) // 2
        patterns = {
            "Наявний": text[middle:middle + 30],
            "Відсутній": "Цього підрядка немає у статті!",
        }

        print(f"\n{filename}")

        for description, pattern in patterns.items():
            print(f"\n{description} підрядок: {pattern!r}")

            for name, algorithm in algorithms.items():
                assert algorithm(text, pattern) == text.find(pattern)

                elapsed = timeit.timeit(
                    lambda: algorithm(text, pattern),
                    number=repetitions,
                )

                print(f"{name}: {elapsed / repetitions:.8f} с")


if __name__ == "__main__":
    main()