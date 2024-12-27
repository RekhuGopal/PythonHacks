import os


def format_price(price_dict):
    return "".join([f"{p}" for p in price_dict.values()])


def analyze_receipts():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

    endpoint = "<API URL>"
    key = "<API Key>"

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    receiptUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png"

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-receipt",
        AnalyzeDocumentRequest(url_source=receiptUrl)
    )       

    receipts: AnalyzeResult = poller.result()

    if receipts.documents:
        for idx, receipt in enumerate(receipts.documents):
            print(f"--------Analysis of receipt #{idx + 1}--------")
            print(f"Receipt type: {receipt.doc_type if receipt.doc_type else 'N/A'}")
            if receipt.fields:
                merchant_name = receipt.fields.get("MerchantName")
                if merchant_name:
                    print(
                        f"Merchant Name: {merchant_name.get('valueString')} has confidence: "
                        f"{merchant_name.confidence}"
                    )
                transaction_date = receipt.fields.get("TransactionDate")
                if transaction_date:
                    print(
                        f"Transaction Date: {transaction_date.get('valueDate')} has confidence: "
                        f"{transaction_date.confidence}"
                    )
                items = receipt.fields.get("Items")
                if items:
                    print("Receipt items:")
                    for idx, item in enumerate(items.get("valueArray")):
                        print(f"...Item #{idx + 1}")
                        item_description = item.get("valueObject").get("Description")
                        if item_description:
                            print(
                                f"......Item Description: {item_description.get('valueString')} has confidence: "
                                f"{item_description.confidence}"
                            )
                        item_quantity = item.get("valueObject").get("Quantity")
                        if item_quantity:
                            print(
                                f"......Item Quantity: {item_quantity.get('valueString')} has confidence: "
                                f"{item_quantity.confidence}"
                            )
                        item_total_price = item.get("valueObject").get("TotalPrice")
                        if item_total_price:
                            print(
                                f"......Total Item Price: {format_price(item_total_price.get('valueCurrency'))} has confidence: "
                                f"{item_total_price.confidence}"
                            )
                subtotal = receipt.fields.get("Subtotal")
                if subtotal:
                    print(
                        f"Subtotal: {format_price(subtotal.get('valueCurrency'))} has confidence: {subtotal.confidence}"
                    )
                tax = receipt.fields.get("TotalTax")
                if tax:
                    print(f"Total tax: {format_price(tax.get('valueCurrency'))} has confidence: {tax.confidence}")
                tip = receipt.fields.get("Tip")
                if tip:
                    print(f"Tip: {format_price(tip.get('valueCurrency'))} has confidence: {tip.confidence}")
                total = receipt.fields.get("Total")
                if total:
                    print(f"Total: {format_price(total.get('valueCurrency'))} has confidence: {total.confidence}")
            print("--------------------------------------")


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        analyze_receipts()
    except HttpResponseError as error:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            raise
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        raise