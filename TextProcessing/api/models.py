class JsonApiDescription:
    version = "v1"
    lastUpdateDate = "Dec 14 2016"
    description = "Use this api for various text-processing purposes."

    jsonVersionField = "apiVersion"
    jsonLastUpdateDateField = "lastUpdateDate"
    jsonDescriptionField = "description"


class JsonAcronymToPartOfSpeech:
    acronym = "acronym"
    partOfSpeech = "partOfSpeech"
    examples = "examples"


class JsonAnnotatedSentence:
    annotatedSentence = "annotatedSentence"


class JsonError:
    errorField = "error"
    errorCodeField = "errorId"
    errorMessageField = "errorMessage"
