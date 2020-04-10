from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context

import subprocess


class OpenPrograms(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        # in different language, the "well known programs" could be different!
        # you need 1 .voc file per each
        self.wnb = self.translate_list('well.known.binaries')
        def create_handler(binary):
            def _f(message):
                message.data['binary'] = binary
                self.log.info("HERE handler() binary=" + binary)
                self.handle_open_program(message)
            return _f
        for binary in self.wnb:
            intent = IntentBuilder('open-' + binary) \
                               .require('open') \
                               .require('bin.' + binary) \
                               .build()  # search for bin.<binary>.voc  (does it?)
            self.register_intent(intent, create_handler(binary))


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
        subprocess.run(["gtk-launch", desktop_file])            # FIXME this is GNOME-specific
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
        app = desktop_file[:-8]                        # FIXME this is not always true
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
        # TODO alternative program?

############# Common programs ######################################################

    @intent_file_handler('open.binary.intent')
    def handle_open_program(self, message):
        """
        This whould work with a few programs, such as Firefox, Thunderbird, VLC
        The same handler should work for opening documents too! xdg-open is the same
        """
        self.log.info("HERE handle_open_program()")
        binary = message.data.get('binary')
        self.log.info("binary=" + str(message.data))
        self.open_binary_then_speak(binary)

    @intent_file_handler('open.browser.intent')
    def handle_open_browser(self, message):
        search_engine = self.settings.get('search_engine', "https://duckduckgo.com")
        self.open_url_then_speak(search_engine)

    @intent_file_handler('open.wordprocessor.intent')
    def handle_open_word(self, message):
        self.open_app_for_mimetype_then_speak("application/msword")

    @intent_file_handler('open.spreadsheet.intent')
    def handle_open_word(self, message):
        self.open_app_for_mimetype_then_speak("application/msexcel")

    @intent_file_handler('open.editor.intent')
    def handle_open_editor(self, message):
        self.open_app_for_mimetype_then_speak("text/plain")

    @intent_file_handler('open.imageprocessor.intent')
    def handle_open_word(self, message):
        self.open_binary_then_speak("gimp")		# FIXME too specific

    @intent_file_handler('open.audioprocessor.intent')
    def handle_open_word(self, message):
        self.open_binary_then_speak("audacity")		# FIXME too specific

    @intent_file_handler('open.calculator.intent')
    def handle_open_calculator(self, message):
        self.open_binary_then_speak("gnome-calculator")		# FIXME too specific


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

    def converse(self, utterance, lang):
        self.log.info("HERE converse() lang="+str(lang))
        # TODO should check if utterance matches "open xxx", and if
        # either xxx is an installed binary or is a well known program
        # if not, return False
        return False

def create_skill():
    return OpenPrograms()

