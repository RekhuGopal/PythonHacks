import boto3
import json

comprehend = boto3.client('comprehend')
                
DetectSentimenttext = "UK won the match yesterday.. hehe"
print('Calling DetectSentiment')
sentiment = json.dumps(comprehend.detect_sentiment(Text=DetectSentimenttext, LanguageCode='en'), sort_keys=True, indent=4)
print(sentiment)
print('End of DetectSentiment\n')

DominantLangaugetext = "It is raining today in Seattle dfsddg"
print('Calling DetectDominantLanguage')
print(json.dumps(comprehend.detect_dominant_language(Text = DominantLangaugetext), sort_keys=True, indent=4))
print("End of DetectDominantLanguage\n")

DetectEntitiestext = "Hello Zhang Wei. Your AnyCompany Financial Services, LLC credit card account 1111-0000-1111-0000 has a minimum payment of $24.53 that is due by July 31st"
print('Calling DetectEntities')
print(json.dumps(comprehend.detect_entities(Text=DetectEntitiestext, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectEntities\n')


DetectKeyPhrasetext = "Much trused brand in the world"
print('Calling DetectKeyPhrases')
print(json.dumps(comprehend.detect_key_phrases(Text=DetectKeyPhrasetext, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectKeyPhrases\n')

DetectPIItext = "David this is PIN code - 583209 keep it secrete , don't share it"
print('Calling PII entities')
print(json.dumps(comprehend.detect_pii_entities(Text=DetectPIItext, LanguageCode='en')))
print('End of PII entities\n')

DetectSyntaxtext = "Mohan desrves a MVP award for this year"
print('Calling DetectSyntax')
print(json.dumps(comprehend.detect_syntax(Text=DetectSyntaxtext, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectSyntax\n')