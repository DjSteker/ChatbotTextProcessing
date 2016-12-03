# ChatbotTextProcessing
Text processing for chatbot IA lab implementation

__Team members__: Pricop Ovidiu, Butnaru Adrian, Ciuc Tiberiu, Ciubotariu Alexandru, Dorneanu Cristian, Lucian Alexandru, Rusu Alexandru, Buruiana Sebastian

# Chatbot inter-module interactions overview:
1. Chatbot receives user raw input as string
2. Raw input is proofread (corrected), processed and translated into an xml tree that gets annotated with metadata
3. Constructed xml tree is semantically interpreted and a response is designed
4. Response is processed and sent back to user as a string

# Text processing roadmap

## 1. Use __nltk__ for constructing a sintactic tree

## 2. Proofread input (error correction):
* each word in sentence will be verified with a dictionary
* if word not found in dictionary -> search word in knowledge base as proper noun
* [Optional] verify that sentence contains at least one verb (otherwise it wouldn't be a sentence)

## 3. Annotate words in sentence
* if proper noun -> annotate word with its definition
* if special construct (calendaristic date, math expression, etc.) -> annotate with its type -> needs predefined types
* if plain text word -> annotate word with its synonims

## 4. Knowledge base communication interface (Uses HTTP requests):
The following communication schema (request-response) serves for text annotation purposes. This way, in the text-processing phase, we are able to annotate proper nouns in user input with their most recent, on-demand crawled data from the world wide web.
  * Request Schema 
  ```javascript
  {
    "title": "Get Proper Noun Definition Request",
    "type": "object",
    "required": [ 
      "word"
    ],
    "properties": {
      "word": {
        "type": "string"
      }
    }
  }
  ```
  
  * Response Schema
  ```javascript
  {
    "title": "Get Proper Noun Definition Response",
    "type": "object",
    "required": [ 
      "shortDefinition", "definitionSource", "eror"
    ],
    "properties": {
      "shortDefinition": {
        "description": "A short definition of the supplied proper noun",
        "type": "string"
      },
      "definitionSource": {
        "description": "The source of the definition, may be a link or a book w. author et. al.",
        "type": "string"
      },
      "error": {
        "type": "boolean"
      },
      "errorMessage": {
        "type": "string"
      },
      "errorId": {
        "type": "integer"
      }
    }
  }
  ```

## 5. Artifficial intelligence communication interface (Uses HTTP requests):
The following communication schema (request-response) will be used by the text-processing module to invoke the AI module and get the chatbot's response to the annotated user input.

  * Request Schema 
  ```javascript
  {
    "title": "Get chatbot computed response Request",
    "type": "object",
    "required": [ 
      "inputData"
    ],
    "properties": {
      "inputData": {
        "type": "string",
        "description": "An xml document with the pre-processed, proofread and annotated user raw input string"
      }
    }
  }
  ```
  
  * Response Schema
  ```javascript
  {
    "title": "Get chatbot computed response Response",
    "type": "object",
    "required": [ 
      "content", "eror"
    ],
    "properties": {
      "content": {
        "description": "A string representing the computed response of the chatbot, using the developed AI",
        "type": "string"
      }
      "error": {
        "type": "boolean"
      },
      "errorMessage": {
        "type": "string"
      },
      "errorId": {
        "type": "integer"
      }
    }
  }
  ```
  
## 6. Artifficial intelligence output post-processing (Uses HTTP requests):
A string will be received from the AI module as the bot's response to the user-supplied input. This string needs to be parsed, corrected (and annotated). [this section needs more information]
