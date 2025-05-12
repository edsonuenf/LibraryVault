import requests
import zipfile
import io
import os
import re
import sys
import shutil

def get_chrome_version():
    import subprocess
    try:
        output = subprocess.check_output(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version', shell=True)
        version = re.search(r"version\s+REG_SZ\s+([0-9.]+)", output.decode())
        if version:
            return version.group(1)
    except Exception as e:
        print("Não foi possível detectar a versão do Chrome automaticamente.")
    return None

def download_chromedriver(version=None):
    if not version:
        version = get_chrome_version()
        if not version:
            print("Informe a versão do Chrome instalada:")
            version = input("Versão do Chrome (ex: 124.0.6367.207): ").strip()
    major_version = version.split('.')[0]
    print(f"Detectado Chrome versão {version} (major: {major_version})")

    # Obter a versão exata do ChromeDriver para o major_version
    url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Não foi possível encontrar a versão do ChromeDriver para seu navegador.")
        sys.exit(1)
    chromedriver_version = response.text.strip()
    print(f"Baixando ChromeDriver versão {chromedriver_version}...")

    # Baixar o zip
    zip_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_win32.zip"
    r = requests.get(zip_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    print("ChromeDriver baixado e extraído na pasta atual.")

    # Opcional: mover para pasta do projeto ou System32
    dest = os.path.join(os.getcwd(), "chromedriver.exe")
    if os.path.exists(dest):
        print(f"ChromeDriver disponível em: {dest}")

if __name__ == "__main__":
    download_chromedriver()
