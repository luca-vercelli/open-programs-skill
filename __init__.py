from mycroft import MycroftSkill, intent_file_handler

import subprocess

SEARCH_ENGINE = "http://www.duckduckgo.com"

class OpenPrograms(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        pass

    @intent_file_handler('programs.open.intent')
    def handle_programs_open(self, message):
        """
        This whould work with a few programs, such as Firefox and Thunderbird
        """
        name = message.data.get('program')
        try:
            subprocess.run([program])
            self.speak_dialog('programs.open', {'program' : program})
        except:
            self.speak_dialog('programs.open.notfound', {'program' : program})

    @intent_file_handler('programs.open.browser.intent')
    def handle_programs_open(self, message):
        search_engine = self.settings.get('search_engine', "http://www.duckduckgo.com")
        subprocess.run(["xdg-open", search_engine], check=True)
        self.speak_dialog('programs.open')

    def stop(self):
        # should close active program ?!?
        pass

def create_skill():
    return OpenPrograms()

