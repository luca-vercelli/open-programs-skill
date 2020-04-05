from mycroft import MycroftSkill, intent_file_handler

import subprocess

class OpenPrograms(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    SEARCH_ENGINE="http://www.duckduckgo.com"
    @intent_file_handler('programs.open.intent')
    def handle_programs_open(self, message):
        """
        This whould work with a few programs, such as Firefox and Thunderbird
        """
        program_name = message.data.get('programname')
        try:
            subprocess.run([program_name])
            self.speak_dialog('programs.open', {'programname' : program_name})
        except:
            self.speak_dialog('programs.open.notfound', {'programname' : program_name})

    @intent_file_handler('programs.open.browser.intent')
    def handle_programs_open(self, message):
        subprocess.run(["xdg-open", SEARCH_ENGINE], check=True)
        self.speak_dialog('programs.open')

    def stop():
        # should close active program ?!?
        pass

def create_skill():
    return OpenPrograms()

