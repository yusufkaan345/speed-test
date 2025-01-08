import time
from multiprocessing import Process
from speedtest_module import perform_speedtest
from file_handler import save_results_to_file
from dashboard.start_dashboard import start_dashboard
from email_handler import EmailNotifier
import os

def run_speedtests(output_file, email_notifier):
    """
    Saatlik hız testi çalıştırma fonksiyonu.
    """
    SPEED_THRESHOLD = 15  # Mbps cinsinden minimum hız limiti
    
    try:
        while True:
            print("\n--- Starting a new speed test ---")
            results = perform_speedtest()
            save_results_to_file(results, output_file)
            
            # Hız kontrolü ve e-posta bildirimi
            if results['download'] < SPEED_THRESHOLD * 1_000_000:  # Convert to bits/s
                if email_notifier.send_speed_alert(results):
                    print(f"Speed alert email sent! Current speed: {results['download'] / 1_000_000:.2f} Mbps")
                
            print("Waiting for the next test...")
            time.sleep(7200)  # 2 saat bekleme
            
    except KeyboardInterrupt:
        print("\nSpeed test monitoring stopped by the user.")

def setup_environment():
    """E-posta yapılandırmasını başlat ve EmailNotifier nesnesini döndür"""
    email_notifier = EmailNotifier()
    # EmailNotifier sınıfı otomatik olarak .env dosyasını oluşturacak
    return email_notifier

if __name__ == "__main__":
    output_file = 'speedtest_results.json'

    # Önce e-posta yapılandırmasını yap
    print("Setting up email configuration...")
    email_notifier = setup_environment()

    # Dashboard'u ayrı bir işlem olarak çalıştır
    dashboard_process = Process(target=start_dashboard)
    dashboard_process.start()

    try:
        # Hız testlerini çalıştır
        run_speedtests(output_file, email_notifier)
    finally:
        # Dashboard işlemini güvenli bir şekilde durdur
        print("\nShutting down dashboard...")
        dashboard_process.terminate()
        dashboard_process.join()
