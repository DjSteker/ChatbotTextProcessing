from django.http import HttpResponse

from api.core import JsonGenerator
from api.errors import UnauthorizedError, UnsupportedHttpVerbError, ExpectedParametersNotSupplied, \
    NltkAcronymToPartOfSpeechError, NltkAnnotateSentenceError

TextJson = "application/json"


def index(request):
    if request.method != "GET":
        return unsupportedHttpVerb(request)

    response = HttpResponse(content_type=TextJson)
    response.status_code = 200
    response.write(JsonGenerator.buildApiV1VersionResponse())
    return response


def nltkAcronymToPartOfSpeech(request):
    if request.method != "GET":
        return unsupportedHttpVerb(request)

    expectedQueryParameters = ["acronym"]
    requestAcronym = request.GET.get("acronym")
    if requestAcronym is None:
        return urlParameterNotSupplied(request, expectedQueryParameters)

    try:
        response = HttpResponse(content_type=TextJson)
        response.status_code = 200
        response.write(JsonGenerator.buildNltkAcronymToPartOfSpeechResponse(requestAcronym))
        return response
    except Exception as e:
        return internalErrorResponse(
            request, JsonGenerator.buildErrorResponse(NltkAcronymToPartOfSpeechError(str(e))))


def nltkAnnotateSentence(request):
    if request.method != "GET":
        return unsupportedHttpVerb(request)

    expectedQueryParameters = ["sentence"]
    requestSentence = request.GET.get("sentence")
    if requestSentence is None:
        return urlParameterNotSupplied(request, expectedQueryParameters)

    try:
        response = HttpResponse(content_type=TextJson)
        response.status_code = 200
        response.write(JsonGenerator.buildNltkAnnotatedSentenceResponse(requestSentence))
        return response
    except Exception as e:
        return internalErrorResponse(
            request, JsonGenerator.buildErrorResponse(NltkAnnotateSentenceError(str(e))))


def unknownRoute(request):
    response = HttpResponse(content_type=TextJson)
    response.status_code = 404
    response.write(JsonGenerator.buildErrorResponse(UnauthorizedError()))
    return response


def unsupportedHttpVerb(request):
    response = HttpResponse(content_type=TextJson)
    response.status_code = 405
    response.write(JsonGenerator.buildErrorResponse(UnsupportedHttpVerbError()))
    return response


def urlParameterNotSupplied(request, expectedParameters):
    response = HttpResponse(content_type=TextJson)
    response.status_code = 400
    response.write(JsonGenerator.buildErrorResponse(ExpectedParametersNotSupplied(str(expectedParameters))))
    return response


def internalErrorResponse(request, errorAsJson):
    response = HttpResponse(content_type=TextJson)
    response.status_code = 400
    response.write(errorAsJson)
    return response
