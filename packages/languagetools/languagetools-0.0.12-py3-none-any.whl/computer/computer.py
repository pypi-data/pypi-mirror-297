import json

from .ai.ai import Ai
from .browser.browser import Browser
from .calendar.calendar import Calendar
from .clipboard.clipboard import Clipboard
from .contacts.contacts import Contacts
from .display.display import Display
from .docs.docs import Docs
from .files.files import Files
from .keyboard.keyboard import Keyboard
from .mail.mail import Mail
from .mouse.mouse import Mouse
from .os.os import Os
from .skills.skills import Skills
from .sms.sms import SMS
from .vision.vision import Vision

class Computer:
    def __init__(self):

        self.offline = False
        self.verbose = False
        self.debug = False

        self.mouse = Mouse(self)
        self.keyboard = Keyboard(self)
        self.display = Display(self)
        self.clipboard = Clipboard(self)
        self.mail = Mail(self)
        self.sms = SMS(self)
        self.calendar = Calendar(self)
        self.contacts = Contacts(self)
        self.browser = Browser(self)
        self.os = Os(self)
        self.vision = Vision(self)
        self.skills = Skills(self)
        self.docs = Docs(self)
        self.ai = Ai(self)
        self.files = Files(self)

        self.emit_images = True
        self.save_skills = True

        self.import_computer_api = False  # Defaults to false
        self._has_imported_computer_api = False  # Because we only want to do this once

        self.import_skills = False
        self._has_imported_skills = False

    @property
    def api_base(self):
        import os
        return os.environ.get('INTERPRETER_API_BASE', 'https://oi-new-api.fly.dev/v0')

    @property
    def api_key(self):
        import os
        return os.environ.get('INTERPRETER_API_KEY')

    def screenshot(self, *args, **kwargs):
        """
        Shortcut for computer.display.screenshot
        """
        return self.display.screenshot(*args, **kwargs)

    def view(self, *args, **kwargs):
        """
        Shortcut for computer.display.screenshot
        """
        return self.display.screenshot(*args, **kwargs)

    def to_dict(self):
        def json_serializable(obj):
            try:
                json.dumps(obj)
                return True
            except:
                return False

        return {k: v for k, v in self.__dict__.items() if json_serializable(v)}

    def load_dict(self, data_dict):
        for key, value in data_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
