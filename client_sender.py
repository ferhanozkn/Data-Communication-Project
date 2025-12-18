import socket
import sys

def calculate_parity(data, parity_type='even'):

    result = []
    for char in data:
        ascii_val = ord(char)
        ones_count = bin(ascii_val).count('1')
        
        if parity_type == 'even':
            parity_bit = '0' if ones_count % 2 == 0 else '1'
        else:  # odd
            parity_bit = '1' if ones_count % 2 == 0 else '0'
        
        result.append(parity_bit)
    
    return ''.join(result)

def calculate_2d_parity(data):

    binary_matrix = []
    for char in data:
        binary = format(ord(char), '08b')
        binary_matrix.append(list(binary))

    row_parities = []
    for row in binary_matrix:
        ones = row.count('1')
        row_parities.append('0' if ones % 2 == 0 else '1')

    col_parities = []
    if binary_matrix:
        for col_idx in range(8):
            ones = sum(1 for row in binary_matrix if row[col_idx] == '1')
            col_parities.append('0' if ones % 2 == 0 else '1')

    return ''.join(row_parities) + ''.join(col_parities)

def calculate_crc16(data):

    polynomial = 0x1021
    crc = 0xFFFF
    
    for char in data:
        crc ^= (ord(char) << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFFFF
    
    return format(crc, '04X')

def calculate_hamming(data):

    result = []
    
    for char in data:
        bits = format(ord(char), '08b')

        for i in range(0, 8, 4):
            block = bits[i:i+4]
            d1, d2, d3, d4 = [int(b) for b in block]

            p1 = d1 ^ d2 ^ d4
            p2 = d1 ^ d3 ^ d4
            p3 = d2 ^ d3 ^ d4
            
            result.append(str(p1) + str(p2) + str(p3))
    
    return ''.join(result)

def calculate_checksum(data):

    checksum = 0

    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (ord(data[i]) << 8) + ord(data[i+1])
        else:
            word = ord(data[i]) << 8
        
        checksum += word

        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF
    
    return format(checksum, '04X')

def main():
    print("=" * 50)
    print("Gönderici Client - VERİ GÖNDERİCİ")
    print("=" * 50)

    data = input("\nAlıcıya göndermek istediğiniz metni girin: ").strip()
    
    if not data:
        print("Hata: Boş metin gönderilemez!")
        return

    print("\n--- Hata Tespit Yöntemini Seçin ---")
    print("1. Parity Bit (Even)")
    print("2. Parity Bit (Odd)")
    print("3. 2D Parity")
    print("4. CRC-16")
    print("5. Hamming Code")
    print("6. Internet Checksum")
    
    choice = input("\nSeçiminiz (1-6): ").strip()

    if choice == '1':
        method = "PARITY_EVEN"
        control_info = calculate_parity(data, 'even')
    elif choice == '2':
        method = "PARITY_ODD"
        control_info = calculate_parity(data, 'odd')
    elif choice == '3':
        method = "2D_PARITY"
        control_info = calculate_2d_parity(data)
    elif choice == '4':
        method = "CRC16"
        control_info = calculate_crc16(data)
    elif choice == '5':
        method = "HAMMING"
        control_info = calculate_hamming(data)
    elif choice == '6':
        method = "CHECKSUM"
        control_info = calculate_checksum(data)
    else:
        print("Geçersiz seçim!")
        return

    packet = f"{data}|{method}|{control_info}"
    
    print(f"\n--- Paket Bilgileri ---")
    print(f"Veri: {data}")
    print(f"Yöntem: {method}")
    print(f"Kontrol Bilgisi: {control_info}")
    print(f"Paket: {packet}")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 5000))

        client_socket.send(packet.encode('utf-8'))
        print("\n✓ Paket server'a gönderildi!")
        
        client_socket.close()
        
    except Exception as e:
        print(f"\n✗ Hata oluştu: {e}")

if __name__ == "__main__":
    main()