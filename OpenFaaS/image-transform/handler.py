from base64 import decodebytes, encodebytes
from json import loads
from albumentations.augmentations import AdvancedBlur
from tempfile import NamedTemporaryFile
import cv2


def transform(image: bytes, transformation_callback) -> bytes:
    with NamedTemporaryFile() as og, NamedTemporaryFile(suffix='.jpeg') as result:
        og.write(image)
        narray = cv2.imread(og.name)
        transformed = transformation_callback(image=narray)['image']
        cv2.imwrite(result.name, transformed)
        transformed = result.read()
    return transformed

advanced_blur = AdvancedBlur(always_apply=False, p=1.0, blur_limit=(3, 39), sigmaX_limit=(0.2, 1.0), sigmaY_limit=(0.2, 5.44), rotate_limit=(-90, 90), beta_limit=(0.5, 8.0), noise_limit=(0.9, 1.1))

def handle(event, context):
    payload = loads(event.body)
    image = decodebytes(payload["image"].encode(encoding='UTF-8'))
    
    transformed = transform(image, advanced_blur)

    return {
        "statusCode": 200,
        "body": {"response": encodebytes(transformed).decode(encoding='UTF-8')}
    }
