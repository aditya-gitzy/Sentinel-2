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

        for category, criteria in self.rules.items():
            valid_exts = criteria.get("extensions", [])
            keywords = criteria.get("keywords", [])

            # If extensions are defined and it doesn't match, skip to the next rule
            if valid_exts and ext not in valid_exts:
                continue

            # If keywords exist, the filename MUST contain at least one of them
            if keywords:
                if any(keyword.lower() in filename for keyword in keywords):
                    return Path(self.destinations.get(category, self.destinations['Others'])).expanduser()
            else:
                # If no keywords are needed, matching the extension is enough
                return Path(self.destinations.get(category, self.destinations['Others'])).expanduser()

        # Fallback if nothing matches
        return Path(self.destinations.get('Others')).expanduser()

    @property
    def watch_dir(self) -> Path:
        return Path(self.config.get('watch_directory', '~/Downloads')).expanduser()

    @property
    def settle_time(self) -> int:
        return self.config.get('settle_seconds', 3)