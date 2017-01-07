from langdetect import detect_langs

minThreshold = 0.7


def DetectLanguage(message):
    if message == '':
        return 'unk'
    langCoef = detect_langs(message)
    if len(langCoef) == 0:
        raise LanguageDetectionError("The language of the message could not be identified.")
    if langCoef[0].prob < minThreshold:
        raise LanguageDetectionError("The language of the message could not be identified.")
    return langCoef[0].lang


replies = {
    'af': "Ek praat nie Afrikaans nie. Gebruik asseblief Engels.",
    'ar': "'ana la 'atakallam alearabiati. yrja aistikhdam alllughat al'iinjaliziat.",
    'bg': "Az ne govorya bulgarski. Molya, izpolzvai?te anglii?ski.",
    'bn': "Ami banla balate pari na. Inreji byabahara karuna.",
    'ca': "No parlo català. Si us plau, utilitzeu anglès.",
    'cs': "Nemluvím cesky. Použijte anglictinu.",
    'cy': "Dydw i ddim yn siarad Cymraeg. Defnyddiwch Saesneg.",
    'da': "Jeg taler ikke dansk. Brug venligst engelsk.",
    'de': "Ich spreche kein Deutsch. Bitte verwende Englisch.",
    'el': "Den miló elliniká. Parakaloúme chrisimopoiíste Angliká.",
    'en': "",
    'es': "Yo no hablo español. Por favor usa inglés.",
    'et': "Ma ei räägi eesti keelt. Palun kasutage inglise keeles.",
    'fi': "En puhu suomea. Käytä Englanti.",
    'fr': "Je ne parle pas français. Veuillez utiliser l'anglais.",
    'gu': "Hu? gujarati nathi bolata. I?galisa upayoga karo.",
    'hi': "main hindee mein baat nahin karate. krpaya inglish istemaal karen.",
    'hr': "Ne govorim hrvatski. Molimo koristite engleski.",
    'hu': "Én nem beszélek magyarul. Használja angol.",
    'id': "Saya tidak berbicara bahasa Indonesia. Harap menggunakan bahasa Inggris.",
    'it': "Non parlo italiano. Si prega di usare l'inglese.",
    'ja': "Watashi wa nihongo o hanasemasen. Eigo o tsukatte kudasai.",
    'kn': "Nanu kanna?a matana?uvudilla. I?gli? ba?asi.",
    'ko': "naneun hangug-eoleul moshae. yeong-eoleul sayonghasibsio.",
    'lt': "Aš nekalbu lietuviškai. Prašome naudoti anglu kalba.",
    'lv': "Es nerunaju latviski. Ludzu, izmantojiet anglu.",
    'mk': "Jas ne zboruvam makedonski. Ve molime da go koristat angliskiot jazik.",
    'ml': "ñan malaya?a? sansarikkilla. i?gli? upayeagikkuka.",
    'mr': "Mi mara?hi bolata nahi. Kr?paya i?graji vapara.",
    'ne': "Ma nepali bolna chaina. A?greji prayoga garnuhos.",
    'nl': "Ik spreek geen Nederlands. Gebruik Engels.",
    'no': "Jeg snakker ikke norsk. Vennligst bruk engelsk.",
    'pa': "Mainu pajabi di gala na karade. Agarezi vica varata karo ji.",
    'pl': "Nie mówie po polsku. Prosze uzywac jezyka angielskiego.",
    'pt': "Eu não falo português. Por favor, use o inglês.",
    'ro': "Eu nu vorbesc române?te. Va rugam sa folosi?i limba engleza.",
    'ru': "YA ne govoryu po-russki. Pozhaluysta, ispol'zuyte angliyskiy yazyk.",
    'sk': "Nechcem hovorit slovenské. Použite anglictinu.",
    'sl': "Ne govorim slovensko. Prosimo, uporabite anglešcino.",
    'so': "Aanan u hadli Soomaali aadan. Fadlan isticmaal Ingiriisi.",
    'sq': "Unë nuk flas shqip. Ju lutem përdorni anglisht.",
    'sv': "Jag talar inte svenska. Använd engelska.",
    'sw': "Sizungumzi Kiswahili. Tafadhali kutumia lugha ya Kiingereza.",
    'ta': "Na? tami? peca mu?iyatu. A?kilam paya?pa?utta tayavu ceytu.",
    'te': "Nenu telugu ma?la?utaru ledu. Dayacesi i?gli? upayogin¯ca??i.",
    'th': "C¯h?n m?` phud p?has¯'a th?y kru?a chi^ p?has¯'a x?ngkvs¯'",
    'tr': "Türkçe bilmiyorum. Lütfen ingilizceyi kullan.",
    'uk': "YA ne hovoryu po-ukrayins'ky. Bud' laska, vykorystovuyte anhliys'ku movu.",
    'vi': "Tôi không nói du?c ti?ng Vi?t. Vui lòng s? d?ng ti?ng Anh.",
    'zh-cn': "Wo bù huì shuo zhongwén. Qing shiyòng yingyu.",
    'zh-tw': "Wo bù huì shuo zhongwén. Qing shiyòng yingyu."
}


def GenerateReply(language):
    if language in replies:
        return replies[language]
    raise LanguageIdentificationError("Sorry, we could not identify your language. Supported languages are: {l}."
                                      .format(l=list(replies.keys())))


class LanguageIdentificationError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(LanguageIdentificationError, self).__init__(message)
        self.message = message


class LanguageDetectionError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(LanguageDetectionError, self).__init__(message)
        self.message = message
