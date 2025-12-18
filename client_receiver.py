import socket

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

def verify_packet(data, method, received_control):

    if method == "PARITY_EVEN":
        computed_control = calculate_parity(data, 'even')
    elif method == "PARITY_ODD":
        computed_control = calculate_parity(data, 'odd')
    elif method == "2D_PARITY":
        computed_control = calculate_2d_parity(data)
    elif method == "CRC16":
        computed_control = calculate_crc16(data)
    elif method == "HAMMING":
        computed_control = calculate_hamming(data)
    elif method == "CHECKSUM":
        computed_control = calculate_checksum(data)
    else:
        return None, "UNKNOWN METHOD"

    if computed_control == received_control:
        status = "✓ DATA CORRECT"
    else:
        status = "✗ DATA CORRUPTED"
    
    return computed_control, status

def main():
    print("=" * 50)
    print("CLIENT 2 - ALICI + HATA KONTROLCÜ")
    print("=" * 50)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(1)
    
    print("\n✓ Alıcı Client hazır, 5001 portunda dinleniyor...")
    print("✓ Server'dan veri bekleniyor...\n")
    
    while True:
        try:
            conn, addr = server_socket.accept()

            packet = conn.recv(4096).decode('utf-8')
            conn.close()
            
            if not packet:
                continue
            
            print("\n" + "=" * 50)
            print("YENİ PAKET ALINDI")
            print("=" * 50)

            parts = packet.split('|')
            if len(parts) != 3:
                print("Hatalı paket formatı!")
                continue
            
            received_data, method, received_control = parts

            computed_control, status = verify_packet(received_data, method, received_control)

            print(f"\nReceived Data        : {received_data}")
            print(f"Method               : {method}")
            print(f"Sent Check Bits      : {received_control}")
            print(f"Computed Check Bits  : {computed_control}")
            print(f"Status               : {status}")
            print("\n" + "=" * 50)
            
        except KeyboardInterrupt:
            print("\n\nAlıcı Client kapatılıyor...")
            break
        except Exception as e:
            print(f"Hata: {e}")
            continue
    
    server_socket.close()

if __name__ == "__main__":
    main()