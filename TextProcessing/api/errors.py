class ApiError:
    code = None
    message = None

    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message


class ExpectedParametersNotSupplied(ApiError):
    def __init__(self, parametersAsString):
        super().__init__(
            code=0,
            message="Expected the following query parameters but did not get them: " + parametersAsString + "."
        )


class UnauthorizedError(ApiError):
    def __init__(self):
        super().__init__(
            code=1,
            message="You are not authorized to access this resource."
        )


class UnsupportedHttpVerbError(ApiError):
    def __init__(self):
        super().__init__(
            code=2,
            message="The accessed resource does not supported the verb you used."
        )


class NltkAcronymToPartOfSpeechError(ApiError):
    def __init__(self, message):
        super().__init__(
            code=3,
            message=message
        )


class NltkAnnotateSentenceError(ApiError):
    def __init__(self, message):
        super().__init__(
            code=4,
            message=message
        )


class GenerateErrorMessageError(ApiError):
    def __init__(self, message):
        super().__init__(
            code=5,
            message=message
        )


class GenerateDetectLanguageError(ApiError):
    def __init__(self, message):
        super().__init__(
            code=6,
            message=message
        )
