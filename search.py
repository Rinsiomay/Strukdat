import pandas as pd
import os

# Configuration
GOOGLE_SHEETS_CSV_URL = 'https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv'
EXCEL_HEADER_ROW = 0

# Dataset columns
COLUMNS_TO_FETCH = [
    'no', 'nim', 'nama_mahasiswa', 'sumber_database',
    'fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal',
    'judul_paper', 'tahun_terbit', 'nama_penulis',
    'abstrak_langusung_copas_dari_paper',
    'kesimpulan_langusung_copas_dari_paper', 'link_paper'
]
COL_JUDUL = 'judul_paper'
COL_TAHUN = 'tahun_terbit'
COL_PENULIS = 'nama_penulis'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_data_from_csv(csv_url, header_row):
    print("🌐 Mengambil data dari Google Sheets (CSV)...")
    df = pd.read_csv(csv_url, header=header_row)
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace(r'[^a-z0-9_]', '', regex=True)
    )
    data = df.to_dict(orient='records')
    print(f"✅ Berhasil mengambil {len(data)} baris data.")
    return data


def sequential_search(data_list, search_term, column_key):
    results = []
    term = str(search_term).strip().lower()
    if not term:
        print("⚠️ Kata kunci pencarian kosong.")
        return []
    if column_key == COL_TAHUN:
        try:
            num = float(term)
            for item in data_list:
                if column_key in item and item[column_key] is not None:
                    try:
                        if float(item[column_key]) == num:
                            results.append(item)
                    except:
                        pass
        except:
            print(f"❌ Nilai tahun '{search_term}' tidak valid.")
    else:
        for item in data_list:
            if column_key in item and item[column_key] is not None:
                if term in str(item[column_key]).strip().lower():
                    results.append(item)
    return results


def dichotomous_search(sorted_data, search_term, column_key):
    results = []
    term = str(search_term).strip().lower()
    if not term:
        print("⚠️ Kata kunci pencarian kosong.")
        return []
    if column_key == COL_TAHUN:
        try:
            num = float(term)
            for item in sorted_data:
                if column_key in item and item[column_key] is not None:
                    try:
                        if float(item[column_key]) == num:
                            results.append(item)
                    except:
                        pass
        except:
            print(f"❌ Nilai tahun '{search_term}' tidak valid.")
    else:
        for item in sorted_data:
            if column_key in item and item[column_key] is not None:
                if str(item[column_key]).strip().lower() == term:
                    results.append(item)
    return results


def display_result(row, index):
    print(f"\n🎉 Hasil #{index} 🎉")
    print("─" * 60)
    for col in COLUMNS_TO_FETCH:
        val = row.get(col, 'N/A')
        if col == 'fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal':
            label = 'Fokus Kata Kunci'
        else:
            label = col.replace('_', ' ').title()

        if col == 'abstrak_langusung_copas_dari_paper':
            print("\n\n📝 Abstrak:")
            print(f"{val}")
            continue
        if col == 'kesimpulan_langusung_copas_dari_paper':
            print("\n\n💡 Kesimpulan:")
            print(f"{val}")
            continue

        print(f"  {label:<50}: {val}")
    print("─" * 60)


if __name__ == "__main__":
    clear_screen()
    print("✨✨✨ Program Pencarian Data Paper ✨✨✨")

    try:
        all_data = load_data_from_csv(GOOGLE_SHEETS_CSV_URL, EXCEL_HEADER_ROW)
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Tekan Enter untuk keluar...")
        exit()

    if not all_data:
        print("🚫 Tidak ada data. Program berhenti.")
        input("Tekan Enter untuk keluar...")
        exit()

    while True:
        clear_screen()
        print("🔍🔍🔍 MENU PENCARIAN 🔍🔍🔍")
        print("1️⃣  Judul Paper")
        print("2️⃣  Tahun Terbit")
        print("3️⃣  Nama Penulis")
        print("❌  Keluar")
        choice = input("Pilih kolom (1/2/3/q): ").strip().lower()
        if choice == 'q':
            break
        key_map = {'1': COL_JUDUL, '2': COL_TAHUN, '3': COL_PENULIS}
        key = key_map.get(choice)
        if not key:
            print("⚠️ Pilihan tidak valid.")
            input("Enter untuk ulang...")
            continue

        value = input(f"🔑 Masukkan kata kunci untuk '{key}': ").strip()
        if not value:
            print("⚠️ Kata kunci kosong.")
            input("Enter untuk ulang...")
            continue

        print("\n▶️ Memilih metode pencarian:")
        print("1️⃣ Linear Search")
        print("2️⃣ Binary Search")
        method = input("Pilih metode (1/2): ").strip()

        if method == '2':
            if key == COL_TAHUN:
                sorted_data = sorted(
                    [d for d in all_data if pd.api.types.is_number(d.get(key)) or str(d.get(key)).replace('.', '',1).isdigit()],
                    key=lambda x: float(x[key])
                )
            else:
                sorted_data = sorted(
                    [d for d in all_data if d.get(key) is not None],
                    key=lambda x: str(x[key]).lower()
                )
            results = dichotomous_search(sorted_data, value, key)
        else:
            results = sequential_search(all_data, value, key)

        clear_screen()
        print(f"\n🔎 Hasil Pencarian untuk '{value}' di '{key}' 🔎")
        print(f"\n🎯 Ditemukan {len(results)} dataset yang sesuai! 🎯")

        if results:
            for idx, row in enumerate(results, start=1):
                display_result(row, idx)
        else:
            print("😢 Maaf, tidak ada hasil yang ditemukan.")

        input("\n🙏 Tekan Enter untuk pencarian lain...")

    clear_screen()
    print("👋 Terima kasih! Sampai jumpa lagi 🙏")
