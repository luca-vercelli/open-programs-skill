from mycroft import MycroftSkill, intent_file_handler


class OpenPrograms(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('programs.open.intent')
    def handle_programs_open(self, message):
        self.speak_dialog('programs.open')


def create_skill():
    return OpenPrograms()

