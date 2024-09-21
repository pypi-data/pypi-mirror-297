import os
import json
import asyncio
import aiohttp
import re
import base64
from cryptography.fernet import Fernet
from fastapi import FastAPI, Request, UploadFile, File, Form, Response,HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, storage, db
from io import BytesIO
import pydicom
from pydicom import dcmread
from pydicom.filewriter import dcmwrite
from threading import Lock
import logging
from datetime import datetime
import warnings

# Suppress specific pydicom warning
warnings.filterwarnings("ignore", message="Invalid value for VR DA")

# Initialize FastAPI app
app = FastAPI()
origins = ['*']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Obfuscated key (Base64 encoded)
obfuscated_key = "Q2dYUTduRVpHVWUyOWF0dTFTZ0huWkFTN1B1TW1CdWtueUFfaFNHVkRpST0=" 

# Decode the key
key = base64.b64decode(obfuscated_key.encode('utf-8'))

cipher_suite = Fernet(key)

# Load the encrypted credentials
creds_path = os.path.join(os.path.dirname(__file__), 'encrypted_creds.txt')
with open(creds_path, 'rb') as encrypted_file:
    encrypted_creds = encrypted_file.read()

# Decrypt the credentials
firebase_creds = cipher_suite.decrypt(encrypted_creds).decode()

# Firebase initialization
cred = credentials.Certificate(json.loads(firebase_creds))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'dicom-admin.appspot.com',
    'databaseURL': 'https://dicom-admin-default-rtdb.firebaseio.com'
})

ref = db.reference()
bucket = storage.bucket()
ORTHANC_SERVER_URL = "http://localhost:8042"

# Persistent aiohttp session
session = None

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.on_event("startup")
async def startup_event():
    global session
    if session is None:
        session = aiohttp.ClientSession()

@app.on_event("shutdown")
async def shutdown_event():
    if session:
        await session.close()

async def fetch_with_retries(url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error fetching {url}: {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Client error on attempt {attempt + 1} for {url}: {e}")
        await asyncio.sleep(1)
    raise Exception(f"Failed to fetch {url} after {retries} attempts")

async def fetch_dicom_with_retries(url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    logger.error(f"Error fetching {url}: {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Client error on attempt {attempt + 1} for {url}: {e}")
        await asyncio.sleep(1)
    raise Exception(f"Failed to fetch {url} after {retries} attempts")


progress_lock = Lock()
progress = {}
cancellation_flags = {}

# Update the cancel_upload endpoint to accept patient_id as a form field
@app.post('/cancelUpload')
async def cancel_upload(patient_id: str = Form(...)):
    with progress_lock:
        if patient_id in progress:
            cancellation_flags[patient_id] = True
            del progress[patient_id]
            return JSONResponse(content={"message": f"Upload for patient {patient_id} has been cancelled."})
        else:
            raise HTTPException(status_code=404, detail="Upload not found for the given patient ID.")

@app.get('/seriesList/{studyInstanceUID}')
async def get_series_list(studyInstanceUID: str):
    try:
        data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/studies/{studyInstanceUID}")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/seriesInstanceUid/{series}')
async def get_series_instance_uid(series: str):
    try:
        data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/series/{series}")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/seriesInstanceList/{series}')
async def get_series_instance_list(series: str):
    try:
        data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/series/{series}/instances")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/instanceFile/{instanceID}')
async def get_instance_files(instanceID: str):
    try:
        content = await fetch_dicom_with_retries(f"{ORTHANC_SERVER_URL}/instances/{instanceID}/file")
        return StreamingResponse(BytesIO(content), media_type="application/dicom")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/studySeries/{studyID}')
async def get_study_series(studyID: str):
    try:
        data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/studies/{studyID}/series")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/patients')
async def get_patients(limit: int = 10, offset: int = 0):
    try:
        patients = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/patients")
        total_count = len(patients)
        paginated_patients = patients[offset:offset + limit]
        return JSONResponse(content={"patients": paginated_patients, "total_count": total_count})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/patient/{patientID}')
async def get_patient(patientID: str):
    try:
        data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/patients/{patientID}")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/patientStudies/{patientID}')
async def get_studies_for_patient(patientID: str):
    try:
        data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/patients/{patientID}/studies")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post('/upload')
async def upload_files(
    adminName1: str = Form(...),
    patientId: str = Form(...),
    timestamp: str = Form(...),
    files: list[UploadFile] = File(...)
):
    results = []
    rootFolderPath = f"superadmin/admins/{adminName1}/patients/{patientId}/folder_{timestamp}/"
    all_uploads_success = True

    for file in files:
        try:
            ds = dcmread(BytesIO(await file.read()))
            ds = mask_dicom(ds)
            memory_file = BytesIO()
            dcmwrite(memory_file, ds, write_like_original=False)
            memory_file.seek(0)

            webkit_path = file.filename
            safe_path = secure_path(webkit_path)
            immediate_directory = os.path.basename(os.path.dirname(webkit_path)) if os.path.dirname(webkit_path) else ""
            safe_immediate_directory = secure_filename(immediate_directory)
            firebase_path = f"{rootFolderPath}{safe_immediate_directory}/{os.path.basename(safe_path)}"
            blob = bucket.blob(firebase_path)
            blob.upload_from_file(memory_file, content_type='application/dicom')
            file_url = blob.public_url
            results.append({"filename": firebase_path, "url": file_url})
        except Exception as e:
            app.logger.error(f"Error processing or uploading file: {e}")
            all_uploads_success = False
            break

    if all_uploads_success:
        db_ref = ref.child(f"superadmin/admins/{adminName1}/patients/{patientId}")
        db_ref.update({'FolderPath': rootFolderPath})
        return JSONResponse(content={"message": "Files have been successfully processed and uploaded!", "files": results})
    else:
        return JSONResponse(content={"error": "Failed to process or upload one or more files"}, status_code=500)



@app.post('/uploadortho')
async def upload_files_ortho(
    adminName1: str = Form(...),
    patientKey: str = Form(...),
    rootFolderPathortho: str = Form(...),
    studyInstanceUID: str = Form(...),
    patientName: str = Form(...),
    studyType: str = Form(...),
    patientID: str = Form(...),
    patientBirthDate: str = Form(...),
    patientSex: str = Form(...),
    studyDate: str = Form(...),
    referringPhysicianName: str = Form(...),
    modality: str = Form(...),
    technicianName: str = Form(...),
    StudyInstanceUid: str = Form(...),
    PatientDataId: str = Form(...),
):
    logger.info(f"Received data: adminName1={adminName1}, patientKey={patientKey}, rootFolderPathortho={rootFolderPathortho}, "
                f"studyInstanceUID={studyInstanceUID}, patientName={patientName}, studyType={studyType}, patientID={patientID}, "
                f"patientBirthDate={patientBirthDate}, patientSex={patientSex}, studyDate={studyDate}, referringPhysicianName={referringPhysicianName}, "
                f"modality={modality}, technicianName={technicianName}, StudyInstanceUid={StudyInstanceUid}, PatientDataId={PatientDataId}")

    results = []
    all_uploads_success = True
    seriesInstanceUid = []

    progress[patientKey] = {"total": 0, "completed": 0}
    cancellation_flags[patientKey] = False  # Initialize the cancellation flag

    try:
        # Fetch series list
        series_data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/studies/{studyInstanceUID}")
        instances_to_upload = []

        for series in series_data["Series"]:
            if cancellation_flags.get(patientKey):  # Check for cancellation
                logger.info(f"Upload for patient {patientKey} has been cancelled.")
                return JSONResponse(content={"message": "Upload cancelled by user."}, status_code=200)

            series_instance_uid_data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/series/{series}")
            series_instance_uid = series_instance_uid_data["MainDicomTags"]["SeriesInstanceUID"]
            series_desc = series_instance_uid_data["MainDicomTags"].get("SeriesDescription") or "Unknown"
            seriesInstanceUid.append(series_instance_uid)

            instance_list_data = await fetch_with_retries(f"{ORTHANC_SERVER_URL}/series/{series}/instances")
            instances_to_upload.extend(
                [{"ID": instance["ID"], "seriesDescription": series_desc} for instance in instance_list_data]
            )

        # Upload each instance
        total_files = len(instances_to_upload)
        progress[patientKey] = {"total": total_files, "completed": 0}

        for instance in instances_to_upload:
            if cancellation_flags.get(patientKey):  # Check for cancellation
                logger.info(f"Upload for patient {patientKey} has been cancelled.")
                return JSONResponse(content={"message": "Upload cancelled by user."}, status_code=200)

            try:
                content = await fetch_dicom_with_retries(f"{ORTHANC_SERVER_URL}/instances/{instance['ID']}/file")
                ds = dcmread(BytesIO(content))
                ds = mask_dicom(ds)

                memory_file = BytesIO()
                dcmwrite(memory_file, ds, write_like_original=False)
                memory_file.seek(0)

                safe_path = secure_filename(f"{instance['ID']}.dcm")
                firebase_path = f"{rootFolderPathortho}{instance['seriesDescription']}/{safe_path}"
                blob = bucket.blob(firebase_path)
                blob.upload_from_file(memory_file, content_type='application/dicom')

                file_url = blob.public_url
                results.append({"filename": firebase_path, "url": file_url})
                with progress_lock:
                    progress[patientKey]["completed"] += 1
            except Exception as e:
                logger.error(f"Error processing or uploading file: {e}")
                all_uploads_success = False
                break

        # If all uploads are successful, save data to Firebase
        if all_uploads_success and not cancellation_flags.get(patientKey):
            await save_patient_data_to_firebase(adminName1, patientKey, rootFolderPathortho, patientName, studyType, patientID, patientBirthDate, patientSex, studyDate, referringPhysicianName, modality, technicianName, StudyInstanceUid, seriesInstanceUid, PatientDataId)
            logger.info("Files have been successfully processed and uploaded!")
            return JSONResponse(content={"message": "Files have been successfully processed and uploaded!", "files": results})
        else:
            if cancellation_flags.get(patientKey):
                logger.info(f"Upload for patient {patientKey} was cancelled by the user.")
                return JSONResponse(content={"message": "Upload cancelled by user."}, status_code=200)
            logger.error("Failed to process or upload one or more files")
            return JSONResponse(content={"error": "Failed to process or upload one or more files"}, status_code=500)

    except Exception as e:
        if cancellation_flags.get(patientKey):
            logger.info(f"Upload for patient {patientKey} was cancelled by the user.")
            return JSONResponse(content={"message": "Upload cancelled by user."}, status_code=200)
        logger.error(f"Error fetching study data: {e}")
        return JSONResponse(content={"error": "Failed to process or upload study data"}, status_code=500)
async def save_patient_data_to_firebase(adminName1, patientKey, rootFolderPathortho, patientName, studyType, patientID, patientBirthDate, patientSex, studyDate, referringPhysicianName, modality, technicianName, StudyInstanceUid, seriesInstanceUid, PatientDataId):
    logger.info(f"Saving patient data to Firebase for patient {patientName} with key {patientKey}")
    
    # Sanitize patient name and key
    sanitizedPatientName = extract_name(patientName) if patientName else "NA"
    patientKey = f"Patient-{sanitize_firebase_key(sanitizedPatientName)}" if sanitizedPatientName != "NA" else "NA"

    # Compute age
    age = "NA"
    try:
        if patientBirthDate and patientBirthDate != "NA":  # Check if patientBirthDate is valid
            birth_year = int(patientBirthDate[:4])
            current_year = datetime.now().year
            age = current_year - birth_year
    except (ValueError, TypeError, IndexError):
        age = "NA"

    # Format study date and DOB
    formatted_study_date = "NA"
    try:
        if studyDate and studyDate != "NA":  # Check if studyDate is valid
            formatted_study_date = datetime.strptime(studyDate, "%Y%m%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        formatted_study_date = "NA"

    formatted_patient_birth_date = "NA"
    try:
        if patientBirthDate and patientBirthDate != "NA":  # Check if patientBirthDate is valid
            formatted_patient_birth_date = datetime.strptime(patientBirthDate, "%Y%m%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        formatted_patient_birth_date = "NA"

    # Determine gender
    genderLabel = "Unknown"
    if patientSex == "M":
        genderLabel = "Male"
    elif patientSex == "F":
        genderLabel = "Female"
    else:
        genderLabel = "NA"  # Assign "NA" if the gender is not provided or invalid

    # Prepare patient data
    patientData = {
        "Age": age,
        "Refered_By_Doctor": referringPhysicianName or "NA",  # Default to "NA" if not provided
        "Dicom_3D": "",
        "Dicom_3DURL": "",
        "Dicom_Report": "",
        "Dicom_ReportURL": "",
        "StudyDate": formatted_study_date,  # Use formatted study date or "NA"
        "DOB": formatted_patient_birth_date,  # Use formatted birth date or "NA"
        "MetaData_Orthanc": {
            "ID": PatientDataId or "NA",  # Default to "NA" if not provided
            "MainDicomTags": {
                "PatientID": patientID or "NA",  # Default to "NA" if not provided
                "PatientName": patientName or "NA",  # Default to "NA" if not provided
                "PatientBirthDate": patientBirthDate or "NA",  # Default to "NA" if not provided
                "PatientSex": patientSex or "NA",  # Default to "NA" if not provided
            },
            "SeriesInstanceUID": seriesInstanceUid or "NA",
            "StudyInstanceUID": StudyInstanceUid or "NA",
        },
        "FolderPath": rootFolderPathortho or "NA",  # Default to "NA" if not provided
        "FullName": sanitizedPatientName,  # Sanitized patient name or "NA"
        "Gender": genderLabel,  # Default to "NA" if not provided
        "ID": patientID or "NA",  # Default to "NA" if not provided
        "Timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),  # Current timestamp
        "Type_of_Dicom_Data": studyType or "NA",  # Default to "NA" if not provided
        "Prescription": "",
        "PrescriptionURL": "",
        "Role": "Patient",
        "Version": "02",
        "Modality": "MRI" if modality == "MR" else "XRAY" if modality == "CR" else modality or "NA",  # Default to "NA" if not provided
    }

    # Save patient data to Firebase
    db_ref = ref.child(f"superadmin/admins/{adminName1}/patients/{patientKey}")
    db_ref.set(patientData)  # No need to await set() as it's not an async function

    # Increment total uploads
    await increment_upload_count(adminName1, modality or "NA")

    # Log upload event
    await log_upload_event(adminName1, technicianName or "NA", sanitizedPatientName, modality or "NA")


async def increment_upload_count(adminName1, modality):
    modality_count_key = "MriUploads" if modality == "MR" else "CTUploads" if modality == "CT" else "XrayUploads" if modality == "CR" else None
    if not modality_count_key:
        logger.warning(f"Unknown modality: {modality}")
        return

    # Increment modality-specific count
    modality_count_ref = ref.child(f"superadmin/admins/{adminName1}/costing/{modality_count_key}")
    snapshot = modality_count_ref.get()  # No need to await get() as it's not an async function
    current_count = snapshot if isinstance(snapshot, int) else int(snapshot or 0)
    modality_count_ref.set(current_count + 1)  # No need to await set() as it's not an async function

    # Increment total upload count
    total_uploads_ref = ref.child(f"superadmin/admins/{adminName1}/costing/TotalUpload")
    snapshot = total_uploads_ref.get()  # No need to await get() as it's not an async function
    current_total_uploads = snapshot if isinstance(snapshot, int) else int(snapshot or 0)
    total_uploads_ref.set(current_total_uploads + 1)  # No need to await set() as it's not an async function

async def log_upload_event(adminName1, technicianName, patientName, modality):
    currentDate = datetime.now()
    monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    currentMonth = monthNames[currentDate.month - 1]
    currentYear = currentDate.year

    monthPath = f"superadmin/admins/{adminName1}/costing/Upload_Events/{currentMonth} {currentYear}"
    monthRef = ref.child(monthPath)

    snapshot = monthRef.get()  
    nextIndex = len(snapshot if snapshot else [])

    uploadData = {
        "TechnicianName": technicianName,
        "PatientName": patientName,
        "Modality": "MRI" if modality == "MR" else "XRAY" if modality == "CR" else modality,
        "timeStamp": currentDate.strftime("%d/%m/%Y, %H:%M:%S"),
    }

    monthRef.child(str(nextIndex)).set(uploadData)
    logger.info(f"Upload event logged for technician {technicianName}, patient {patientName}, modality {modality}")

@app.get('/progress/{patient_id}')
async def progress_status(patient_id: str):
    async def event_stream():
        while True:
            with progress_lock:
                progress_info = progress.get(patient_id, {"total": 0, "completed": 0})
                json_progress_info = json.dumps(progress_info)
            yield f"data: {json_progress_info}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_stream(), media_type='text/event-stream')

@app.get('/health')
async def health_check():
    return JSONResponse(content={"status": "ok"})

def mask_dicom(ds):
    if 'PatientName' in ds and ds.PatientName:
        ds.PatientName = mask_value(ds.PatientName)
    if 'PatientID' in ds and ds.PatientID:
        ds.PatientID = mask_value(ds.PatientID)
    if 'PatientBirthDate' in ds and ds.PatientBirthDate:
        ds.PatientBirthDate = mask_date(ds.PatientBirthDate)
    return ds

def secure_path(path):
    parts = path.split('/')
    safe_parts = [secure_filename(part) for part in parts]
    return os.path.join(*safe_parts)

def mask_value(value):
    if isinstance(value, pydicom.valuerep.PersonName):
        value = str(value)  

    masked_value = value[0] + '*' * (len(value) - 2) + value[-1] if len(value) > 1 else value
    return masked_value

def mask_date(date):
    return f"{date[0]}{'*'*(len(date)-2)}{date[-1]}" if date and len(date) == 8 else date

def extract_name(full_string):
    match = re.match(r'^[a-zA-Z.^ ]+', full_string)
    if not match: return None
    return re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z ]+', ' ', match.group(0))).strip()

def sanitize_firebase_key(key):
    return key.replace('/', '_')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)

import uvicorn

def main():
    uvicorn.run("easiofy_data_anonymization.api:app", host="127.0.0.1", port=5000, reload=True)

if __name__ == '__main__':
    main()
