import logging
from json import dumps
import azure.functions as func


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    xml = myblob.read()
    print(xml)
    return dumps({"xml": xml.decode('utf-8')})
