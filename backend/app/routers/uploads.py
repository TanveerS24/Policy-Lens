import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from bson import ObjectId

from app.config.settings import settings
from app.database.client import get_db
from app.models.upload import UploadInDB
from app.schemas.upload import PublishRequest, UploadResponse
from app.services.pdf_service import chunk_text, extract_text_from_pdf
from app.services.rag_service import rag_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDFs are supported")

    contents = await file.read()
    filename = f"{uuid.uuid4()}.pdf"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        f.write(contents)

    # Extract text and generate summary.
    text = extract_text_from_pdf(contents)
    summary = await rag_service.summarize_policy(text, title=file.filename)

    db = get_db()

    upload_doc = {
        "filename": file.filename,
        "stored_filename": filename,
        "content_type": file.content_type,
        "size": len(contents),
        "owner_id": user.id,
        "status": "pending",
        "summary": summary,
    }
    result = await db["uploads"].insert_one(upload_doc)
    return UploadResponse(**{**upload_doc, "_id": str(result.inserted_id)})


@router.get("/my", response_model=list[UploadResponse])
async def list_my_uploads(user=Depends(get_current_user), db=Depends(get_db)):
    cursor = db["uploads"].find({"owner_id": user.id}).sort([("_id", -1)])
    items = [UploadResponse(**{**doc, "_id": str(doc.get("_id"))}) async for doc in cursor]
    return items


@router.delete("/{upload_id}")
async def delete_upload(upload_id: str, user=Depends(get_current_user), db=Depends(get_db)):
    if not ObjectId.is_valid(upload_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid upload id")
    upload = await db["uploads"].find_one({"_id": ObjectId(upload_id), "owner_id": user.id})
    if not upload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Upload not found")

    # delete file from disk if exists
    stored = upload.get("stored_filename")
    if stored:
        try:
            os.remove(UPLOAD_DIR / stored)
        except Exception:
            pass
    await db["uploads"].delete_one({"_id": ObjectId(upload_id)})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


@router.post("/publish")
async def publish_upload(request: PublishRequest, user=Depends(get_current_user), db=Depends(get_db)):
    if not ObjectId.is_valid(request.upload_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid upload id")
    upload = await db["uploads"].find_one({"_id": ObjectId(request.upload_id), "owner_id": user.id})
    if not upload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Upload not found")

    # Create policy draft entry pending approval
    summary = upload.get("summary") or {}
    policy_doc = {
        "title": summary.get("title") or upload.get("filename"),
        "short_description": summary.get("short_description"),
        "summary": summary.get("summary"),
        "eligibility_criteria": summary.get("eligibility_criteria"),
        "benefits": summary.get("benefits"),
        "notes": summary.get("notes"),
        "category": "",
        "state": "",
        "pdf_url": None,
        "approved": False,
        "created_by": user.id,
    }
    result = await db["policies"].insert_one(policy_doc)
    await db["uploads"].update_one({"_id": ObjectId(request.upload_id)}, {"$set": {"policy_id": str(result.inserted_id)}})

    # store embeddings for RAG
    text = extract_text_from_pdf((UPLOAD_DIR / upload.get("stored_filename")).read_bytes())
    chunks = chunk_text(text)
    await rag_service.store_chunks(str(result.inserted_id), chunks)

    return {"policy_id": str(result.inserted_id)}
