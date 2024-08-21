import os
import base64
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

expected_leads = ['I', 'II', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

INPUT_DIR = 'data'
for root, dirs, files in os.walk(INPUT_DIR):
    for filename in files:
        ipath = os.path.join(root, filename)
        print('Parsing ' + ipath)
        x = ET.parse(ipath).iter('LeadData')
        ilead = 0
        ecg_waveforms = []
        for c in x:
            # 500 hz * 10초 * 8 채널
            nsamp = int(c.find('LeadSampleCountTotal').text)
            if nsamp != 5000:
                continue
            lead = c.find('LeadID').text
            amp = float(c.find('LeadAmplitudeUnitsPerBit').text)
            if amp != 4.88:
                print(f'lead amp error in {ipath}')
                quit()
            if expected_leads[ilead] != lead:
                print(f'lead name error in {ipath}')
                quit()
            buf = base64.b64decode(c.find('WaveFormData').text)
            data = np.frombuffer(buf, '<i2', nsamp)
            ecg_waveforms.append(data)
            ilead += 1
        
        vals = np.array(ecg_waveforms)  # 8 x 5000
        vals = vals.flatten()
        
        plt.figure(figsize=(20,1))
        plt.plot(vals)
        plt.savefig(f'{filename}_{lead}.png')
        plt.close()
        quit()

# 실제 데이터는 i, ii, v1-6 까지 8개만 있다. 나머지 4개는 아래와 같이 만들어냄
# III = II - I
# aVR = -(I + II)/2
# aVL = I - II/2
# aVF = II - I/2
