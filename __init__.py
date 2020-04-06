from mycroft import MycroftSkill, intent_file_handler

import subprocess

SEARCH_ENGINE = "http://www.duckduckgo.com"

class OpenPrograms(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        pass

    def _common_open_program(self, *programs_list):
        """
        Launch the first available program
        """
        if not programs_list:
            raise ValueError("Why an empty list here?!?")
        for program in programs_list:
            try:
                proc = subprocess.Popen(program.split(" "))
                self.log.info("Launched PID " + str(proc.pid))
                self.speak_dialog('programs.open', {'program' : program})
                return
            except FileNotFoundError:
                self.log.info("Not found: " + str(program))
                pass
        self.speak_dialog('programs.open.notfound', {'program' : programs_list[0]})
        # TODO maybe the user wants some program of the same kind...

    def _common_open_url(self, url):
        subprocess.run(["xdg-open", url], check=True)
        self.speak_dialog('programs.open')

############# Common programs ######################################################

    @intent_file_handler('programs.open.intent')
    def handle_open_program(self, message):
        """
        This whould work with a few programs, such as Firefox and Thunderbird
        """
        program = message.data.get('program')
        self._common_open_program(program)

    @intent_file_handler('programs.open.chrome.intent')
    def handle_open_chrome(self, message):
        """
        'Google Chrome' is not equal to its binary 'chromium'
        Moreover, there are two different binaries, either 'chrome' or 'chromium'
        """
        self._common_open_program("chromium", "chrome", "google-chrome")

    @intent_file_handler('programs.open.browser.intent')
    def handle_open_browser(self, message):
        search_engine = self.settings.get('search_engine', "https://duckduckgo.com")
        self._common_open_url(search_engine)

    @intent_file_handler('programs.open.wordprocessor.intent')
    def handle_open_word(self, message):
        # no way to use xdg-utils ? 
        self._common_open_program("oowriter", "libreoffice --writer", "abiword", "word")

############# Common websites... many more exist, unluckily... ####################

    @intent_file_handler('programs.open.google.intent')
    def handle_open_google(self, message):
        self._common_open_url("https://www.google.com")

    @intent_file_handler('programs.open.youtube.intent')
    def handle_open_youtube(self, message):
        self._common_open_url("https://www.youtube.com")

    @intent_file_handler('programs.open.duckduck.intent')
    def handle_open_duckduck(self, message):
        self._common_open_url("https://duckduckgo.com")

    @intent_file_handler('programs.open.stackoverflow.intent')
    def handle_open_stackoverflow(self, message):
        self._common_open_url("https://www.stackoverflow.com")

    @intent_file_handler('programs.open.mycrofthome.intent')
    def handle_open_mycroft_home(self, message):
        self._common_open_url("https://home.mycroft.ai")

################################################################################

    def stop(self):
        # should close active program ?!?
        pass

def create_skill():
    return OpenPrograms()

