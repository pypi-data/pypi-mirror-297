A simple script to convert TextBlaze snippets to Espanso matches.

Oriented for the conversion of the whole TextBlaze repository at once using the "Export all folders" button in the
settings. Will work just as fine with a single folder.

I use `\` as a shortcut initiator because I think it is more convenient to access the shortcuts in a single button no
matter the keyboard layout.

### Prerequisites
- Python 3.12
- pip

### Installation
- `pip install textblaze-to-espanso`

### Environment variables
- `TEXTBLAZE_EXPORT_JSON_PATH`: path to TextBlaze export json
- `ESPANSO_MATCHES_PATH`: espanso/match directory path
- `SNIPPETS_DIRECTORY_NAME="test_version"`: Name of the directory where new matches will be stored
- `REPLACER_CHARACTER="\\"`: The character that will replace the original `/`. I prefer backslash
- `FOLDERS_KEY="folders"`: TextBlaze json key containing folders with snippets
- `FOLDER_NAME_KEY="name"`: TextBlaze Folder name json key
- `SNIPPETS_KEY="snippets"`:  TextBlaze snippets json key
- `SNIPPET_SHORTCUT_KEY="shortcut"`: TextBlaze shortcut json key
- `SNIPPET_TEXT_KEY="text" `: TextBlaze text snippet json key
- `ESPANSO_FILE_EXTENSION=".yml"`: Espanso configuration file extension

### Usage

1. Configure paths in environment
2. Execute the package: `python -m textblaze_to_espanso --env-file=$ENV_FILE_PATH`
3. Locate the matches inside the configured directory
4. Try to use your snippets. They should work in all environments from the get-go. You may need to reload Espanso
