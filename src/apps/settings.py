from pathlib import Path

SRC_DIR = Path(__file__).parents[1].resolve()
INDEX_PATH = str(SRC_DIR / "views" / "index.html")
SCRIPTS_PATH = str(SRC_DIR / "views" / "scripts")
STYLES_PATH = str(SRC_DIR / "views" / "styles")
PAGES_PATH = str(SRC_DIR / "views" / "pages")
