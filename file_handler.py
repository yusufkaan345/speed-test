import json

def save_results_to_file(results, output_file):
    """
    Save results to a JSON file.
    """
    # Dosyayı okuma ve başlatma
    try:
        with open(output_file, 'r') as f:
            all_results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Dosya bulunmazsa ya da JSON hatası varsa
        all_results = []  # Boş bir liste ile başlat

    # Yeni sonuçları ekle
    all_results.append(results)

    # Verileri dosyaya yaz
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=4)

    print(f"Results have been saved to {output_file}.")
