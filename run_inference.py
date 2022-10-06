import argparse
from asyncio.log import logger
from Layoutlmv3_inference.ocr import prepare_batch_for_inference
from Layoutlmv3_inference.inference_handler import handle
from xml_converter import pdftoxml_maker
import logging
import os

def data_preprocessing(inference_out):
    predicted_data = inference_out[0].get('output')

    invoice_number = ''
    invoice_date = ''
    po_number = ''
    invoice_amount = ''
    itemdetails = []

    for p_d in predicted_data:
        if p_d.get('label') == 'INVOICE NUMBER': 
            invoice_number = p_d.get('text')
        elif p_d.get('label') == 'INVOICE DATE': 
            invoice_date = p_d.get('text')
        elif p_d.get('label') == 'PURCHASE ORDER NUMBER': 
            po_number = p_d.get('text')
        elif p_d.get('label') == 'INVOICE AMOUNT':
            invoice_amount = p_d.get('text')

    return invoice_number,invoice_date,po_number,invoice_amount, itemdetails

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--model_path", type=str)
        parser.add_argument("--images_path", type=str)
        args, _ = parser.parse_known_args()
        images_path = args.images_path
        image_files = os.listdir(images_path)
        print(image_files, 'runinfer16')
        images_path = [images_path+f'/{image_file}' for image_file in image_files]
        inference_batch = prepare_batch_for_inference(images_path)
        context = {"model_dir": args.model_path}
        inference_out = handle(inference_batch,context)
        invoice_number,invoice_date,po_number,invoice_amount,itemdetails = data_preprocessing(inference_out)
        pdftoxml_maker(invoice_number,invoice_date,po_number,invoice_amount, itemdetails)
    except Exception as err:
        os.makedirs('log', exist_ok=True)
        logging.basicConfig(filename='log/error_output.log', level=logging.ERROR,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(__name__)
        logger.error(err)
