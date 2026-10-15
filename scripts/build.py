"""Copy only the website to the deployable dist directory."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
shutil.copytree(root / 'site', root / 'dist', dirs_exist_ok=True)
print('Static website ready in dist/')
