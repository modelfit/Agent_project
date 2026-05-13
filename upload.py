# upload.py (run separately)
from rag.uploader import upload_file
import sys

result = upload_file(sys.argv[1])
print(result)