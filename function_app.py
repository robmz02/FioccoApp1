import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json
import csv
import io

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="Fiocco")
def Fiocco(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Verifica se il parametro "name" è presente nella richiesta
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # Salva il parametro "name" come file CSV su Azure Blob Storage
        storage_connection_string = "AZURE_STORAGE_CONNECTION_STRING"
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        container_name = "test"
        container_client = blob_service_client.get_container_client(container_name)
        blob_name = f"{name}.csv"
        
        # Creazione del file CSV
        csv_data = [["Name"], [name]]

        # Salvataggio del file CSV nel blob
        blob_client = container_client.get_blob_client(blob_name)
        with io.StringIO() as output:
            writer = csv.writer(output)
            writer.writerows(csv_data)
            blob_client.upload_blob(output.getvalue(), overwrite=True)
        
        func.HttpResponse(f"File CSV creato con successo per il nome '{name}'.", status_code=200)
    else:
        func.HttpResponse(
            "Passa un nome tramite il parametro 'name' nell'input JSON.",
             status_code=400
        )