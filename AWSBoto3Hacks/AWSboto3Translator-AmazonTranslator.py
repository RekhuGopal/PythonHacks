
import boto3

translate = boto3.client('translate')
result = translate.translate_text(Text="Today is Sunday...",
                                  SourceLanguageCode="en",
                                  TargetLanguageCode="kn")
print(f'TranslatedText: {result["TranslatedText"]}')
print(f'SourceLanguageCode: {result["SourceLanguageCode"]}')
print(f'TargetLanguageCode: {result["TargetLanguageCode"]}')
