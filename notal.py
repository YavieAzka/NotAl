#!/usr/bin/env python3
import sys
import re
import ast
from io import StringIO

class NotalParser:
    def __init__(self):
        # Menyimpan tipe variabel yang dideklarasikan
        self.declared_variables = {}
        # Pemetaan kata kunci Notal ke Python
        self.keywords = {
            'tampilkan': 'print',
            'masukan': 'input',
            'jika': 'if',
            'maka': ':',
            'lainnya': 'else:',
            'ulangi': 'for',
            'selama': 'while',
            'fungsi': 'def',
            'kembalikan': 'return',
            'dan': 'and',
            'atau': 'or',
            'bukan': 'not',
            'benar': 'True',
            'salah': 'False'
        }
        
        # Tipe data Notal ke Python
        self.data_types = {
            'integer': 'int',
            'float': 'float',
            'string': 'str',
            'boolean': 'bool',
            'daftar': 'list'
        }
    
    def parse(self, notal_code):
        # Tambahkan import yang diperlukan
        python_code = "import math\n\n"
        
        # Tambahkan fungsi main otomatis
        python_code += "def main():\n"
        
        # Pisahkan kode berdasarkan baris
        lines = notal_code.strip().split('\n')
        
        # Indentasi default untuk kode dalam fungsi main
        base_indent_level = 1
        
        for line in lines:
            # Lewati baris kosong tapi pertahankan dalam output
            if not line.strip():
                python_code += "\n"
                continue
            processed_line = line.strip()

            # Abaikan struktur PROGRAM, kamus, dan algoritma
            if processed_line.startswith("PROGRAM"):
                continue  # Abaikan nama program
            elif processed_line == "KAMUS":
                continue  # Abaikan header kamus
            elif processed_line == "ALGORITMA":
                continue  # Abaikan header algoritma

            # Hitung indentasi dari spasi awal (4 spasi = 1 level)
            leading_spaces = len(line) - len(line.lstrip())
            indent_level = base_indent_level + (leading_spaces // 4)
            
            # Hapus spasi awal untuk pemrosesan
            processed_line = line.strip()
            
            # Proses komentar dengan kurung kurawal
            comment_match = re.search(r'{(.*?)}', processed_line)
            if comment_match:
                comment_text = comment_match.group(1)
                processed_line = re.sub(r'{.*?}', f'# {comment_text}', processed_line)
                if processed_line.strip() == f'# {comment_text}':
                    # Jika hanya komentar, tambahkan ke kode Python
                    python_code += "    " * indent_level + processed_line + "\n"
                    continue
            
            # Proses deklarasi variabel (format: var1, var2: tipe_data)
            var_declaration_match = re.match(r'^([a-zA-Z0-9_\s,]+):\s*([a-zA-Z]+)$', processed_line)
            if var_declaration_match:
                var_names = var_declaration_match.group(1).strip().split(',')
                data_type = var_declaration_match.group(2).strip()
                
                # Konversi ke tipe data Python jika ada dalam kamus
                python_type = self.data_types.get(data_type, data_type)
                
                # Simpan tipe variabel
                for var in var_names:
                    self.declared_variables[var.strip()] = python_type

                # Buat pernyataan Python untuk setiap variabel
                processed_line = "; ".join([f"{var.strip()} = None" for var in var_names])
                # Tambahkan komentar tipe data untuk referensi
                processed_line += f"  # Tipe: {python_type}"

            
            # Proses fungsi output
            if processed_line.startswith('output('):
                processed_line = re.sub(r'output\((.*)\)$', r'print(\1)', processed_line)
            
            # Proses penugasan (assignment) dengan simbol <-
            assignment_match = re.match(r'([a-zA-Z_]\w*)\s*<-\s*(.+)', processed_line)
            if assignment_match:
                var_name = assignment_match.group(1).strip()
                expression = assignment_match.group(2).strip()
                processed_line = f"{var_name} = {expression}"

            # Proses fungsi output (menangkap kutipan yang hilang)
            if processed_line.startswith('output('):
                processed_line = re.sub(r'output\((.*)\)$', r'print(\1)', processed_line)
            
            # Proses input() dari pengguna dengan konversi tipe data
            input_match = re.match(r'input\s*\(\s*([a-zA-Z_]\w*)(?:,\s*"([^"]*)")?\s*\)$', processed_line)
            if input_match:
                var_name = input_match.group(1).strip()
                prompt = input_match.group(2)

                # Ambil tipe variabel
                var_type = self.declared_variables.get(var_name, "str")

                # Tentukan fungsi konversi
                type_cast = {
                    "int": "int",
                    "float": "float",
                    "str": "str",
                    "bool": "bool"
                }.get(var_type, "str")

                # Bangun perintah input() dengan konversi tipe
                if prompt:
                    processed_line = f"{var_name} = {type_cast}(input(\"{prompt}\"))"
                else:
                    processed_line = f"{var_name} = {type_cast}(input())"

            # Proses kata kunci
            for notal_keyword, python_keyword in self.keywords.items():
                if notal_keyword in ['jika', 'selama', 'ulangi', 'fungsi'] and notal_keyword in processed_line:
                    processed_line = re.sub(r'\b' + notal_keyword + r'\b', python_keyword, processed_line)
                    if not processed_line.rstrip().endswith(':'):
                        processed_line = processed_line.rstrip() + ':'
                else:
                    processed_line = re.sub(r'\b' + notal_keyword + r'\b', python_keyword, processed_line)
            
            # Proses if statement dengan kondisi di dalam tanda ()
            if_match = re.match(r'^if\s*\(\s*(.+?)\s*\)\s*then$', processed_line)
            if if_match:
                condition = if_match.group(1).strip()
                condition = re.sub(r'(?<![<>!])=', '==', condition)
                processed_line = f"if {condition}:"

            # Proses else (harus berdiri sendiri di baris)
            elif processed_line == 'else':
                processed_line = "else:"

            # Proses struktur for loop khusus
            if 'for' in processed_line and 'dalam' in processed_line:
                processed_line = processed_line.replace('dalam', 'in')
            
            # Tambahkan indentasi yang sesuai
            if processed_line:
                python_code += "    " * indent_level + processed_line + "\n"
        
        # Tambahkan pemanggilan fungsi main di akhir
        python_code += "\nif __name__ == \"__main__\":\n    main()\n"
        
        return python_code

class NotalInterpreter:
    def __init__(self, debug=False):
        self.parser = NotalParser()
        self.debug = debug
    
    def run_code(self, notal_code):
        # Parse kode Notal menjadi Python
        python_code = self.parser.parse(notal_code)
        
        # Tampilkan kode Python hanya jika mode debug aktif
        if self.debug:
            print("=== Kode Python yang Dihasilkan ===")
            print(python_code)
            print("===================================")
        
        try:
            # Kompilasi kode Python
            compiled_code = compile(python_code, "<string>", "exec")
            
            # Eksekusi kode
            local_vars = {}
            exec(compiled_code, globals(), local_vars)
            
            return True, None
        except Exception as e:
            if self.debug:
                return False, str(e)
            else:
                # Dalam mode non-debug, kesalahan akan ditampilkan minimal
                return False, f"Error: {type(e).__name__}"
    
    def run_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                notal_code = f.read()
            
            success, error = self.run_code(notal_code)
            
            if not success and self.debug:
                print(f"Error: {error}")
                return False
            
            return True
        except FileNotFoundError:
            if self.debug:
                print(f"Error: File '{filename}' not found")
            return False

def main():
    # Periksa argumen command line
    if len(sys.argv) < 2:
        print("Usage: notal <filename.notal> [--debug]")
        return
    
    # Periksa jika mode debug diaktifkan
    debug_mode = "--debug" in sys.argv
    
    # Dapatkan nama file (argumen pertama yang bukan flag)
    filename = next((arg for arg in sys.argv[1:] if not arg.startswith("--")), None)
    
    if not filename:
        print("Error: No filename specified")
        return
    
    # Jalankan interpreter
    interpreter = NotalInterpreter(debug=debug_mode)
    interpreter.run_file(filename)

if __name__ == "__main__":
    main()