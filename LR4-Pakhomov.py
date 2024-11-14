import random

# Таблиця замін для S-блоку (можна змінити за потребою)
S_BOX = [
    0x3, 0xF, 0xE, 0x8,
    0x2, 0xD, 0xB, 0x7,
    0x0, 0xA, 0x9, 0x5,
    0x6, 0xC, 0x4, 0x1
]

# Генеруємо зворотну таблицю замін для S-блоку
INV_S_BOX = [0] * len(S_BOX)
for i, v in enumerate(S_BOX):
    INV_S_BOX[v] = i

def s_block_forward(input_byte):
    """Пряме перетворення S-блоку"""
    print(f"Блок S, початкове значення {input_byte:#04x}.", end=' ')
    left_nibble = (input_byte >> 4) & 0xF
    right_nibble = input_byte & 0xF
    left_substitute = S_BOX[left_nibble]
    right_substitute = S_BOX[right_nibble]
    result = (left_substitute << 4) | right_substitute
    print(f"Значення після шифрування {result:#04x}")
    return result

def s_block_inverse(output_byte):
    """Зворотне перетворення S-блоку"""
    print(f"Блок S, початкове значення {output_byte:#04x}.", end=' ')
    left_nibble = (output_byte >> 4) & 0xF
    right_nibble = output_byte & 0xF
    left_original = INV_S_BOX[left_nibble]
    right_original = INV_S_BOX[right_nibble]
    result = (left_original << 4) | right_original
    print(f"Значення після дешифрування {result:#04x}")
    return result

# Формула перестановки бітів для P-блоку (можна змінити за потребою)
P_PERMUTATION = [1, 5, 2, 0, 3, 7, 4, 6]

def p_block_forward(input_byte):
    """Пряме перетворення P-блоку"""
    print(f"Блок P, початкове значення {input_byte:#04x}.", end=' ')
    output_byte = 0
    for i, bit_position in enumerate(P_PERMUTATION):
        bit = (input_byte >> bit_position) & 1
        output_byte |= (bit << i)
    print(f"Значення після шифрування {output_byte:#04x}")
    return output_byte

def p_block_inverse(output_byte):
    """Зворотне перетворення P-блоку"""
    print(f"Блок P, початкове значення {output_byte:#04x}.", end=' ')
    input_byte = 0
    for i, bit_position in enumerate(P_PERMUTATION):
        bit = (output_byte >> i) & 1
        input_byte |= (bit << bit_position)
    print(f"Значення після дешифрування {input_byte:#04x}")
    return input_byte

# Розширене тестування функцій
def extended_test_s_p_blocks():
    # Тест для всіх значень байта від 0 до 255
    for byte in range(256):
        # S-блок
        encrypted_byte = s_block_forward(byte)
        decrypted_byte = s_block_inverse(encrypted_byte)
        assert byte == decrypted_byte, f"S-блок помилка при байті {byte}"

        # P-блок
        permuted_byte = p_block_forward(byte)
        original_byte = p_block_inverse(permuted_byte)
        assert byte == original_byte, f"P-блок помилка при байті {byte}"

    # Тест граничних значень
    boundary_values = [0x00, 0xFF, 0x0F, 0xF0]
    for byte in boundary_values:
        encrypted_byte = s_block_forward(byte)
        decrypted_byte = s_block_inverse(encrypted_byte)
        assert byte == decrypted_byte, f"S-блок помилка при граничному значенні {byte}"

        permuted_byte = p_block_forward(byte)
        original_byte = p_block_inverse(permuted_byte)
        assert byte == original_byte, f"P-блок помилка при граничному значенні {byte}"

    # Тест випадкових значень
    random.seed(42)
    for _ in range(100):
        byte = random.randint(0, 255)
        encrypted_byte = s_block_forward(byte)
        decrypted_byte = s_block_inverse(encrypted_byte)
        assert byte == decrypted_byte, f"S-блок помилка при випадковому значенні {byte}"

        permuted_byte = p_block_forward(byte)
        original_byte = p_block_inverse(permuted_byte)
        assert byte == original_byte, f"P-блок помилка при випадковому значенні {byte}"

    print("Всі розширені тести пройдено успішно.")

# Запуск розширених тестів
extended_test_s_p_blocks()
