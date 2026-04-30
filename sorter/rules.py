import json
from pathlib import Path

class RuleEngine:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.rules = self.config.get('rules', {})
        self.destinations = self.config.get('destinations', {})

    def resolve_destination(self, file_path: str) -> Path:
        path_obj = Path(file_path)
        ext = path_obj.suffix.lower()
        filename = path_obj.stem.lower()

        # PASS 1: Strict Mode. Check rules that have KEYWORDS first.
        for category, criteria in self.rules.items():
            valid_exts = criteria.get("extensions", [])
            keywords = criteria.get("keywords", [])

            # Only process rules that actually require keywords in this first pass
            if keywords:
                if valid_exts and ext not in valid_exts:
                    continue
                if any(keyword.lower() in filename for keyword in keywords):
                    return Path(self.destinations.get(category, self.destinations['Others'])).expanduser()

        # PASS 2: General Mode. Check rules that only rely on EXTENSIONS.
        for category, criteria in self.rules.items():
            valid_exts = criteria.get("extensions", [])
            keywords = criteria.get("keywords", [])

            # Now process the broad rules (like your generic "Code" or "Images" folders)
            if not keywords:
                if valid_exts and ext in valid_exts:
                    return Path(self.destinations.get(category, self.destinations['Others'])).expanduser()

        # Fallback if nothing matches
        return Path(self.destinations.get('Others')).expanduser()

    # --- THESE WERE THE MISSING PIECES! ---
    @property
    def watch_dir(self) -> Path:
        return Path(self.config.get('watch_directory', 'C:/Users/LENOVO/Downloads')).expanduser()

    @property
    def settle_time(self) -> int:
        return self.config.get('settle_seconds', 3)