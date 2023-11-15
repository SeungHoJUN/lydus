import os
import re

INPUT_DIR = 'data'
OUTPUT_DIR = 'deidentified_data'

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

for root, dirs, files in os.walk(INPUT_DIR):
    for filename in files:
        ipath = os.path.join(root, filename)
        odir = os.path.join(OUTPUT_DIR, root[len(INPUT_DIR) + 1:])
        os.makedirs(odir, exist_ok=True)
        opath = os.path.join(odir, os.path.basename(filename))

        print(ipath, '==>', opath, end='...', flush=True)
        text = open(ipath).read()
        text = re.sub('<(PatientID|PatientLastName|PatientFirstName|SiteName|LocationName|AcquisitionTime|AcquisitionDate|EditTime|EditDate|EditorLastName|EditorFirstName|AdmitDate|AdmitTime|OrderTime)>(.*)</\\1>', '<\\1></\\1>', text)
        with open(opath, "w") as f:
            f.write(text)

        print('done')
