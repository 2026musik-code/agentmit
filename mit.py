import os
import sys
import re
import subprocess
import time

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.prompt import Prompt
    from rich.table import Table
    from openai import OpenAI
except ImportError:
    print("Harap install dependencies terlebih dahulu: pip install rich openai")
    sys.exit(1)

console = Console()

# Konfigurasi API
API_KEY = "key"
BASE_URL = "https://autoapp.biz.id/v1"

# Setup Client
client = OpenAI(
    api_key=API_KEY, 
    base_url=BASE_URL,
    timeout=60.0, # Tambahkan timeout agar tidak hang/macet jika server lambat
    default_headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_logo():
    logo = """
 ██╗  ██╗██╗██████╗  ██████╗ 
 ██║ ██╔╝██║██╔══██╗██╔═══██╗
 █████╔╝ ██║██████╔╝██║   ██║
 ██╔═██╗ ██║██╔══██╗██║   ██║
 ██║  ██╗██║██║  ██║╚██████╔╝
 ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ 
    """
    console.print(Panel(
        Text(logo, style="bold cyan", justify="center"), 
        title="[bold magenta]KIRO AGENTIC[/bold magenta]", 
        subtitle="[bold yellow]Professional Edition[/bold yellow]",
        border_style="blue"
    ))

def select_model():
    console.print("\n[bold cyan]Sedang men-scan model AI aktif di server...[/bold cyan]")
    try:
        model_data = client.models.list().data
        models = sorted([m.id for m in model_data])
    except Exception as e:
        console.print(f"[bold red]Gagal mengambil model: {e}[/bold red]")
        models = [
            "kiro/claude-sonnet-4.5",
            "kiro/claude-haiku-4.5",
            "kiro/deepseek-3.2",
            "kiro/minimax-m2.5",
            "kiro/minimax-m2.1",
            "kiro/glm-5",
            "kiro/qwen3-coder-next",
            "kiro/auto",
            "kiro/claude-sonnet-4"
        ]
    
    models = models[:20]
    console.print("\n[bold green]=== MENU SCAN MODEL AI AKTIF ===[/bold green]")
    
    table = Table(show_header=False, show_edge=False, box=None, padding=(0, 2))
    for _ in range(4):
        table.add_column()
        
    for row in range(5):
        row_data = []
        for col in range(4):
            idx = row + col * 5
            if idx < len(models):
                row_data.append(f"[[bold cyan]{idx+1}[/bold cyan]] [green]✓[/green] {models[idx]}")
            else:
                row_data.append("")
        if any(row_data):
            table.add_row(*row_data)
            
    console.print(table)
    
    custom_idx = len(models) + 1
    console.print(f"[[bold cyan]{custom_idx}[/bold cyan]] Custom Model")
    
    choice = Prompt.ask(f"\n[bold yellow]Pilih Model Aktif (1-{custom_idx})[/bold yellow]", default="1")
    
    if choice == str(custom_idx):
        custom = Prompt.ask("[bold yellow]Masukkan nama custom model[/bold yellow]")
        return custom
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(models):
            return models[idx]
    except:
        pass
    
    return models[0]

def main():
    clear_screen()
    show_logo()
    
    active_model = select_model()
    
    clear_screen()
    show_logo()
    
    status_text = Text()
    status_text.append("Status: ", style="bold green")
    status_text.append("ONLINE\n", style="bold cyan")
    status_text.append("Model Aktif: ", style="bold green")
    status_text.append(f"{active_model}\n", style="bold yellow")
    status_text.append("Tujuan Utama: ", style="bold green")
    status_text.append("Koding, Analisa, Temuan, Cek Error", style="italic white")
    
    console.print(Panel(status_text, border_style="green"))
    console.print("[italic gray]Ketik 'exit' atau 'quit' untuk keluar.[/italic gray]\n")
    
    system_prompt = """Anda adalah Agentic AI profesional dengan AKSES PENUH ke terminal/sistem operasi.
Tujuan utama Anda:
- Koding (Programming)
- Analisa
- Temuan (Discovery/Research)
- Browsing (Gunakan kemampuan search/analisa web jika diperlukan)
- Cek Error (Debugging)

Instruksi Agen (PENTING):
1. Setiap diberikan tugas, Anda HARUS menyusun list/daftar rencana metode atau langkah-langkah penyelesaian.
2. Eksekusi metode tersebut satu per satu. Jangan mengeksekusi semua metode sekaligus jika tidak perlu.
3. Jika sebuah metode GAGAL, berikan tanda silang (❌) pada daftar Anda, catat alasan kegagalannya, lalu LANJUTKAN ke metode alternatif berikutnya di daftar Anda.
4. Jika metode BERHASIL, berikan tanda centang (✅). Jika sedang berjalan, beri tanda (⏳).
5. Selalu tampilkan update daftar metode ini di setiap respon Anda agar user mengetahui apa yang sudah dicoba, gagal, dan akan dilakukan selanjutnya.
6. Selesaikan setiap tugas/prompt secara tuntas dari awal hingga selesai. JANGAN MUDAH MENYERAH jika terjadi error.
7. Pastikan balasan Anda rapih, profesional, dan berwarna (gunakan format markdown dengan baik). Gunakan blok kode (```) untuk setiap baris kode atau log error.

PENTING - AKSES TERMINAL DAN BROWSING:
Anda MEMILIKI AKSES ke terminal lokal secara FULL/PENUH. Jangan pernah berkata bahwa Anda tidak memiliki akses. Anda bisa mensimulasikan error, mencari tahu penyebab gagal, dan menyelesaikan masalah yang dihadapi.
Anda juga bisa dan memiliki akses untuk menggunakan Chromium/Browser (misal via curl, wget, python requests, atau playwright/puppeteer jika diinstall) untuk web scraping, debugging web, dll.

Untuk menjalankan perintah di terminal, Anda HARUS menggunakan format XML berikut:

<function_calls>
<invoke name="antml:computer:execute_command">
<parameter name="command">PERINTAH ANDA DI SINI</parameter>
</invoke>
</function_calls>

Selalu gunakan format di atas jika Anda butuh berinteraksi dengan sistem, file, jaringan, atau membuka Chromium/Browser via CLI.
"""
    
    messages = [{"role": "system", "content": system_prompt}]
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold green]➜ Anda[/bold green]")
            if user_input.lower() in ['exit', 'quit']:
                console.print("[bold red]Mematikan Agen... Sampai jumpa![/bold red]")
                break
            
            if not user_input.strip():
                continue
                
            messages.append({"role": "user", "content": user_input})
            
            with console.status("[bold cyan]Agent sedang berpikir, mengeksekusi, dan menganalisa di latar belakang...[/bold cyan]", spinner="dots2"):
                while True:
                    # Membatasi "ingatan" AI (Sliding Window Context)
                    # Simpan prompt sistem (index 0) dan 15 percakapan/hasil eksekusi terakhir
                    if len(messages) > 15:
                        messages = [messages[0]] + messages[-14:]
                        
                    max_retries = 5
                    retry_count = 0
                    response = None
                    
                    while retry_count < max_retries:
                        try:
                            response = client.chat.completions.create(
                                model=active_model,
                                messages=messages,
                                timeout=30.0
                            )
                            break
                        except Exception as e:
                            retry_count += 1
                            console.print(f"[dim yellow]⚠ API sibuk/timeout (percobaan {retry_count}/{max_retries}). Mencoba ulang...[/dim yellow]")
                            time.sleep(2)
                            
                    if response is None:
                        break
                    
                    if isinstance(response, str):
                        reply = response
                    elif hasattr(response, 'choices') and len(response.choices) > 0:
                        reply = response.choices[0].message.content
                    elif isinstance(response, dict) and 'choices' in response:
                        reply = response['choices'][0]['message']['content']
                    else:
                        reply = str(response)
                    
                    # Remove <function_calls> tags completely
                    reply = re.sub(r'</?function_calls>', '', reply, flags=re.IGNORECASE)
                    
                    reply = re.sub(r'```[a-z]*\s*(?=<invoke)', '', reply, flags=re.IGNORECASE)
                    reply = re.sub(r'(</invoke>)\s*```', r'\1', reply, flags=re.IGNORECASE)
                    
                    messages.append({"role": "assistant", "content": reply})
                    
                    # Eksekusi tool/command jika ada
                    commands_to_run = re.findall(r'<invoke name="antml:computer:execute_command">\s*<parameter name="command">(.*?)</parameter>\s*</invoke>', reply, flags=re.DOTALL | re.IGNORECASE)
                    
                    if commands_to_run:
                        tool_outputs = ""
                        for cmd in commands_to_run:
                            cmd = cmd.strip()
                            console.print(f"[dim cyan]➔ Menjalankan perintah di latar belakang:[/dim cyan] [dim]{cmd}[/dim]")
                            try:
                                process = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
                                output = process.stdout + process.stderr
                                if not output.strip():
                                    output = "(Command completed with no output)"
                            except Exception as e:
                                output = f"Error executing command: {str(e)}"
                                
                            # Batasi panjang output agar tidak terlalu panjang (max 4000 char per output)
                            if len(output) > 4000:
                                output = output[:4000] + "\n... (output dipotong karena terlalu panjang)"
                                
                            tool_outputs += f"Command: {cmd}\nOutput:\n{output}\n\n"
                        
                        # Tambahkan output ke message lalu ulangi loop agar AI merespon
                        messages.append({"role": "user", "content": f"Berhasil menjalankan perintah di latar belakang. Berikut adalah outputnya (tolong analisa dan berikan ringkasan hasil kerja, atau lanjutkan langkah berikutnya jika diperlukan):\n\n<tool_response>\n{tool_outputs}\n</tool_response>"})
                    else:
                        # Jika tidak ada perintah, keluar dari loop AI
                        break
                        
            if response is None:
                console.print("[bold red]✖ Gagal mendapatkan respon setelah 5 kali percobaan. Silakan coba lagi.[/bold red]")
                continue
                
            # Rendering markdown yang rapih HANYA untuk hasil akhir
            console.print("\n")
            
            # Hilangkan XML tags jika tersisa di hasil akhir
            final_display = re.sub(r'<invoke.*?</invoke>', '', reply, flags=re.DOTALL | re.IGNORECASE)
            
            console.print(Panel(
                Markdown(final_display.strip()), 
                title="[bold magenta]KIRO AGENTIC - HASIL KERJA[/bold magenta]", 
                border_style="cyan",
                padding=(1, 2)
            ))
                    
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Sesi diakhiri oleh pengguna.[/bold red]")
            break
        except Exception as e:
            console.print(f"\n[bold red]✖ Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()
