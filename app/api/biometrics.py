from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import Annotated

# THIS LINE IS CRITICAL: It defines the 'router' variable
router = APIRouter(
    prefix="/biometrics",
    tags=["Biometrics"]
)

# Dependency to check for user_id existence
def get_user_id(user_id: str):
    """Placeholder for checking if the user ID is provided."""
    if not user_id:
        # FastAPI will usually catch this via schema, but good practice to ensure
        raise HTTPException(status_code=400, detail="User ID is required.")
    return user_id

@router.post("/verify-face")
async def verify_user_face(
    user_id: Annotated[str, Depends(get_user_id)],
    face_image: UploadFile = File(...)
):
    """
    Simulates a secure biometric verification process.
    The verification result is based on the uploaded filename for quick demo purposes.
    """
    
    # --- HACKATHON MOCKING LOGIC: Check filename ---
    filename = face_image.filename.lower()
    
    if "authorized" in filename:
        # Success case: The user uploaded the 'authorized' file
        verification_status = True
        confidence_score = 0.98
        
    elif "unauthorized" in filename:
        # Failure case: The user uploaded the 'unauthorized' file
        verification_status = False
        confidence_score = 0.45
        
    else:
        # Default for any other file (treat as success for a neutral demo)
        verification_status = True
        confidence_score = 0.85

    # You must read the file data to finalize the upload and prevent connection issues
    # In a real app, you would send this 'bytes' object to the biometric API
    image_bytes = await face_image.read()
    
    # --- FINAL RESPONSE ---
    if verification_status:
        # Successful response
        print(f"✅ Biometric Match for User {user_id}. Score: {confidence_score:.2f}. File Size: {len(image_bytes)/1024:.2f} KB")
        return {
            "user_id": user_id,
            "status": "success",
            "message": "Biometric Identity Verified",
            "confidence": confidence_score,
            "token": "BIO_ACCESS_TOKEN_XYZ"  # A temporary access token
        }
    else:
        # Failed verification response
        print(f"❌ Biometric Verification FAILED for User {user_id}.")
        # Use a standard 401 Unauthorized error
        raise HTTPException(
            status_code=401,
            detail="Biometric verification failed. User identity not confirmed."
        )