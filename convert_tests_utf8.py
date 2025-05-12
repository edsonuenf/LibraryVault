import os

def convert_to_utf8(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Se não estiver em utf-8, tenta abrir em latin1 e salvar em utf-8
                    with open(file_path, 'r', encoding='latin1') as f:
                        content = f.read()
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Convertido para UTF-8: {file_path}")
                except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")

# Altere o caminho abaixo para o diretório onde estão seus testes, se necessário
convert_to_utf8('apps')
