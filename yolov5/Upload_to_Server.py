import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

# Firebase 인증서 위치
certi_route = "capstone-continue-firebase-adminsdk-ubpi1-68bc0133b4.json"

# Firebase initialize
cred = credentials.Certificate(certi_route)
firebase_admin.initialize_app(cred, {
        'projectId' : 'capstone-continue',
        'storageBucket': 'capstone-continue.appspot.com'
})
bucket = storage.bucket()
db = firestore.client()

# Upload(raw data : 0, 시간, 장소, case, class_num, image)
def Upload(time, place, case, class_num, raw_image_route, result_image_route):

    filename = raw_image_route
    save_in = "Detected_raw_images/"
    blob_raw = bucket.blob(save_in + filename)
    blob_raw.upload_from_filename(filename)
    blob_raw.make_public()

    filename = result_image_route
    save_in = "Detected_result_images/"
    blob_result = bucket.blob(save_in + filename)
    blob_result.upload_from_filename(filename)
    blob_result.make_public()

    doc_ref = db.collection(u'Detection').document(u'json')
    doc_ref.set({
        u'time': time,
        u'place': place,
        u'case': case,
        u'class': class_num,
        u'raw_imageURL': blob_raw.public_url,
        u'result_imageURL' : blob_result.public_url
    })

    print("Upload Finished")

Upload('2020', "ai center", 1, 1, "1.jpg", "2.jpg")
