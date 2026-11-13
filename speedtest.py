import argparse
import time
import sys
import requests

def measure_speed(url: str, num_requests: int = 10):
    """
    Замеряет скорость скачивания, делая num_requests последовательных запросов.
    """
    
    total_bytes = 0
    total_time = 0.0
    
    print(f"Начало теста. Целевой URL: {url}")
    print(f"Будет выполнено {num_requests} последовательных запросов...\n")

    for i in range(1, num_requests + 1):
        start_time = time.perf_counter()
        
        try:
            # stream=True позволяет скачивать файл частями, не загружая его целиком в RAM
            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()
                
                bytes_downloaded = 0
                # Итерируемся по чанкам, чтобы дождаться полного ответа и посчитать байты
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        bytes_downloaded += len(chunk)
                        
        except requests.exceptions.RequestException as e:
            print(f"\nОшибка на запросе {i}: {e}")
            sys.exit(1)

        end_time = time.perf_counter()
        request_time = end_time - start_time
        
        total_bytes += bytes_downloaded
        total_time += request_time

        # Выводим прогресс в консоль
        size_kb = bytes_downloaded / 1024
        print(f"Запрос {i:2d}: скачано {size_kb:8.2f} KB за {request_time:.3f} сек")

    # Расчет результатов
    avg_time = total_time / num_requests
    
    # Считаем скорость в Мегабитах в секунду (Mbps)
    # 1 байт = 8 бит. 1 Мегабит = 1 000 000 бит.
    speed_mbps = (total_bytes * 8) / (total_time * 1_000_000)
    
    total_mb = total_bytes / (1024 * 1024)

    print("\n" + "="*30)
    print("РЕЗУЛЬТАТЫ ТЕСТА")
    print("="*30)
    print(f"Всего скачано:      {total_mb:.2f} MB")
    print(f"Общее время:        {total_time:.2f} сек")
    print(f"Среднее время:      {avg_time:.3f} сек")
    print(f"Скорость скачивания: {speed_mbps:.2f} Mbps")
    print("="*30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для замера скорости интернета.")
    parser.add_argument("url", type=str, help="Адрес файла для скачивания (например, тяжёлая картинка)")
    parser.add_argument("-n", "--num", type=int, default=10, help="Количество запросов (по умолчанию 10)")
    
    args = parser.parse_args()
    
    if args.num <= 0:
        print("Количество запросов должно быть больше 0.")
        sys.exit(1)
        
    measure_speed(args.url, args.num)
