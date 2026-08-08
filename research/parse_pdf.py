import io, re, json

t = io.open('research/neetpg-yearwise.txt', encoding='utf-8').read()
pages = t.split('===PAGE ')
# page idx -> book page is idx-2 (first===PAGE 0? verify via PAGE marks
# toc book pages: papers 5-77, 78-134(?) use header scan.

# Book page ranges from contents: 2025 5-31, SOL 32-77, 2024 78-134, SOL 135-226,
# 2023 227-254, SOL 255-294, 2022 295-324, SOL 325-371, 2021 372-397, SOL 398-438,
# 2020 439-473, SOL 474-542, 2019 543-573, SOL 574-641, 2018 642-669, SOL 670-741
# Plus intro pages ~1-3. So page index i (0-based) ~ book page i+1 with correction.
# Instead: locate question-paper start/end by scanning page header blocks.

def find_pp_start(ppage):
    # find page whose text begins with 'EXAMINATION PAPER <year>' (book page ppage)
    for i, p in enumerate(pages):
        if f'EXAMINATION PAPER {ppage}' in p[:200] and 'SOLUTION' not in p[:200]:
            return i
    return None

def next_start(year):
    # end of paper body = start of next paper (2025->solution; others-> next paper)
    for i, p in enumerate(pages):
        if 'EXAMINATION PAPER {y} SOLUTION'.format(y=year) in p[:300]:
            return i
    return None

# Locate each paper by author headers
starts = {}
for y in [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018]:
    starts[y] = find_HEAD_start(y)

starts_sol = {}
for y in list(starts):
    starts_sol[y] = next_start(y)

print('paper idx:', {y: (s, starts_sol.get(y)) for y, s in starts.items()})

SUBJ = {
 'ANATOMY':'Anatomy','BIOCHEMISTRY':'Biochemistry','PHYSIOLOGY':'Physiology',
 'PATHOLOGY':'Pathology','PHARMACOLOGY':'Pharmacology','MICROBIOLOGY':'Microbiology',
 'FORENSIC MEDICINE':'Forensic Medicine','FORENSICS':'Forensic Medicine','FMT':'Forensic Medicine',
 'COMMUNITY MEDICINE':'PSM','COMMUNITY MED':'PSM','PSM':'PSM','PREVENTIVE':'PSM',
 'ENT':'ENT','OPHTHALMOLOGY':'Ophthalmology','OPHTHALMO':'Ophthalmology','OPTHALMOLOGY':'Ophthalmology',
 'GENERAL MEDICINE':'Medicine','MEDICINE':'Medicine','CLINICAL MEDICINE':'Medicine',
 'SURGERY':'Surgery','GENERAL SURGERY':'Surgery','GEN SURGERY':'Surgery',
 'OBG':'OBG','OBS & GYNE':'OBG','OBS&GYNE':'OBG','OBSTETRICS':'OBG','GYNAECOLOGY':'OBG','GYNECOLOGY':'OBG',
 'PAEDIATRICS':'Paediatrics','PEDIATRICS':'Paediatrics',
 'PSYCHIATRY':'Psychiatry','PSYCHAE','PSYCHAE: Psychiatry',
 'ANAESTHESIA':'Anaesthesia','ANESTHESIA':'Anaesthesia','ANAESTHESIOLOGY':'Anaesthesia',
 'RADIOLOGY':'Radiology','RADIO DIAGNOSIS':'Radiology','RADIODIAGNOSIS':'Radiology',
 'ORTHOPAEDICS':'Orthopaedics','ORTHOPEDICS':'Orthopaedics','ORTHO':'Orthopaedics',
 'DERMATOLOGY':'Dermatology','SKIN':'Dermatology'}

def canon(s):
    u = re.sub(r'\s+', ' ', s.strip()).upper().rstrip('.,:')
    return SUBJ_SET.get(u, None)

hdr_words = {'ANATOMY','BIOCHEMISTRY','PHYSIOLOGY','PATHOLOGY','PHARMACOLOGY','MICROBIOLOGY',
 'FORENSIC','PSM','COMMUNITY','MEDICINE','SURGERY','GEN','GENERAL','OBG','OBS','GYNE','GYNAECOLOGY'}
