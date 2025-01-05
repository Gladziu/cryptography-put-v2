import hashlib
import os
import time

'''
Algorytmy:
- md5
- sha1
- sha2 (sha224, sha256, sha384, sha512, sha512_224, sha512_256)
- sha3 (sha3_224, sha3_256, sha3_384, sha3_512)
'''
algorithms = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']


def generate_hash(text, algorithm):
    hash_func = getattr(hashlib, algorithm)
    hash_obj = hash_func()
    hash_obj.update(text.encode('utf-8'))
    return hash_obj.hexdigest()


def generate_hash_by_input():
    text = input("Wprowadź tekst do zhashowania: ")

    print("\nWyniki dla wprowadzonego tekstu:")
    for algorithm in algorithms:
        hash_value = generate_hash(text, algorithm)
        print(
            f"Algorytm: {algorithm.upper():<10} | Skrót: {hash_value} | Długość: {len(hash_value)} | Długoś w bitach: {len(hash_value) * 4}")

def compare_hash_functions(input_data):
    print("\nPorównanie szybkości działania")
    results = []

    for data in input_data:
        print("\nDługość wproadzonego tekstu:", len(data))
        for algorithm in algorithms:
            start_time = time.time()
            hash_value = generate_hash(data, algorithm)
            elapsed_time = time.time() - start_time
            print(
                f"Algorytm: {algorithm.upper():<10} | Skrót: {hash_value} | Czas: {elapsed_time:.6f}s")
            results.append((algorithm, len(hash_value), elapsed_time))
    return results


def check_collisions(num_samples, algorithm):
    print(f"\nSprawdzanie kolizji dla algorytmu {algorithm}")
    seen_hashes = {}

    for _ in range(num_samples):
        # Tworzymy losowe dane wejściowe
        random_data = str(os.urandom(16))
        hash_value = generate_hash(random_data, algorithm)

        # Zapisujemy pierwsze 12 bitów skrótu
        first_12_bits = hash_value[:3]

        if first_12_bits in seen_hashes:
            print(
                f"Kolizja! Dwa różne teksty mają te same pierwsze 12 {[first_12_bits]} bitów skrótu: {seen_hashes[first_12_bits]} i {str(os.urandom(16))}")
            return
        seen_hashes[first_12_bits] = str(os.urandom(16))

    print("Brak kolizji na pierwszych 12 bitach.")


def test_sac(algorithm):
    print(f"\nTestowanie SAC dla algorytmu {algorithm}")
    text = "Test"

    original_hash = generate_hash(text, algorithm)
    print(f"Pierwotny tekst: {text}")
    print(f"Pierwotny skrót: {original_hash}")

    # Oryginalny skrót na postać binarną
    original_hash_binary = bin(int(original_hash, 16))[2:].zfill(len(original_hash) * 4)

    # Testujemy zmianę jednego bitu w tekście
    for i in range(len(text) * 8):

        text_bytes = bytearray(text, 'utf-8')
        byte_index = i // 8
        bit_index = i % 8

        # Zmieniamy dokładnie jeden bit w odpowiednim bajcie
        text_bytes[byte_index] ^= (1 << bit_index)
        modified_text = text_bytes.decode('utf-8', errors='ignore')

        modified_hash = generate_hash(modified_text, algorithm)
        modified_hash_binary = bin(int(modified_hash, 16))[2:].zfill(len(modified_hash) * 4)

        bit_diff = 0
        for a, b in zip(original_hash_binary, modified_hash_binary):
            if a != b:
                bit_diff += 1

        print(f"Zmodyfikowany tekst: {modified_text}")
        print(f"Zmodyfikowany skrót: {modified_hash}")
        print(f"Liczba różniących się bitów w skrócie: {bit_diff}")


def main():
    generate_hash_by_input()

    input_data = [
        "test",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "x" * 1000000,
        "x" * 100000000
    ]
    compare_hash_functions(input_data)

    check_collisions(100, "sha3_256")

    test_sac("sha256")

if __name__ == "__main__":
    main()
