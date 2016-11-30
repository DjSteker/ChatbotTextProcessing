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
1. Define Words by checking them with a dictionary: 
  * Request Schema
  ```javascript
  {
    "title": "Define Word Request",
    "type": "object",
    "required": [ 
      "word", "partOfSpeech"
    ],
    "properties": {
      "word": {
        "type": "string"
      },
      "partOfSpeech": {
        "type": "string",
        "oneOf" : [
          "noun", "pronoun", "verb", "adjective", "adverb", "preposition", "conjunction", "interjection"
        ]
      }
    }
  }
  ```
  * Response Schema
  ```javascript
  {
    "title": "Define Word Response",
    "type": "object",
    "required": [ 
      "isValidWord", "wordDefinitions", "error"
    ],
    "properties": {
      "isValidWord": {
        "type": "boolean"
      },
      "wordDefinitions": {
        "type": "array",
        "items": { 
          "type": "string" 
        },
        "description": "The definitions found in an explicative dictionary for the supplied word"
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
  
2. Get word synonyms:
  * Request Schema
  ```javascript
  {
    "title": "Get Word Synonyms Request",
    "type": "object",
    "required": [ 
      "word", "partOfSpeech"
    ],
    "properties": {
      "word": {
        "type": "string"
      },
      "partOfSpeech": {
        "type": "string",
        "oneOf" : [
          "noun", "pronoun", "verb", "adjective", "adverb", "preposition", "conjunction", "interjection"
        ]
      }
    }
  }
  ```
  * Response Schema
  ```javascript
  {
    "title": "Get Word Synonyms Response",
    "type": "object",
    "required": [ 
      "wordSynonyms", "error"
    ],
    "properties": {
      "wordSynonyms": {
        "type": "array",
        "items": { 
          "type": "string" 
        },
        "description": "A list of synonyms of the part-of-speech of the supplied word"
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

3. Define a propor noun:
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
        "description": "[TODO talk to IA guys], maybe an xml",
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
* [TODO talk to IA guys]
