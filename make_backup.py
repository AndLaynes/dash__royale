import os
import zipfile
from datetime import datetime

def create_backup():
    # Setup paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(root_dir, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"dash_royale_backup_{timestamp}.zip"
    zip_path = os.path.join(backup_dir, zip_filename)
    
    print(f"Iniciando backup em: {zip_path}")
    
    # Files/Dirs to exclude
    EXCLUDE_DIRS = {'.git', '__pycache__', 'backups', 'venv', '.vscode', '.idea'}
    EXCLUDE_EXTS = {'.pyc'}
    
    file_count = 0
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                    continue
                    
                file_path = os.path.join(root, file)
                # Archive name relative to root
                arcname = os.path.relpath(file_path, root_dir)
                
                # Check if it's the zip file itself (just in case)
                if file_path == zip_path:
                    continue
                    
                zipf.write(file_path, arcname)
                file_count += 1
                
    print(f"Backup concluído com sucesso!")
    print(f"Arquivos arquivados: {file_count}")
    print(f"Local: {zip_path}")

if __name__ == "__main__":
    create_backup()
