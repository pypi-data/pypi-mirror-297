Semantic Comparison is a search algorithm that returns the most likely answer to a given instruction based on a history of instructions and responses.

# Semantic Comparison

This code is an algorithm projected, architected and developed by Sapiens Technology®️ and aims to save indexed conversations from language models for later consultation through semantic comparison using the prompts as a key to return the respective responses. This avoids unnecessary processing when an instruction has already been made previously by the same user, thus returning the already existing response to the same instruction without the need to process it again in the model. The algorithm also has the ability to adapt responses when instructions are similar but not completely the same, readjusting terms and words in general.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Perpetual Context.

```bash
pip install semantic-comparison
```

## Usage
Basic usage example:
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter.
summary_file = infinite_context.getSummaryTXT(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the txt file (accepts any file in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You will can use the constructor's "display_error_point" parameter to display or hide details of possible errors during execution.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext( # creation of the object for accessing class resources
    display_error_point=True # "True" to display error details if an error occurs, or "False" to display no error details
) # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter.
summary_file = infinite_context.getSummaryTXT(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the txt file (accepts any file in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryCode" function returns the summary of a programming code contained in a string respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to variables
file_path = './files/file_name.py' # address read file
max_tokens = 200000 # maximum number of tokens to be returned in the summary
# opens the file addressed in the "file_path" variable in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "text" which will be passed to the parameter of the same name in the code summary function
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file: text = file.read() # reading the text contained in the file
# code for generating summary of read content
# returns a summary of the code contained in the variable of the "text" parameter with a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryCode(text=text, max_tokens=max_tokens) # function call that will return the summary of the code (accepts any type of code in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryText" function returns the summary of a string respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# opens the file addressed in the "file_path" variable in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "text" which will be passed to the parameter of the same name in the text summary function
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file: text = file.read() # reading the text contained in the file
# code for generating summary of read content
# returns a summary of the string contained in the variable of the "text" parameter with a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryText(text=text, max_tokens=max_tokens) # function call that will return the summary of the string (accepts any string value)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryTXT" function returns the summary of a text file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryTXT(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the txt file (accepts any type of file in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryYouTube" function returns the summary of a YouTube video respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://www.youtube.com/watch?v=9iqn1HhFJ6c' # youtube video address
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the video contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryYouTube(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the video (only youtube videos)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryWEBPage" function returns the summary of a WEB Page respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://en.wikipedia.org/wiki/Artificial_intelligence' # address of a web page
max_tokens = 20000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the web page contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryWEBPage(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of web page
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryPDF" function returns the summary of a PDF file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pdf' # pdf file address
max_tokens = 8000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the pdf file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryPDF(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in pdf format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None, # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
    use_api=True, # "True" to try to use the image text extraction external API if one or more pages are images, or "False" to use local text extraction when necessary
    language=None # string with the acronym of the language that will be used to extract text from images when one or more pages are images, or "None" for slower default recognition that is more susceptible to errors
) # function call that will return the summary of pdf file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
Note that it is possible to define a main page with an integer referring to the page numbering in the "main_page" parameter, so the page in question will have a number of tokens in the summary greater than the number of tokens in the other pages. Also note that it is possible to previously define the language in which the file was written to facilitate recognition and increase the accuracy of the result.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pdf' # pdf file address
max_tokens = 8000 # maximum 8000 tokens in result string
main_page = 2 # page number 2 should have all the attention focused on it
use_api = True # activates the text extraction API if there are images in the file
language = 'en' # makes it clear that the text contained in the file is in english (will only be used if the API request fails and the text local detection algorithm is requested)
# code for generating summary of read content
# returns a string with the summary of the pdf file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryPDF(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in pdf format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=main_page # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
    use_api=use_api, # "True" to try to use the image text extraction external API if one or more pages are images, or "False" to use local text extraction when necessary
    language=language # string with the acronym of the language that will be used to extract text from images when one or more pages are images, or "None" for slower default recognition that is more susceptible to errors
) # function call that will return the summary of pdf file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
All file summary functions (of any type) will accept in the "file_path" parameter either a local file or a file at a web address.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://www.sjsu.edu/writingcenter/docs/handouts/Articles.pdf' # pdf file address
max_tokens = 1000 # maximum 1000 tokens in result string
main_page = 3 # page number 3 should have all the attention focused on it
use_api = False # disables the API for extracting text from images because the current file is not a scanned document
language = None # disables the language because it will not be necessary to extract text from images
# code for generating summary of read content
# returns a string with the summary of the pdf file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryPDF(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in pdf format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=main_page # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
    use_api=use_api, # "True" to try to use the image text extraction external API if one or more pages are images, or "False" to use local text extraction when necessary
    language=language # string with the acronym of the language that will be used to extract text from images when one or more pages are images, or "None" for slower default recognition that is more susceptible to errors ("None" can also be used if the document has not been scanned)
) # function call that will return the summary of pdf file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryWord" function returns the summary of a Microsoft Word file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.docx' # microsoft word file address
max_tokens = 1000 # maximum 1000 tokens in result string
characters_per_page = 3800 # defines that the file must be subdivided into pages with a maximum of 3800 characters
# code for generating summary of read content
# returns a string with the summary of the microsoft word file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryWord(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in docx format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None, # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
    characters_per_page=characters_per_page # approximate integer number of characters per page to subdivide the full text of the file into specific pages (the default value is 4000)
) # function call that will return the summary of microsoft word file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryPowerPoint" function returns the summary of a Microsoft Powerpoint file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pptx' # microsoft powerpoint file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the microsoft powerpoint file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryPowerPoint(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: pptx, ppsx, pptm)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None # integer with the number of the page/slide that should receive the most attention, or "None" to distribute attention equally
) # function call that will return the summary of microsoft powerpoint file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryCSV" function returns the summary of a CSV file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv' # csv file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the csv file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryCSV(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in csv format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    separator=None # string with the cell delimiter character used in the file to be read, or "None" so that recognition of the delimiter character is automatically done more slowly
) # function call that will return the summary of csv file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryExcel" function returns the summary of a Microsoft Excel file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.xlsx' # microsoft excel file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the microsoft excel file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryExcel(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in xlsx format)
    max_tokens=max_tokens # maximum tokens limit in result string
) # function call that will return the summary of microsoft excel file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryImage" function returns the summary of a image file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.jpg' # image file address
max_tokens = 4000 # maximum 4000 tokens in result string
use_api = True # will attempt to use the external API before performing objects and texts recognition locally
language = 'pt' # specifies that the text contained in the image is in portuguese
maximum_colors = 5 # will return a maximum of five of the most predominant colors in the image
# code for generating summary of read content
# returns a string with the summary of the image file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryImage(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: webp, jpg, jpeg, png, gif, bmp, dng, mpo, tif, tiff, pfm)
    max_tokens=max_tokens, # maximum tokens limit in result string
    use_api=use_api, # if "True" will attempt to detect objects and texts first with the external API before performing local detection, if "False" will perform local detection directly
    language=language, # string with the abbreviation of the language that will be used to detect texts in the image with local detection without the external API, or "None" if the external API is used instead of local detection (if the external API fails the request, local detection will be used automatically)
    maximum_colors=maximum_colors # maximum integer number of predominant colors to be detected in the image (always a positive integer)
) # function call that will return the summary of image file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryAudio" function returns the summary of a audio file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.wav' # audio file address
max_tokens = 4000 # maximum 4000 tokens in result string
language = 'en' # specifies that the audio is in the english language to make the transcription process faster and more accurate
# code for generating summary of read content
# returns a string with the summary of the audio file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryAudio(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: mp3, wav, mpeg, m4a, aac, ogg, flac, aiff, wma, ac3, amr)
    max_tokens=max_tokens, # maximum tokens limit in result string
    language=language # string with the audio language or "None" to try each of the possible languages ​​until you find one that is compatible
) # function call that will return the summary of audio file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryVideo" function returns the summary of a video file respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.mp4' # video file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the video file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryVideo(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: mp4, avi, mkv, mov, webm, flv, 3gp, wmv, ogv)
    max_tokens=max_tokens, # maximum tokens limit in result string
    use_api=True, # "True" to try to use the external API to recognize objects and texts in the video frames, or "False" to use only local recognition
    language=None, # string com a sigla do idioma que será usado na detecção local de textos nos frames do vídeo, ou "None" se a detecção de textos for feita com a API externa (it is recommended to set the language even with the API, because if the API fails the language will be necessary for correct local detection; here we use "None" just as an example)
    maximum_colors=3 # integer with the maximum value of predominant colors to be captured in the video frames (always a positive integer)
) # function call that will return the summary of video file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryFile" function returns the summary of any file accepted by the expert functions, respecting the tokens limit defined in the call.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pdf' # file address
max_tokens = 8000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = infinite_context.getSummaryFile( # accepts microsoft word files, powerpoint, excel, pdf documents, csv spreadsheets, text files, code files, youtube video addresses, web page addresses, images, audios and videos
    file_path=file_path, # address of a local file or a file on the web
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None, # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally (only for pdf, word and powerpoint files)
    characters_per_page=4000, # used for docx documents only; defines the maximum number of characters per page in the interpretation (always a positive integer; only for word files)
    separator=None, # only used for csv files; string with the cell delimiter character, or "None" so that the delimiter character is recognized automatically (only for csv files)
    use_api=True, # "True" to try to use the external API to detect objects and texts in images and videos, or "False" to use only local detection (only for image, video and pdf files)
    language=None, # string with the acronym of the language used to detect text in images and videos without an API, or for faster and more accurate transcription of audio files ("None" to automatically detect the language more slowly and less accurately; only for image, audio, video and pdf files)
    maximum_colors=3 # integer with the maximum number of predominant colors to be detected in images and videos (always a positive integer; only for image and video files)
) # function call that will return the summary of file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You can use the "existingPath" function to check whether a local or WEB path for a given file exists. Any file of any type can be recognized.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
existing_path = infinite_context.existingPath( # checks for a local address, or a web address
    file_path='./files/file_name.txt', # string with the local or web address to check
    show_message=False # if "True" will display a message warning about the non-existence of the address when it does not exist, if "False" no message will be displayed
) # returns "True" if the path exists or "False" if it does not
# function return check
if existing_path: print('The path exists.') # message to confirm the existence of the path
else: print('The path does NOT exist!') # message to warn that the verified path does not exist
```
```bash
The path does NOT exist!
```
Note that when we set the "show_message" parameter to "True" an alert message will be displayed when the path does not exist before the boolean is returned by the function.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
existing_path = infinite_context.existingPath( # checks for a local address, or a web address
    file_path='./files/file_name.txt', # string with the local or web address to check
    show_message=True # if "True" will display a message warning about the non-existence of the address when it does not exist, if "False" no message will be displayed
) # returns "True" if the path exists or "False" if it does not
# function return check
if existing_path: print('The path exists.') # message to confirm the existence of the path
else: print('The path does NOT exist!') # message to warn that the verified path does not exist
```
```bash
The path to the "./files/file_name.txt" file does not exist.
The path does NOT exist!
```
You can use the "getHashCode" function to obtain a string with a unique hash code generated based on the current date and time.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
hash_code = infinite_context.getHashCode() # This function does not receive any parameters, it just returns a string with a unique hash code that can be used as a file name for the user
print(hash_code) # displays the hash code that was returned by calling the above function
```
```bash
f27c60e2e1879a600c8ce14e216994caf8869a3d37b27f49f44b5b34319949e3
```
You can use the "getFileType" function to obtain the type of a file through its address. Any file of any type can be recognized.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
file_type = infinite_context.getFileType(file_path='./files/file_name.xlsx') # returns the type of file extension assigned to the string in "file_path"
print('The file is of type: '+file_type+'.') # displays the file type
```
```bash
The file is of type: xlsx.
```
You can use the "countTokens" function to count the tokens in a string.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
string = 'This is example text for counting tokens in a string.' # example text for tokens count
number_of_tokens = infinite_context.countTokens(string=string) # returns the number of tokens contained in the "string" parameter text
print(f'The "{string}" text has {number_of_tokens} tokens.') # displays the number of tokens
```
```bash
The "This is example text for counting tokens in a string." text has 11 tokens.
```
You can use the "getKeyWords" function to obtain a list of keywords contained in a string.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
string = 'Brazil was discovered in 1500.' # Example text for keywords recognition
keywords_list = infinite_context.getKeyWords(string=string) # returns the keywords contained in the "string" parameter text (the return will always be a list of strings)
print(f'The keywords contained in the text "{string}" are:', ', '.join(keywords_list)+'.') # displays the keywords
```
```bash
The keywords contained in the text "Brazil was discovered in 1500." are: brazil, discovered, 1500.
```
You can use the "getBeginningAndEnd" function to return only the beginning and end of a text based on the tokens limit.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# opens the file addressed in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "string" which will be passed to the parameter of the same name in the text summary function
with open('./files/file_name.txt', 'r', encoding='utf-8', errors='ignore') as file: string = file.read() # reading the string contained in the file
# code for generating summary of read content
# returns a summary with the start and end of the input string
summary_file = infinite_context.getBeginningAndEnd(
    string=string, # string with the text that will be summarized
    max_tokens=1000, # maximum number of tokens returned in result text
    separator='' # string that will be between the beginning and end of the summary (use an empty string so that the two parts are completely joined together)
) # function call that will return the summary of the string
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You can also assign a separator text between the beginning and end of the return from the "getBeginningAndEnd" function.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# opens the file addressed in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "string" which will be passed to the parameter of the same name in the text summary function
with open('./files/file_name.txt', 'r', encoding='utf-8', errors='ignore') as file: string = file.read() # reading the string contained in the file
# code for generating summary of read content
# returns a summary with the start and end of the input string
summary_file = infinite_context.getBeginningAndEnd(
    string=string, # string with the text that will be summarized
    max_tokens=1000, # maximum number of tokens returned in result text
    separator='\n...\n' # an ellipsis will be placed between the beginning and end of the summarized text
) # function call that will return the summary of the string
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You can use the "getBeginningMiddleAndEnd" function to return only the beginning, middle and end of a text based on the tokens limit.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# opens the file addressed in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "string" which will be passed to the parameter of the same name in the text summary function
with open('./files/file_name.txt', 'r', encoding='utf-8', errors='ignore') as file: string = file.read() # reading the string contained in the file
# code for generating summary of read content
# returns a summary with the beginning, middle and end of the input string
summary_file = infinite_context.getBeginningMiddleAndEnd(
    string=string, # string with the text that will be summarized
    max_tokens=1000, # maximum number of tokens returned in result text
    separator='\n...\n' # an ellipsis will be placed between the beginning and end of the summarized text (use an empty string so that the three parts are completely joined together)
) # function call that will return the summary of the string
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "imageToBase64" function returns a dictionary with the base-64 string of an image in the "base64_string" key and the image type in the "image_type" key.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
file_path = './files/file_name.png' # variable to store the image address; this variable will be assigned to the parameter of the same name as the function
base64_of_the_image = infinite_context.imageToBase64(file_path=file_path) # function call that will return the string with the base-64 encoding of the image (accepts any image file)
base64_of_the_image = base64_of_the_image['base64_string'] # the base64 string will be returned in a dictionary with the name key "base64_string"
# checking the text returned by the summary function
if len(base64_of_the_image.strip()) > 0: print('Base 64 generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the base-64!') # if there is no text in the return, it displays the error message
# code to save a text file with the base-64 returned by the function
write = open('./base64_of_the_image.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "base64_of_the_image.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(base64_of_the_image) # writes the content of the "base64_of_the_image" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Base 64 generated successfully.
```
The "saveBase64Image" function converts a base-64 image string into an image file.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
file_path = './files/file_name.png' # variable to store the image address; this variable will be assigned to the parameter of the same name as the "imageToBase64" function
result_dictionary = infinite_context.imageToBase64(file_path=file_path) # function that will return a dictionary with the base-64 string in the "base64_string" key and the type of the converted image in the "image_type" key (accepts any image file)
# code to generate the corresponding base-64 image file
result = infinite_context.saveBase64Image( # call the function that will convert base-64 into a physical file; returns "True" if the file is generated without errors, or "False" if an error occurs
    base64_string=result_dictionary['base64_string'], # parameter that receives the base-64 string
    file_path='./', # parameter that receives the address of the directory where the file will be generated
    image_name='my_image', # parameter that receives the name of the image file that will be generated
    extension=result_dictionary['image_type'] # parameter that receives the type of image file that will be generated
) # the return will be "True" or "False" (if the image is saved successfully the return will be "True")
# checks if the file was generated successfully and without errors
if result: print('The image was generated successfully.') # if the return is "True", it displays the success message
else: print('ERROR when generating the image!') # if the return is "False", it displays the error message
```
```bash
The image was generated successfully.
```
The "saveImageFromPDF" function converts a page of a PDF file into an image.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
result = infinite_context.saveImageFromPDF( # call of the function that will convert one of the pages of the pdf file into an image
    pdf_path='./files/file_name.pdf', # address of the pdf file that will have its page extracted as an image (only for pdf files)
    image_path='./', # parameter that receives the address of the directory where the file will be generated
    image_name='my_image', # parameter that receives the name of the image file that will be generated
    extension='png', # parameter that receives the type of image file that will be generated
    page_index=2 # index starting from zero referring to the position of the page that will be converted into an image
) # the return will be "True" or "False" (if the image is saved successfully the return will be "True")
# checks if the file was generated successfully and without errors
if result: print('The image was generated successfully.') # if the return is "True", it displays the success message
else: print('ERROR when generating the image!') # if the return is "False", it displays the error message
```
```bash
The image was generated successfully.
```
The "getObjectsFromImage" function returns a string with the names of objects detected in an image, the object names will be separated by a comma between them.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
objects_in_the_image = infinite_context.getObjectsFromImage( # returns a string with the names of the objects in the image separated by commas
    file_path='./files/file_name.png', # local or web path of the image to be used for detection (accepted file types without api: jpeg, jpg, png, gif, tiff, bmp, webp, ico, eps, pcx, ppm, xbm, xpm, tga, icns, dds, dib, im, msp, sgi, spider; accepted file types with api: jpeg, jpg, png)
    use_api=True # if "True" will try detection with the external API first and only use local detection if the API fails, if "False" will only use local detection
) # returns an empty string if no objects are detected, a string with a single name if only one object is detected, or a string with multiple names separated by commas if multiple objects are detected
# checks whether one or more objects have been detected
if len(objects_in_the_image) > 0: print('Object(s) detected: '+objects_in_the_image) # if one or more objects are detected, the return will be displayed
else: print('No objects were detected in the image!') # if no object is detected a warning message will be displayed
```
```bash
Object(s) detected: bed, book, bowl, clock, cup, dining table, keyboard, laptop, mouse, remote, scissors
```
The "getTextsFromImage" function returns a string with the texts contained in an image.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
texts_in_the_image = infinite_context.getTextsFromImage( # returns the texts contained in an image or an empty string if no text is detected
    file_path='./files/file_name.png', # local or web path of the image to be used for detection (accepted file types without api: jpeg, jpg, png, gif, tiff, bmp, webp, ico, eps, pcx, ppm, xbm, xpm, tga, icns, dds, dib, im, msp, sgi, spider; accepted file types with api: jpeg, jpg, png)
    use_api=True, # if "True" will try detection with the external API first and only use local detection if the API fails, if "False" will only use local detection
    language=None # string with the language acronym for local detection or "None" for detection via API
) # returns the string with the image texts or an empty string if there is no text or if text is not detected
# checks whether one or more objects have been detected
if len(texts_in_the_image) > 0: print('Text detected: '+texts_in_the_image) # if one or more texts are detected, the return will be displayed
else: print('No texts were detected in the image!') # if no text is detected a warning message will be displayed
```
```bash
Text detected: Example text contained in the image.
```
The "getColorsFromImage" function returns a string with the names of predominant colors detected in an image, the colors names will be separated by a comma between them.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
colors_in_the_image = infinite_context.getColorsFromImage( # returns a string with the names of the colors that stand out the most
    file_path='./files/file_name.png', # local or web path of the image to be used for detection (accepted file types: jpeg, jpg, png, gif, tiff, bmp, webp, ico, eps, pcx, ppm, xbm, xpm, tga, icns, dds, dib, im, msp, sgi, spider)
    maximum_colors=5 # integer with the maximum number of colors to be returned as a response (always a positive integer)
) # returns a string with the names of one or more colors among those that stand out most in the image, always respecting the limit imposed in the "maximum_colors" parameter
# checks whether one or more colors have been detected
if len(colors_in_the_image) > 0: print('Color(s) detected: '+colors_in_the_image) # if one or more colors are detected, the return will be displayed
else: print('No colors were detected in the image!') # if no color is detected a warning message will be displayed
```
```bash
Color(s) detected: black, brown, gray, orange, white
```
The "saveImageFromVideo" function saves the image of a video frame at the specified hour, minute and second.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# code for assigning values to main variables
video_path='./files/file_name.mp4' # path of the video file that will have one of its frames saved as an image (accepted file types: mp4, avi, mov, mkv, wmv, flv)
image_path='./' # directory path where the frame image should be saved
image_name='IMAGE' # name of the image file that will be generated for the frame
extension='.png' # extension (with or without the dot) for the type of image file to be saved
hour=0 # integer referring to the hour of the video where the frame is located
minute=4 # integer referring to the minute of the video where the frame is located
second=25 # integer referring to the second of the video where the frame is located
frame_path = image_path+image_name+extension # full path to the frame image that will be saved
result = infinite_context.saveImageFromVideo( # returns "True" if the frame was captured successfully, or "False" otherwise
    video_path=video_path, # parameter that will receive the string with the local or web address of the video that will have its frame extracted (accepted file types: mp4, avi, mkv, mov, wmv, flv)
    image_path=image_path, # string parameter with the path to the directory where the frame image will be generated
    image_name=image_name, # string parameter with the name of the image that will be generated for the frame
    extension=extension, # string parameter with the extension/type of the image that will be generated
    hour=hour, # integer parameter with the number referring to the hour where the frame is located
    minute=minute, # integer parameter with the number referring to the minute where the frame is located
    second=second # integer parameter with the number referring to the second where the frame is located
) # the return will always be a boolean value that will indicate the success or failure of the operation
# checks if the frame was saved successfully and without errors
if result: print(f'The frame at time {hour}:{minute}:{second} was saved successfully in "{frame_path}".') # if the return is "True", it displays the success message
else: print('ERROR when saving video frame!') # if the return is "False", it displays the error message
```
```bash
The frame at time 0:4:25 was saved successfully in "./IMAGE.png".
```
The "saveAudioFromVideo" function saves the complete audio contained in any video.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
# code for assigning values to main variables
video_path='./files/file_name.mp4' # path to the video that will have its audio extracted and saved (accepted file types: mp4, mov, avi, mkv, wmv, flv)
audio_path='./' # directory where the audio file should be saved
audio_name='AUDIO' # name of the audio file that will be generated
extension='.wav' # extension (with or without the dot) for the type of audio file to be saved
final_path = audio_path+audio_name+extension # full path to the audio that will be saved from the video
result = infinite_context.saveAudioFromVideo( # returns "True" if the audio was extracted and saved successfully, or "False" otherwise
    video_path=video_path, # parameter that will receive the string with the local or web address of the video file that should have its complete audio extracted and saved (accepted file types: mp4, avi, mkv, mov, wmv, flv, webm, mpeg, mpg, m4v)
    audio_path=audio_path, # string parameter with the path to the directory where the audio will be generated
    audio_name=audio_name, # string parameter with the name of the audio that will be generated for the video
    extension=extension # string parameter with the extension/type of the audio that will be generated
) # the return will always be a boolean value that will indicate the success or failure of the operation
# checks if the audio was saved successfully
if result: print(f'The audio file was successfully generated in "{final_path}".') # if the return is "True", it displays the success message
else: print('ERROR when saving video audio!') # if the return is "False", it displays the error message
```
```bash
The audio file was successfully generated in "./AUDIO.wav".
```
The "getAudioTranscript" function returns a string with the transcription of an audio file.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
transcribed_audio = infinite_context.getAudioTranscript( # returns a string with the audio transcription
    file_path='./files/file_name.wav', # local or web path to the audio file to be transcribed (accepted file types: wav, mp3)
    language='en' # string with the acronym of the language in which the audio is found, or "None" to try all possible languages ​​one by one in a slower process
) # it will return as a result a string with the transcription text or an empty string in case of an error
# checks whether the audio was transcribed successfully
if len(transcribed_audio) > 0: print('Transcription result: '+transcribed_audio) # if there is a transcript, it will be displayed
else: print('ERROR when transcribing the audio file!') # if there is no transcript, it displays an error message
```
```bash
Transcription result: transcribed audio result as an example
```
The "countPDFPages" function returns an integer with the number of pages in a PDF file.
```python
from infinite_context import InfiniteContext # module import
infinite_context = InfiniteContext() # main class object instantiation
file_path = './files/file_name.pdf' # variable for the address of the pdf file that will be assigned to the parameter of the same name
number_of_pages = infinite_context.countPDFPages(file_path=file_path) # call of the function that returns the number of pages in the pdf file addressed in the "file_path" parameter (only for pdf files)
print(f'The PDF file "{file_path}" has {number_of_pages} pages.') # displays the number of pages in the read pdf file
```
```bash
The PDF file "./files/file_name.pdf" has 15 pages.
```
The "saveContext" function saves the current context as an index file in the directory of the referenced dialog.
```python
from infinite_context import InfiniteContext # module main class import
infinite_context = InfiniteContext() # main class object instantiation
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
# saves the current context of an input prompt with its corresponding response
# the input/prompt pair with output/answer will be saved as one of the dialog indexes
save_context = infinite_context.saveContext( # only contexts previously saved by this function can be remembered by the model
    user_id=user_id, # assignment of identifier of the user who will have their dialogs saved
    dialog_id=dialog_id, # assigning identifier of current dialog with user input and output pairs
    prompt='Hello, who are you?', # user prompt; used to obtain a response from the language model
    answer="Hi, I'm Sapiens Chat." # response issued by the model to respond to the user's last prompt
) # the return will be "True" or "False" (if the context is saved successfully the return will be "True")
# checks if the context was saved successfully and without errors
if save_context: print('Context saved successfully.') # if the return is "True", it displays the success message
else: print('ERROR when saving the context!') # if the return is "False", it displays the error message
```
```bash
Context saved successfully.
```
The "deleteContext" function deletes all indexed inputs and outputs in the referenced dialog
```python
from infinite_context import InfiniteContext # module main class import
infinite_context = InfiniteContext() # main class object instantiation
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
# deletes all input and output pairs indexed in the dialog directory with the corresponding identifier
save_context = infinite_context.deleteContext( # the deleted dialog will no longer be remembered when the corresponding context is consulted
    user_id=user_id, # assigning an identifier to the user whose dialogues were saved
    dialog_id=dialog_id # assigning identifier of the dialog to be deleted with user input and output pairs
) # the return will be "True" or "False" (if the context is successfully deleted the return will be "True")
# checks whether the context was deleted successfully and without errors
if save_context: print('Context deleted successfully.') # if the return is "True", it displays the success message
else: print('ERROR when deleting the context!') # if the return is "False", it displays the error message
```
```bash
Context deleted successfully.
```

## Methods
### Construtor: InfiniteContext

Parameters
| Name                | Description                                                | Type  | Default Value |
|---------------------|------------------------------------------------------------|-------|---------------|
| display_error_point | Enable or disable error details                            | bool  | True          |

### existingPath (function return type: bool): Returns True if the path exists, or False if it does not exist
Parameters
| Name          | Description                                                       | Type | Default Value |
|---------------|-------------------------------------------------------------------|------|---------------|
| file_path     | Local path or a web address to any file                           | str  | ''            |
| show_message  | Show or hide the non-existent file message                        | bool | False         |

### getHashCode (function return type: str): Returns a unique hash code based on the current date and time
No parameters

### getFileType (function return type: str): Returns the type of a file
Parameters
| Name          | Description                                                       | Type | Default Value |
|---------------|-------------------------------------------------------------------|------|---------------|
| file_path     | Local path or a web address to any file                           | str  | ''            |

### countTokens (function return type: int): Returns the number of tokens in a string
Parameters
| Name      | Description                                                           | Type | Default Value |
|-----------|-----------------------------------------------------------------------|------|---------------|
| string    | String with the text that will have the tokens counted                | str  | ''            |

### getKeyWords (function return type: list): Returns a list with the keywords from a string
Parameters
| Name   | Description                                                              | Type | Default Value |
|--------|--------------------------------------------------------------------------|------|---------------|
| string | String that will have the keywords extracted                             | str  | ''            |

### getBeginningAndEnd (function return type: str): Returns the beginning and end of text in a string
Parameters
| Name       | Description                                                          | Type | Default Value |
|------------|----------------------------------------------------------------------|------|---------------|
| string     | String with the text that will be summarized                         | str  | ''            |
| max_tokens | Maximum number of tokens in result string                            | int  | 1000          |
| separator  | Separator between joined parts in the result string                  | str  | ''            |

### getBeginningMiddleAndEnd (function return type: str): Returns the beginning, middle and end of text in a string
Parameters
| Name       | Description                                                          | Type | Default Value |
|------------|----------------------------------------------------------------------|------|---------------|
| string     | String with the text that will be summarized                         | str  | ''            |
| max_tokens | Maximum number of tokens in result string                            | int  | 1000          |
| separator  | Separator between joined parts in the result string                  | str  | ''            |

### getSummaryCode (function return type: str): Returns the summary of a programming code
Parameters
| Name       | Description                                                          | Type | Default Value |
|------------|----------------------------------------------------------------------|------|---------------|
| text       | Text with the code that will be summarized                           | str  | ''            |
| max_tokens | Maximum number of tokens in result string                            | int  | 1000          |

### getSummaryText (function return type: str): Returns the summary of any text
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| text       | Text with the string that will be summarized                        | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |

### getSummaryTXT (function return type: str): Returns the summary of a TXT file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a TXT file                                  | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |

### imageToBase64 (function return type: dict): Returns a dictionary with the base-64 of an image and the type of that same image
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| file_path | Local or web address of a image file                                 | str   | ''            |

### saveBase64Image (function return type: bool): Saves an image file in base-4
Parameters
| Name          | Description                                                      | Type  | Default Value |
|---------------|------------------------------------------------------------------|-------|---------------|
| base64_string | Image base-64 string                                             | str   | ''            |
| file_path     | Directory address where the file will be saved                   | str   | ''            |
| image_name    | Name of the file to be saved                                     | str   | ''            |
| extension     | Extension of the type of file to be saved                        | str   | ''            |

### saveImageFromPDF (function return type: bool): Saves an image of a page from a PDF file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| pdf_path   | Local or web address of a PDF file                                  | str   | ''            |
| image_path | Directory address where the file will be saved                      | str   | ''            |
| image_name | Name of the file to be saved                                        | str   | ''            |
| extension  | Extension of the type of file to be saved                           | str   | ''            |
| page_index | Index of the page that will be converted into an image              | int   | 0             |

### getObjectsFromImage (function return type: str): Returns the names of objects contained in an image
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| file_path | Local or web address of an image file                                | str   | ''            |
| use_api   | Enable or disable the use of the external API                        | bool  | True          |

### getTextsFromImage (function return type: str): Returns the texts contained in an image
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| file_path | Local or web address of an image file                                | str   | ''            |
| use_api   | Enable or disable the use of the external API                        | bool  | True          |
| language  | Sets the language for local text detection without API               | str   | None          |

### getColorsFromImage (function return type: str): Returns the names of the predominant colors contained in an image
Parameters
| Name           | Description                                                     | Type  | Default Value |
|----------------|-----------------------------------------------------------------|-------|---------------|
| file_path      | Local or web address of an image file                           | str   | ''            |
| maximum_colors | Maximum number of colors to return                              | int   | True          |

### saveImageFromVideo (function return type: bool): Saves a frame of a certain time from a video to an image file
Parameters
| Name           | Description                                                     | Type  | Default Value |
|----------------|-----------------------------------------------------------------|-------|---------------|
| video_path     | Local or web address of an video file                           | str   | ''            |
| image_path     | Path to the save directory                                      | str   | ''            |
| image_name     | Name of the file that will be generated                         | str   | ''            |
| extension      | Extension for the file type with or without a dot               | str   | ''            |
| hour           | Exact hour to capture the frame                                 | int   | 0             |
| minute         | Exact minute to capture the frame                               | int   | 0             |
| second         | Exact second to capture the frame                               | int   | 0             |

### saveAudioFromVideo (function return type: bool): Saves all audio contained in a video
Parameters
| Name           | Description                                                     | Type  | Default Value |
|----------------|-----------------------------------------------------------------|-------|---------------|
| video_path     | Local or web address of an video file                           | str   | ''            |
| audio_path     | Path to the save directory                                      | str   | ''            |
| audio_name     | Name of the file that will be generated                         | str   | ''            |
| extension      | Extension for the file type with or without a dot               | str   | ''            |

### getAudioTranscript (function return type: str): Returns text with the complete transcription of an audio file
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| file_path | Local or web address of an audio file                                | str   | ''            |
| language  | Language used in transcription                                       | str   | None          |

### countPDFPages (function return type: int): Returns the number of pages in a PDF file
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| file_path | Local or web address of a PDF file                                   | str   | ''            |

### getSummaryYouTube (function return type: str): Returns the content summary of a YouTube video
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | YouTube video address                                               | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |

### getSummaryWEBPage (function return type: str): Returns the summary of the content of a WEB page
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | WEB page address                                                    | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |

### getSummaryPDF (function return type: str): Returns the summary of the content of a PDF file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a PDF file                                  | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |
| main_page  | Page number that will contain most of the summary                   | int   | None          |
| use_api    | Defines whether the external API will be used                       | bool  | True          |
| language   | Sets language if external API is not used                           | str   | None          |

### getSummaryWord (function return type: str): Returns the summary of the content of a Microsoft Word file
Parameters
| Name                | Description                                                | Type  | Default Value |
|---------------------|------------------------------------------------------------|-------|---------------|
| file_path           | Local or web address of a Microsoft Word file              | str   | ''            |
| max_tokens          | Maximum number of tokens in result string                  | int   | 1000          |
| main_page           | Page number that will contain most of the summary          | int   | None          |
| characters_per_page | Maximum number of characters per page                      | int   | 4000          |

### getSummaryPowerPoint (function return type: str): Returns the summary of the contents of a Microsoft PowerPoint file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a Microsoft PowerPoint file                 | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |
| main_page  | Page number that will contain most of the summary                   | int   | None          |

### getSummaryCSV (function return type: str): Returns the summary of the content of a CSV file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a CSV file                                  | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |
| separator  | Cell separator/delimiter character                                  | str   | None          |

### getSummaryExcel (function return type: str): Returns the summary of the content of a Microsoft Excel file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a Microsoft Excel file                      | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |

### getSummaryImage (function return type: str): Returns the summary of the content of a image file
Parameters
| Name           | Description                                                     | Type  | Default Value |
|----------------|-----------------------------------------------------------------|-------|---------------|
| file_path      | Local or web address of a image file                            | str   | ''            |
| max_tokens     | Maximum number of tokens in result string                       | int   | 1000          |
| use_api        | Defines whether to use the API to detect objects and texts      | bool  | True          |
| language       | Sets the language for local text detection without API          | str   | None          |
| maximum_colors | Maximum number of colors to return                              | int   | 3             |

### getSummaryAudio (function return type: str): Returns the summary of the content of a audio file
Parameters
| Name       | Description                                                         | Type  | Default Value |
|------------|---------------------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a audio file                                | str   | ''            |
| max_tokens | Maximum number of tokens in result string                           | int   | 1000          |
| language   | Language used in transcription                                      | str   | None          |

### getSummaryVideo (function return type: str): Returns the summary of the content of a video file
Parameters
| Name           | Description                                                     | Type  | Default Value |
|----------------|-----------------------------------------------------------------|-------|---------------|
| file_path      | Local or web address of a video file                            | str   | ''            |
| max_tokens     | Maximum number of tokens in result string                       | int   | 1000          |
| use_api        | Defines whether to use the API to detect objects and texts      | bool  | True          |
| language       | Sets the language for local text detection without API          | str   | None          |
| maximum_colors | Maximum number of colors to return                              | int   | 3             |

### getSummaryFile (function return type: str): Returns the summary of the contents of a file
Parameters
| Name                | Description                                                | Type  | Default Value |
|---------------------|------------------------------------------------------------|-------|---------------|
| file_path           | Local or web address of a file                             | str   | ''            |
| max_tokens          | Maximum number of tokens in result string                  | int   | 1000          |
| main_page           | Page number that will contain most of the summary          | int   | None          |
| characters_per_page | Maximum number of characters per page                      | int   | 4000          |
| separator           | Cell separator/delimiter character                         | str   | None          |
| use_api             | Defines whether to use the API to detect objects and texts | bool  | True          |
| language            | Sets the language for local text detection without API     | str   | None          |
| maximum_colors      | Maximum number of colors to return                         | int   | 3             |

### saveContext (function return type: bool): Saves current context to indexed files
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| user_id   | User identifier                                                      | int   | 0             |
| dialog_id | Dialog identifier                                                    | int   | 0             |
| prompt    | User input prompt                                                    | str   | ''            |
| answer    | Virtual assistant output response                                    | str   | ''            |

### deleteContext (function return type: bool): Deletes the conversation context of a dialog belonging to a user
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| user_id   | User identifier                                                      | int   | 0             |
| dialog_id | Dialog identifier                                                    | int   | 0             |

### getContext (function return type: str/list): Gets the full conversational context of a user's dialog
Parameters
| Name      | Description                                                          | Type  | Default Value |
|-----------|----------------------------------------------------------------------|-------|---------------|
| user_id   | User identifier                                                      | int   | 0             |
| dialog_id | Dialog identifier                                                    | int   | 0             |
| config    | Setting for context return format                                    | dict  | None          |

## getContext (function return type: list/str): Returns context based on semantic comparison algorithms
```python
from infinite_context import InfiniteContext # module main class import
infinite_context = InfiniteContext() # main class object instantiation
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
system = 'You are an Artificial Intelligence created by Sapiens Technology called Sapiens Chat.' # system prompt used to define how the language model should behave
prompt = 'Hello! Please tell me who you are.' # user prompt; used to obtain a response from the language model
# code to get the main context of the conversation from one of any user's dialogs
main_context = infinite_context.getContext( # function call that will return the main context in the format "list" or "str" respecting the tokens limit established in the model settings
    user_id=user_id, # assignment of identifier of the user who will have their dialogs consulted
    dialog_id=dialog_id, # assignment of identifier of one of the dialogs with user input and output pairs
    config={'system': system, 'prompt': prompt, 'max_tokens': 4000} # assignment of the configuration dictionary that will define the context format
) # the "main_context" variable will store the return of the "getContext" function contained in the "infinite_context" object
if len(main_context) > 0: # checks if there is content in the returned context
    write = open( # assigns to the "write" object the opening of a file for writing and recording
        './main_context.txt', # address, name and extension of the file that will receive the recorded content, if the file does not exist it will be generated
        'w', # "w" value so that the file is opened in writing mode
        encoding='utf-8', # assigns "utf-8" to the opening encoding to interpret any special accent characters
        errors='ignore' # the "ignore" value ignores possible errors when opening the file
    ) # the "write" variable receives the opened file
    write.write(str(main_context)) # writes the string corresponding to the returned context to the file
    write.close() # closes the file that was opened, freeing it from memory
    print('The main context of the dialogue was successfully achieved.') # displays a success message if everything goes correctly
else: print('ERROR getting main dialog context!') # displays an error message if context is not returned
```
```bash
The main context of the dialogue was successfully achieved.
```
```python
from infinite_context import InfiniteContext # module main class import
infinite_context = InfiniteContext( # main class object instantiation
    display_error_point=False # if "True", it enables the detailed display of possible errors, if "False" it disables the detailed display of possible errors
) # the "perpetual context" variable receives the value of the "InfiniteContext" class instantiation and becomes an object of that same class
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
system = 'You are an Artificial Intelligence created by Sapiens Technology called Sapiens Chat.' # system prompt used to define how the language model should behave
prompt = 'Hello! Please tell me who you are.' # user prompt; used to obtain a response from the language model
# data dictionary used as configuration for the context output format
config = { # with the exception of the key named "max_tokens", all other keys are dispensable
    'system': system, # system prompt assignment (optional value)
    'prompt': prompt, # user prompt assignment (optional value)
    'max_tokens': 4000, # assigning of maximum tokens limit in the context (optional value but highly recommended as the default is 1)
    ''''
        the supported format types in "return_format" are: "dictionaries_list" (ChatGPT API messages vector pattern with customizable keys and values),
        "chatgpt_pattern" (ChatGPT API messages vector pattern), "gemini_pattern" (Gemini API messages vector pattern),
        "claude_pattern" (Claude API input text pattern), "llama3_pattern" (Llama 3 input text pattern),
        "mistral_pattern" (Mistral input text pattern), "gemma_pattern" (Gemma input text pattern),
        "phi3_pattern" (Phi-3 input text pattern), "yi_pattern" (Yi input text pattern), "falcon_pattern" (Falcon input text pattern),
        "falcon2_pattern" (Falcon 2 input text pattern), "stablelm2_pattern" (Stable LM 2 input text pattern)
        or any string other than the previous ones for a standard return
    '''
    'return_format': 'dictionaries_list', # return context format; default value is "dictionaries_list" for a list of dictionaries similar to the one used by the OpenAI API
    'system_key': 'system', # name of the value used in the "role" key to specify the system prompt in the first dictionary of the return list (only used for the "dictionaries_list" pattern)
    'interlocutor_key': 'role', # name of the key used to define who owns the text content in the return list dictionaries (only used for the "dictionaries_list" pattern)
    'user_value': 'user', # value used in the "role" key or the key that replaces it; this value will specify that the dictionary text in the list belongs to the human user (only used for the "dictionaries_list" pattern)
    'assistant_value': 'assistant', # value used in the "role" key or the key that replaces it; this value will specify that the dictionary text in the list belongs to the virtual assistant issuing the responses (only used for the "dictionaries_list" pattern)
    'content_key': 'content', # name of the key used to define the text contents in the return list dictionaries (only used for the "dictionaries_list" pattern)
    'dialogue_indexes': [] # list of integers with the position indices of the input and output pairs that must appear in the returned context; if the list is empty, the input and output pairs returned will be those that best explain the user's current prompt
} # the keys "role" and "content" or their replacements in "interlocutor_key" and "content_key" will be in all dictionaries in the return list when the format returned is "dictionaries_list"
# code to get the main context of the conversation from one of any user's dialogs
main_context = infinite_context.getContext( # function call that will return the main context in the format "list" or "str" respecting the tokens limit established in the model settings
    user_id=user_id, # assignment of identifier of the user who will have their dialogs consulted
    dialog_id=dialog_id, # assignment of identifier of one of the dialogs with user input and output pairs
    config=config # assignment of the configuration dictionary that will define the context format
) # the "main_context" variable will store the return of the "getContext" function contained in the "infinite_context" object
if len(main_context) > 0: # checks if there is content in the returned context
    write = open( # assigns to the "write" object the opening of a file for writing and recording
        './main_context.txt', # address, name and extension of the file that will receive the recorded content, if the file does not exist it will be generated
        'w', # "w" value so that the file is opened in writing mode
        encoding='utf-8', # assigns "utf-8" to the opening encoding to interpret any special accent characters
        errors='ignore' # the "ignore" value ignores possible errors when opening the file
    ) # the "write" variable receives the opened file
    write.write(str(main_context)) # writes the string corresponding to the returned context to the file
    write.close() # closes the file that was opened, freeing it from memory
    print('The main context of the dialogue was successfully achieved.') # displays a success message if everything goes correctly
else: print('ERROR getting main dialog context!') # displays an error message if context is not returned
```
```bash
The main context of the dialogue was successfully achieved.
```

## Contributing

We do not accept contributions that may result in changing the original code.

Make sure you are using the appropriate version.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.
