from collections import Counter

English_letter_frequency = "etaoinshrdlucmwfgypbgkjqxz"


def caesar_encrypt(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def score_english(text):
    letters = [c.lower() for c in text if c.isalpha()]
    if not letters:
        return float('inf')
    freq = Counter(letters)
    observed = [ch for ch, _ in freq.most_common()]
    score = 0
    for i, ch in enumerate(observed):
        try:
            expected_pos = English_letter_frequency.index(ch)
        except ValueError:
            expected_pos = 25
        score += abs(i - expected_pos)
    return score


def break_caesar(ciphertext):
    best_shift = 0
    best_score = float('inf')
    best_text = ""
    for shift in range(26):
        candidate = caesar_decrypt(ciphertext, shift)
        s = score_english(candidate)
        if s < best_score:
            best_score = s
            best_shift = shift
            best_text = candidate
    return best_shift, best_text


if __name__ == "__main__":
    plaintext = "the quick brown fox jumps over the lazy dog " \
                "and the dog was not amused at all because it was tired"
    print("plaintext:  ", plaintext)

    cipher = caesar_encrypt(plaintext, 7)
    print("cipher:  ", cipher)

    shift, cracked = break_caesar(cipher)
    print(f"Recovered shift: {shift}")
    print("Cracked text:  ", cracked)
    print("Success:  ", cracked == plaintext)