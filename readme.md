conda create -n docparser python=3.11 -y
                                                                      
conda activate docparser
python --version
mkdir document_parser
cd document_parser
touch requirements.txt
touch extractor.py


# 5) Run server
uvicorn main:app --reload --port 8001
Uvicorn running on http://127.0.0.1:8001


curl -X POST "http://127.0.0.1:8001/extract/dividend" \
  -F "file=@/Users/parteekslathia/Documents/work/ASX/annocements/TESTV1/resource/agl_dividend.pdf"


curl -X POST "http://127.0.0.1:8001/extract/dividend" \
  -F "file=@/Users/parteekslathia/Documents/work/ASX/annocements/TESTV1/resource/BHP_dividend.pdf"