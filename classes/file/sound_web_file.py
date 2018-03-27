from classes.file.web_file import WebFile
from utils import Lang


class SoundWebFile(WebFile):
    def __init__(self, lang, url):
        WebFile.__init__(self, 'audio', lang, url)


class SoundEngWebFile(SoundWebFile):
    def __init__(self, url):
        SoundWebFile.__init__(self, Lang.Eng, url)
