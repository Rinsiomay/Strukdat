# Strukdat
# Struktur-Data
Tempat menampung tugas Struktur Data milik Ananta Galih Mahardika dengan NIM 3337240055

# DOKUMENTASI PROGRAM PENCARIAN MENGGUNAKAN ALGORITMA LINEAR DAN BINER PADA DATASET SPREADSHEET

- Repositori ini berisi program Python untuk mencari data paper akademik menggunakan **algoritma Linear Search dan Binary Search**
- Data paper diambil otomatis dari Google Spreadsheet (format CSV)
- Menggunakan library pandas untuk manipulasi data dan mendukung dua algoritma pencarian
- Pencarian dapat dilakukan berdasarkan judul paper, tahun terbit, atau nama penulis.
---

## Daftar File

- `tempCodeRunnerFile.py`  
  Program utama untuk pencarian data paper menggunakan Linear Search dan Binary Search.
---

## Sumber Data
```
https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/edit?gid=743838712#gid=743838712
```
---

## Persyaratan Sistem
- Python 3.6 atau lebih baru
- Library pandas (pip install pandas)
- Koneksi internet untuk mengakses Google Sheets
- Terminal atau Command Prompt untuk menjalankan program. Bisa juga menggunakan terminal bawaan text editor seperti Visual Studio Code
---

## Instruksi Penggunaan
#### Persiapan:
1. Pastikan Python dan library pandas sudah terinstal
2. Pastikan koneksi internet tersedia
3. Simpan kode sumber ke file bernama tempCodeRunnerFile.py

#### Menjalankan Program
4. Buka Terminal atau Command Prompt
5. Navigasi ke direktori tempat file tempCodeRunnerFile.py disimpan
6. Jalankan program dengan perintah: `python tempCodeRunnerFile.py`

#### Menggunakan Program
7. Program akan memuat data dari Google Sheets yang telah dikonfigurasi
8. Pilih kolom untuk pencarian (Judul Paper, Tahun Terbit, atau Nama Penulis)
9. Masukkan kata kunci pencarian
10. Pilih metode pencarian (Linear Search atau Binary Search)
11. Tinjau hasil pencarian yang ditampilkan
12. Tekan Enter untuk melakukan pencarian baru atau ketik 'q' untuk keluar
---

## Penjelasan Program:
### 1. Konfigurasi
```python
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
```
Bagian ini mendefinisikan:
- URL Google Sheets yang akan diakses (dalam format CSV)
- Baris yang digunakan sebagai header (indeks 0, baris pertama)
- Daftar kolom yang akan diambil dan ditampilkan
- Konstanta untuk nama kolom yang digunakan dalam pencarian
---

### 2. clear_screen()
```python
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```
Penjelasan:
- Fungsi ini membersihkan layar terminal untuk antarmuka yang lebih bersih
- Menggunakan perintah cls pada Windows atau clear pada Unix/Linux/macOS
- Perintah sistem dipilih berdasarkan nilai os.name yang mendeteksi sistem operasi
---

### 3. load_data_from_csv()
```python
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
```
Penjelasan:
- Mengambil data dari URL Google Sheets yang diberikan dalam format CSV menggunakan pandas
- Membersihkan nama kolom (lowercase, mengganti spasi dengan underscore, menghapus karakter non-alfanumerik)
- Mengkonversi DataFrame pandas ke list of dictionaries dengan to_dict(orient='records')
- Menampilkan jumlah baris data yang berhasil diambil dengan emoji
- Mengembalikan data dalam format list of dictionaries
---

### 4. sequential_search()
```python
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
```
Penjelasan:
- Implementasi algoritma pencarian linear (sequential search)
- Membersihkan kata kunci pencarian (lowercase dan hapus whitespace)
- Memeriksa apakah kata kunci kosong dan mengembalikan list kosong jika benar
- Melakukan pencarian berdasarkan tipe kolom:
  - Untuk kolom tahun (COL_TAHUN): Mengkonversi kata kunci ke float dan melakukan perbandingan nilai yang sama persis
  - Untuk kolom teks (judul dan penulis): Melakukan pencarian substring (jika kata kunci terdapat dalam nilai kolom)
- Mengembalikan daftar item yang cocok dengan kriteria pencarian
---

### 5. dichotomous_search()
```python
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
```
Penjelasan:
- Implementasi pencarian dikotomis (binary search) dengan pendekatan exact match
- Bekerja pada data yang sudah diurutkan (sorted_data)
- Untuk kolom tahun: Mencari nilai tahun yang sama persis setelah konversi ke float
- Untuk kolom teks: Mencari string yang sama persis (case-insensitive)
- Mengembalikan daftar item yang cocok dengan kriteria pencarian
---

### 6. display_result()
```python
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
```
Penjelasan:
- Menampilkan hasil pencarian dengan format yang mudah dibaca dan dengan emoji
- Memformat nama kolom untuk tampilan yang lebih baik (mengubah underscore menjadi spasi, capitalized)
- Memberikan tampilan khusus untuk abstrak dan kesimpulan dengan emoji dan format yang lebih jelas
- Menggunakan indentasi dan garis pembatas untuk meningkatkan keterbacaan
---

### 7. Blok if __name__ == "__main__":
```python
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
```
Penjelasan:
- Entry point utama program dengan antarmuka berbasis menu
- Mengambil data dari Google Sheets di awal program
- Menampilkan menu interaktif dengan emoji untuk memilih kolom pencarian
- Memproses pilihan pengguna untuk kolom dan metode pencarian
- Melakukan pengurutan data sesuai kebutuhan sebelum pencarian biner
- Menampilkan hasil pencarian dengan format yang jelas
- Mengulang proses pencarian hingga pengguna memilih keluar
- Menggunakan emoji dan format yang jelas untuk antarmuka pengguna yang lebih menarik
---

## Tentang Projek Ini:

Projek UTS Struktur Data  
Universitas Sultan Ageng Tirtayasa  
Oleh: Ananta Galih Mahardika [3337240055]  
Dosen: Cakra Adipura Wicaksana, S.T., M.T
