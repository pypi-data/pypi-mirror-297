import os
import pathlib

from dataclasses import dataclass


@dataclass
class ConverterSettings:
    textblaze_export_json_path: pathlib.Path | os.PathLike = os.environ.get(
        "TEXTBLAZE_EXPORT_JSON_PATH"
    )
    espanso_matches_path: pathlib.Path | os.PathLike = os.environ.get(
        "ESPANSO_MATCHES_PATH"
    )
    snippets_directory_name: pathlib.Path | os.PathLike = os.environ.get(
        "SNIPPETS_DIRECTORY_NAME", pathlib.Path("test_version")
    )
    assert isinstance(
        textblaze_export_json_path,
        (pathlib.Path, os.PathLike, str),
    ), type(textblaze_export_json_path)
    assert isinstance(
        espanso_matches_path,
        (pathlib.Path, os.PathLike, str),
    ), type(espanso_matches_path)
    snippets_matches_directory = espanso_matches_path / snippets_directory_name
    folders_key = os.environ.get("FOLDERS_KEY", "folders")
    folder_name_key = os.environ.get("FOLDER_NAME_KEY", "name")
    snippets_key = os.environ.get("SNIPPETS_KEY", "snippets")
    snippet_shortcut_key = os.environ.get("SNIPPET_SHORTCUT_KEY", "shortcut")
    snippet_text_key = os.environ.get("SNIPPET_TEXT_KEY", "text")
    espanso_file_extension = os.environ.get("ESPANSO_FILE_EXTENSION", ".yml")
    replacer_character = os.environ.get("REPLACER_CHARACTER", "\\")
