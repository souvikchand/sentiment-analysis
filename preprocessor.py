replacement_dict = {
    r'\br\b'         : 'are'           ,          r'\bwkly\b'    : 'weekly'   ,
    r'\bk\b'         : 'ok'            ,          r'\bu\b'       : 'you'      ,
    r'\btkts\b'      : 'tickets'       ,          r'\bb\b'       : 'be'       ,
    r'\baft\b'       : 'after'         ,          r'&amp;'       : ''         ,
    r'â€™'           : "'"             ,          r'\bur\b'      : 'your'     ,
    r'\bv\b'         : 'very'          ,          r'\bpls\b'     : 'please'   ,
    r'\bc\b'         : 'see'           ,          r'\blar\b'     : 'later'    ,
    r'\bda\b'        : 'the'           ,          r'frnd'        : 'friend'   ,
    r'\bwat\b'       : 'what'          ,          r'\babt\b'     : 'about'    ,
    r'\bwen\b'       : 'when'          ,          r'\benuff\b'   : 'enough'   ,
    r'\bn\b'         : 'in'            ,          r'\brply\b'    : 'reply'    ,
    r'\bthk\b'       : 'think'         ,          r'\btot\b'     : 'thought'  ,
    r'\bnite\b'      : 'night'         ,          r'\bnvm\b'     : 'never mind',
    r'\btxt\b'       : 'text'          ,          r'\btxting\b'  : 'texting'  ,
    r'\bgr8\b'       : 'great'         ,          r'\bim\b'      : 'i am'     ,
    r'\b<unk>\b'     : ''              ,          r'\bfav\b'     : 'favorite' ,
    r'\bdlvr\b'      : 'deliver'       ,          r"(?<=\s)'m(?=\s)|^'m(?=\s)|(?<=\s)'m$" : 'am',
    r'\b\w*\d\w*\b'  : ''              ,          r"(?<=\s)<unk>(?=\s)|^<unk>(?=\s)|(?<=\s)<unk>$": ''


}

def replace_words(text:str)->str:
    """
    solves fast typing 

    input--> string

    output--> string
    """
    for pattern, replacement in replacement_dict.items():
        text = re.sub(pattern, replacement, text)
    return text

def emoji_decode(text)->str:
  """
  decodes emojis to their meaning

  example: input: '👾' 

           output: 'alien monster'
  """
  demojize_text= emoji.demojize(text)
  demojize_text = re.sub(r':', '', demojize_text)
  demojize_text = re.sub(r'_', ' ', demojize_text)
  return demojize_text

def remove_url_and_domains(text):
    """
    removes urls, mentions and links
    
    example: http, https, www, .com, .org, .en, .edu, .gov, .net
    """
    # Remove the URLs
    re_url = re.compile(r'https?://\S+|www\.\S+')
    text = re_url.sub('', text)

    # Define the regex pattern to match text containing domain-like patterns
    pattern = r'\b(?:\w+@\w+\.\w+|\w+\.\w+|\w+\.(?:com|tv|org|net|edu|gov|en|mil|int))\b'

    # Replace matched patterns with an empty string
    text = re.sub(r'\S*\b(?:\w+@\w+\.\w+|\w+\.\w+|\w+\.(?:com|tv|org|net|edu|gov|mil|int))\b\S*', '', text)

    # Remove custom patterns like RhandlerR, RhttpsR
    custom_pattern = r'\bR(?:handler|https|http|web|other_patterns_here)R\b'
    text = re.sub(custom_pattern, '', text)

    # Remove multiple spaces resulting from removal and trim leading/trailing spaces
    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    return cleaned_text

def remove_punctuation(text):
    """
    remove punctuations
    example -->
    input: "Hello, World! This is a test. Let's &remove #punctuation & @ special_characters... 123!()"

    output: 'Hello World This is a test Lets remove punctuation special characters 123'
    """
    text = re.sub(r'_', " ", text)
    text= text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def lower_case(text):
  return text.lower()


def correct_spelling_preserve_entities(text):
    """
    Use spaCy to process the text and identify entities

    example -->

    input: "I havv a speling eror in this sentnce. Google and Microsft are big tech compnies. 
            Jhon mrries Clara. yumekuyi high school"

    output: I have a spelling error in this sentence . Google and Microsft are big teach companies . 
            Jhon marries Clara . yumekuyi high school
    """
    
    doc = nlp(text)

    # Initialize a list to hold the final corrected text
    corrected_tokens = []

    for token in doc:
        # Check if the token is part of a named entity
        if token.ent_type_:
            # If it is a named entity, don't correct it, just add it as is
            corrected_tokens.append(token.text)
        else:
            # Otherwise, correct the spelling
            corrected_word = str(TextBlob(token.text).correct())
            corrected_tokens.append(corrected_word)

    # Join the tokens back into a single string
    corrected_text = ' '.join(corrected_tokens)
    corrected_text = re.sub(r'\s+', ' ', corrected_text).strip()

    return corrected_text