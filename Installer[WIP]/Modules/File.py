import zipfile

def extract_zip(zip_path, extract_to):
    """
    Extracts a zip file to the specified directory.

    :param zip_path: Path to the zip file.
    :param extract_to: Directory where the contents should be extracted.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")
    except zipfile.BadZipFile:
        print(f"Error: {zip_path} is not a valid zip file.")
    except Exception as e:
        print(f"An error occurred while extracting {zip_path}: {e}")