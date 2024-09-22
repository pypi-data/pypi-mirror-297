import dataclasses
import json
import re

import loguru
from ruamel.yaml import YAML

from .settings import ConverterSettings


class TextBlazeToEspansoConverter:
    """
    Convert TextBlaze JSON file with snippets to an Espanso matches
    directory filled with YAML files named after TextBlaze directories
    """

    def __init__(self, settings: dataclasses.dataclass = ConverterSettings):
        self.settings = settings
        assert self.settings.textblaze_export_json_path
        assert self.settings.espanso_matches_path
        self.filenames = set()

    def convert(self):
        loguru.logger.debug(
            f"Creating {self.settings.snippets_matches_directory}"
        )
        self.settings.snippets_matches_directory.mkdir(
            parents=True, exist_ok=True
        )
        loguru.logger.debug(
            f"Opening TextBlaze snippets file "
            f"{self.settings.textblaze_export_json_path}"
        )
        snippets_dict = json.loads(
            open(self.settings.textblaze_export_json_path, "r").read()
        )
        for folder in snippets_dict.get(self.settings.folders_key):
            self._save_folders_as_espanso_matches(folder)

    @property
    def yaml_processor(self):
        yaml = YAML(typ="rt", pure=True)
        yaml.indent(mapping=2, sequence=4, offset=2)
        return yaml

    def _save_folders_as_espanso_matches(self, folder: dict):
        matches = {"matches": []}
        filename = (
            self._snake_cased(folder.get(self.settings.folder_name_key))
            + self.settings.espanso_file_extension
        )
        self.filenames.add(filename)
        for snippet in folder.get(self.settings.snippets_key):
            matches["matches"].append(
                {
                    "trigger": self._format_trigger(snippet),
                    "repl"
                    "ace": f"{snippet.get(self.settings.snippet_text_key)}",
                }
            )
        self.yaml_processor.dump(
            matches,
            open(self.settings.snippets_matches_directory / filename, "w"),
        )
        loguru.logger.debug(
            f"Saved {filename} to {self.settings.snippets_matches_directory}"
        )

    def _format_trigger(self, snippet):
        """
        I substitute the original symbol bc the escape symbol is typed in a
        single button on any keyboard layout. I prefer it to the espanso's
        default
        """
        return f"{snippet.get(self.settings.snippet_shortcut_key)}".replace(
            "/", self.settings.replacer_character
        )

    @staticmethod
    def _snake_cased(string, regex="([A-Z][a-z]+)", replacement=r"_\1"):
        return re.sub(regex, replacement, string).replace(" ", "_").lower()
