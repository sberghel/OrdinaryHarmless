import appdirs
import json
import os

SETTINGS_FILE = 'settings.json'
APP_NAME = 'OnTheWay'
APP_AUTHOR = 'OrdinaryHarmless'

class Settings:
    def __init__(self, journal_dir, edsm_key):
        self.journal_dir = journal_dir
        self.edsm_key = edsm_key
        return self

    def to_json_str(self):
        d = {'journal_dir': self.journal_dir,
                'edsm_key': self.edsm_key}
        return json.dumps(d)

    @classmethod
    def from_json(cls, json_str):
        d = json.loads(json_str)
        try:
            journal_dir = d['journal_dir']
        except KeyError:
            journal_dir = ''
        try:
            edsm_key = d['edsm_key']
        except KeyError:
            edsm_key = ''
        return cls(journal_dir, edsm_key)



def get_settings():
    user_data_dir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(user_data_dir, exist_ok=True)
    settings_filename = os.path.join(user_data_dir, SETTINGS_FILE)
    try:
        s = _read_settings(settings_filename)
    except FileNotFoundError:
        s = _create_settings(settings_filename)
    if s.journal_dir is None:
        s.journal_dir = _get_journal_dir()
    if s.edsm_key is None:
        s.edsm_key = _get_edsm_key()
    _save_settings(settings, settings_filename)
    return s

def _read_settings(settings_filename):
    with open(settings_filename) as f:
        return Settings.from_json('\n'.join(f.readlines()))

def _create_settings(settings_filename):
    journal_dir = _get_journal_dir()
    edsm_key = _get_edsm_key()
    s = Settings(journal_dir, edsm_key)
    _save_settings(s, settings_filename)
    return s

def _save_settings(settings, settings_filename):
    with open(settings_filename, mode='w') as f:
        f.write(s.to_json_str)

# This is split into its own function just in case I want to change it later
def _get_journal_dir():
    journal_dir = os.path.expanduser(
            os.path.join("~",
                "Saved Games",
                "Frontier Developments",
                "Elite Dangerous")
            )
    return journal_dir

# This is split into its own function because this is not its optimal form.
# I mean, look at it. I'm somewhat ashamed.
def _get_edsm_key():
    edsm_key = input("Copy your EDSM key here: ")
    return edsm_key
