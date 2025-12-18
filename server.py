import socket
import random
import time

def bit_flip(data):

    if not data:
        return data
    
    data_bytes = bytearray(data.encode('utf-8'))
    random_byte = random.randint(0, len(data_bytes) - 1)
    random_bit = random.randint(0, 7)
    
    data_bytes[random_byte] ^= (1 << random_bit)
    
    try:
        return data_bytes.decode('utf-8', errors='ignore')
    except:
        return data

def character_substitution(data):

    if not data:
        return data
    
    pos = random.randint(0, len(data) - 1)
    new_char = chr(random.randint(65, 90))  # A-Z arası
    return data[:pos] + new_char + data[pos+1:]

def character_deletion(data):

    if len(data) <= 1:
        return data
    
    pos = random.randint(0, len(data) - 1)
    return data[:pos] + data[pos+1:]

def character_insertion(data):

    if not data:
        return data
    
    pos = random.randint(0, len(data))
    new_char = chr(random.randint(97, 122))  # a-z arası
    return data[:pos] + new_char + data[pos:]

def character_swapping(data):

    if len(data) < 2:
        return data
    
    pos = random.randint(0, len(data) - 2)
    data_list = list(data)
    data_list[pos], data_list[pos+1] = data_list[pos+1], data_list[pos]
    return ''.join(data_list)

def multiple_bit_flips(data):

    result = data
    flip_count = random.randint(2, 4)
    for _ in range(flip_count):
        result = bit_flip(result)
    return result

def burst_error(data):

    if len(data) < 3:
        return data
    
    burst_length = min(random.randint(3, 8), len(data))
    start_pos = random.randint(0, len(data) - burst_length)
    
    corrupted = ''.join(chr(random.randint(33, 126)) for _ in range(burst_length))
    
    return data[:start_pos] + corrupted + data[start_pos + burst_length:]

def corrupt_data(data, method):

    methods = {
        1: ("Bit Flip", bit_flip),
        2: ("Character Substitution", character_substitution),
        3: ("Character Deletion", character_deletion),
        4: ("Character Insertion", character_insertion),
        5: ("Character Swapping", character_swapping),
        6: ("Multiple Bit Flips", multiple_bit_flips),
        7: ("Burst Error", burst_error)
    }
    
    method_name, method_func = methods[method]
    corrupted = method_func(data)
    
    return corrupted, method_name

def main():
    print("=" * 50)
    print("SERVER - ARA DÜĞÜM + VERİ BOZUCU")
    print("=" * 50)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    
    print("\n✓ Server 5000 portunda dinleniyor...")
    print("✓ Gönderici Client'tan veri bekleniyor...\n")
    
    while True:
        try:

            conn, addr = server_socket.accept()
            print(f"✓ Gönderici Client bağlandı: {addr}")

            data = conn.recv(4096).decode('utf-8')
            conn.close()
            
            if not data:
                continue
            
            print(f"\n--- Gelen Paket ---")
            print(f"Paket: {data}")

            parts = data.split('|')
            if len(parts) != 3:
                print("Hatalı paket formatı!")
                continue
            
            original_data, method, control_info = parts
            
            print(f"Orijinal Veri: {original_data}")
            print(f"Yöntem: {method}")
            print(f"Kontrol Bilgisi: {control_info}")

            print("\n--- Hata Enjeksiyon Yöntemini Seçin ---")
            print("1. Bit Flip")
            print("2. Character Substitution")
            print("3. Character Deletion")
            print("4. Character Insertion")
            print("5. Character Swapping")
            print("6. Multiple Bit Flips")
            print("7. Burst Error")
            print("8. Hata Enjekte Etme (Temiz Gönder)")
            
            corruption_choice = input("\nSeçiminiz (1-8): ").strip()
            
            if corruption_choice == '8':
                corrupted_data = original_data
                corruption_method = "Hata Yok (Temiz)"
            else:
                try:
                    choice_num = int(corruption_choice)
                    if 1 <= choice_num <= 7:
                        corrupted_data, corruption_method = corrupt_data(original_data, choice_num)
                    else:
                        corrupted_data = original_data
                        corruption_method = "Geçersiz Seçim (Temiz Gönderildi)"
                except:
                    corrupted_data = original_data
                    corruption_method = "Hata (Temiz Gönderildi)"
            
            print(f"\n--- Bozulma Sonucu ---")
            print(f"Uygulanan Yöntem: {corruption_method}")
            print(f"Orijinal: {original_data}")
            print(f"Bozulmuş: {corrupted_data}")

            new_packet = f"{corrupted_data}|{method}|{control_info}"

            print("\n✓ Alıcı Client'a  gönderiliyor...")
            time.sleep(1)

            client2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client2_socket.connect(('localhost', 5001))
                client2_socket.send(new_packet.encode('utf-8'))
                print("✓ Paket Alıcı Client'a gönderildi!\n")
            except:
                print("✗ Alıcı Client'a bağlanılamadı! Alıcı Client'ı başlattığınızdan emin olun.\n")
            finally:
                client2_socket.close()
            
            print("=" * 50)
            print("\n✓ Bir sonraki paketi bekleniyor...\n")
            
        except KeyboardInterrupt:
            print("\n\nServer kapatılıyor...")
            break
        except Exception as e:
            print(f"Hata: {e}")
            continue
    
    server_socket.close()

if __name__ == "__main__":
    main()