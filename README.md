# 🌟 Utility for Translating Fluent Localization Dictionaries 📚

Managing and updating a vast array of languages efficiently!

## Features
- Seamlessly translate all your localizations using GPT.
- Translate either a specific dictionary or all dictionaries simultaneously with ease.

## How to Run
1. Install the package:


```bash
   # Using poetry
   poetry add git+https://github.com/Radim296/python_fluent_translator

   # Using pip
   pip install git+https://github.com/Radim296/python_fluent_translator
```


2. Run fluent_trans to automatically create the configuration file.

3. Edit the configuration file (fluent_translator.json):

```bash
    {
        # GPT model to use
        "gpt_model": "gpt-4-1106-preview",

        # Print logs in the console
        "logs": true,

        # Feature in development
        "use_cache": false,

        # By default, only new keys will be translated
        "update_all": false,

        # Number of keys to translate at a time
        "parallel_keys_translation_limit": 1,

        # Number of dictionaries to translate at a time
        "bulk_parallel_translation_limit": 1,

        # Keys to ignore during translation
        "ignored_keys": [
            "key_only_in_english"
        ],

        # Keys to translate exclusively
        "translate_only": [
        ],

        # OpenAI API token
        "gpt_token": "sk-################################################",

        # Information about your dictionaries
        "dictionaries": {
            "en": "en.ftl" // ISO 639-1 Language Code: path_to_dictionary
        }
    }
```

4. Run the Translator:

```bash
    # Translate all dictionaries:

    fluent_trans -a

    # Translate a specific dictionary:

    fluent_trans -c ru
```
