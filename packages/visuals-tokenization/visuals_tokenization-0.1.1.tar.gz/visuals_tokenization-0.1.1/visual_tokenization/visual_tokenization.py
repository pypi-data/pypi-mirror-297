import nltk
import transformers
import spacy
import gensim
import beautifultable

def view_tokenize(text):
    ##TODO: WORD TOKENIZATION:
        
    from nltk.tokenize import word_tokenize
    token1 = word_tokenize(text)
    
    
    ##TODO: SENTENCE TOKENIZATION
    
    from nltk.tokenize import sent_tokenize
    token2 = sent_tokenize(text)
    
    
    ##TODO: WHITE SPACE TOKENIZATION
    from nltk.tokenize import WhitespaceTokenizer 
    token3 = WhitespaceTokenizer() .tokenize(text) 
    
    #TODO: REGEX TOKENIZATION
    from nltk.tokenize import regexp_tokenize
    token4 = regexp_tokenize(text, r'\w+')
    
    #TODO: TREE BANK WORD TOKENIZATION
    from nltk.tokenize import TreebankWordTokenizer
    token5=TreebankWordTokenizer().tokenize(text)
    
    #TODO: WORD PUNCT TOKENIZATION
    from nltk.tokenize import WordPunctTokenizer 
    token6 = WordPunctTokenizer().tokenize(text) 
    
    #TODO: TWEET TOKENIZATION
    from nltk.tokenize import TweetTokenizer
    token7 = TweetTokenizer().tokenize(text)
    
    #TODO: MWE TOKENIZATION
    from nltk.tokenize import MWETokenizer
    tokenizer=MWETokenizer()
    tokenizer.add_mwe(('older','patients'))
    token8 = tokenizer.tokenize(word_tokenize(text))
    
    
    
    #TODO: BERT TOKENIZER
    from transformers import BertTokenizer
    tokenizer = BertTokenizer.from_pretrained('google-bert/bert-base-uncased')
    token10 = tokenizer.tokenize(text)
    
    #TODO: SPACY TOKENIZATION
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    token11 = [token.text for token in doc]
    
    #TODO: GENSIM
    from gensim.utils import tokenize
    token12=list(tokenize(text))
    
    #TODO: BIGRAM
    from nltk import word_tokenize
    from nltk.util import ngrams
    tokens = word_tokenize(text)
    token13 = list(ngrams(tokens, 2))
    
    #TODO: TRIGRAM
    from nltk import word_tokenize
    from nltk.util import ngrams
    tokens = word_tokenize(text)
    token14 = list(ngrams(tokens, 3))
    
    
    #TODO:XLNET TOKENIZATION
    
    from transformers import XLNetTokenizer
    tokenizer = XLNetTokenizer.from_pretrained("xlnet/xlnet-base-cased")
    token15 = tokenizer.tokenize(text)
    
    
    from beautifultable import BeautifulTable
    table = BeautifulTable()
    table.columns.header = ["Tokenization Methord","tokens"]
    table.rows.append(["Word Tokenization",token1])
    table.rows.append(["Sentence Tokenization",token2])
    table.rows.append(["White Space Tokenization",token3])
    table.rows.append(["Regex Tokenization",token4])
    table.rows.append(["TreeBank word Tokenization",token5])
    table.rows.append(["WordPunct Tokenization",token6])
    table.rows.append(["TWEET Tokenization",token7])
    table.rows.append(["MWE Tokenization",token8])
    table.rows.append(["BERT Tokenization",token10])
    table.rows.append(["Spacy Tokenization",token11])
    table.rows.append(["Gensim Tokenization",token12])
    table.rows.append(["Bigram Tokenization",token13])
    table.rows.append(["Trigram Tokenization",token14])
    table.rows.append(["XLNet Tokenization",token15])
    
    print(table)



