from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context

import subprocess

SEARCH_ENGINE = "http://www.duckduckgo.com"

class OpenPrograms(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        pass

#    def load_programs_db(self):
#        filename = self.find_resource('programs', 'resources')
#        with open(filename) as f:
#            lines = f.readlines()
#        lines = [x[:-1] for x in lines]
#        lines = [x.split(':') for x in lines if x]
#        self.category_names = set(x[0] for x in lines)
#        self.categories = {x:[z[1] for z in lines if z[0]==x] for x in self.category_names}

#    def get_alt_programs(self, binary, category_name):
#        others = [x for x in self.categories[category_name] if x != binary]
#        return [x for x in others if self.is_program_installed(binary)]

############# Utility ######################################################

    def open_url(self, url):
        """
        Open given URL (using xdg-open)
        """
        subprocess.run(["xdg-open", url], check=True)

    def open_doc(self, document_path):
        """
        Open given document (using xdg-open)
        """
        subprocess.run(["xdg-open", document_path], check=True)

    def get_desktop_file_for_mimetype(self, mimetype):
        """
        Retrieve default app for given MIME type (using xdg-mime)
        """
        subprocess.run(["xdg-mime", "query", "default", mimetype], check=True)

    def open_app_for_mimetype(self, mimetype):
        """
        Retrieve default app for given MIME type (using get_desktop_file_for_mimetype),
        then launch it (using gtk-launch)
        Return desktop file
        """
        desktop_file = self.get_desktop_file_for_mimetype(mimetype)
        subprocess.run(["gtk-launch", desktop_file])			# FIXME this is GNOME-specific
        return desktop_file

    def open_binary(self, binary):
        """
        Open given binary (using subprocess.Popen).
        May rise FileNotFoundError.
        Return Popen object
        """
        proc = subprocess.Popen(binary.split(" "))
        self.log.info("Launched PID " + str(proc.pid))
        return proc

    def is_program_installed(self, binary):
        """
        Check if program is installed running binary --version (well not exactly the best)
        """
        try:
            subprocess.Popen(binary.split(" ") + ["--version"])
            return True
        except FileNotFoundError:
            return False

############# Common intents ######################################################

    def open_url_then_speak(self, url):
        self.open_url(url)
        self.speak_dialog('programs.open')

    def open_app_for_mimetype_then_speak(self, mimetype):
        desktop_file = self.open_app_for_mimetype(mimetype)
        app = desktop_file[:-8]						# FIXME this is not always true
        self.speak_dialog('programs.open', {'program' : app})
        # TODO app may be None

    def open_binary_then_speak(self, binary):
        try:
            self.open_binary(binary)
            self.speak_dialog('programs.open', {'program' : binary})
            return
        except FileNotFoundError:
            self.log.info("Not found: " + str(binary))
            self.speak_dialog('programs.open.notfound', {'program' : binary})
        except Exception as e:
            self.log.exception(e)
            self.speak_dialog('programs.open.error', {'program' : binary})
        # TODO alternative prorgram?

############# Common programs ######################################################

    @intent_file_handler('open.binary.intent')
#    @intent_handler(IntentBuilder('open')
#                   .require('open')
#                   .one_of('firefox','thunderbird', 'chrome', 'chromium'))
    def handle_open_program(self, message):
        """
        This whould work with a few programs, such as Firefox, Thunderbird, VLC
        """
        binary = message.data.get('binary')
        self.log.info("binary=" + str(message.data))
        self.open_binary_then_speak(binary)

#    @intent_file_handler('programs.open.chrome.intent')
    def handle_open_chrome(self, message):
        """
        'Google Chrome' is not equal to its binary 'chromium'
        Moreover, there are two different binaries, either 'chrome' or 'chromium'
        """
        self._common_open_program("chromium", "chrome", "google-chrome")

    @intent_file_handler('open.browser.intent')
    def handle_open_browser(self, message):
        search_engine = self.settings.get('search_engine', "https://duckduckgo.com")
        self.open_url_then_speak(search_engine)

    @intent_file_handler('open.wordprocessor.intent')
    def handle_open_word(self, message):
        self.open_app_for_mimetype_then_speak("application/msword")

############# Common websites... many more exist, unluckily... ####################

#    @intent_file_handler('programs.open.google.intent')
    def handle_open_google(self, message):
        self.open_url_then_speak("https://www.google.com")

#    @intent_file_handler('programs.open.youtube.intent')
    def handle_open_youtube(self, message):
        self.open_url_then_speak("https://www.youtube.com")

#    @intent_file_handler('programs.open.duckduck.intent')
    def handle_open_duckduck(self, message):
        self.open_url_then_speak("https://duckduckgo.com")

#    @intent_file_handler('programs.open.stackoverflow.intent')
    def handle_open_stackoverflow(self, message):
        self.open_url_then_speak("https://www.stackoverflow.com")

#    @intent_file_handler('programs.open.mycrofthome.intent')
    def handle_open_mycroft_home(self, message):
        self.open_url_then_speak("https://home.mycroft.ai")

################################################################################

    def stop(self):
        # should close active program ?!?
        pass

def create_skill():
    return OpenPrograms()

