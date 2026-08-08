# -*- coding: utf-8 -*-
"""Merge second-pass agent findings into corrections.json."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
c = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))

NEW = [
 # ortho
 {'qid':'q729','currentS':'Orthopaedics','currentT':'Ankylosing Spondylitis','correctS':'Orthopaedics','correctT':'Intertrochanteric Fracture','reason':'Dynamic hip screw treatment for intertrochanteric femur fracture'},
 # FM
 {'qid':'q1058','currentS':'Forensic Medicine','currentT':'Dehydration Assessment','correctS':'Forensic Medicine','correctT':'Snake Venom','reason':'Elapidae venom toxinology'},
 # ENT
 {'qid':'q228','currentS':'ENT','currentT':'Ear Reflexes','correctS':'ENT','correctT':'Arnold Reflex','reason':'Ear-cough reflex auricular branch of vagus'},
 # Biochem
 {'qid':'q291','currentS':'Biochemistry','currentT':'Phenylketonuria','correctS':'Biochemistry','correctT':'Tetrahydrobiopterin Deficiency','reason':'PAH present, BH4 cofactor deficiency'},
 # paeds
 {'qid':'q2023','currentS':'Paediatrics','currentT':'Uterovaginal Prolapse','correctS':'Paediatrics','correctT':'Low Birth Weight Feeding','reason':'Preterm formula for LBW infants'},
 {'qid':'q2027','currentS':'Paediatrics','currentT':'Cervical Cancer Staging','correctS':'Paediatrics','correctT':'Febrile Seizures','reason':'Febrile seizure recurrence risk age<1'},
 {'qid':'q2376','currentS':'Paediatrics','currentT':'Disaster Management','correctS':'Paediatrics','correctT':'Severe COVID Treatment','reason':'Corticosteroids for severe COVID child'},
 {'qid':'q2689','currentS':'Paediatrics','currentT':'Vomiting Reflex','correctS':'Medicine','correctT':'Ankylosing Spondylitis','reason':'Adult progressive spinal stiffness'},
 # derm
 {'qid':'q688','currentS':'Dermatology','currentT':'Hematuria','correctS':'Dermatology','correctT':'Leprosy Treatment','reason':'WHO MDT multibacillary leprosy'},
 # radiology
 {'qid':'q1875','currentS':'Radiology','currentT':'Cardiopulmonary Resuscitation','correctS':'Orthopaedics','correctT':'Trendelenburg Gait','reason':'Gluteal weakness Trendelenburg'},
 {'qid':'q2068','currentS':'Radiology','currentT':'Epidemic Typhus','correctS':'Paediatrics','correctT':'Rett Syndrome','reason':'Female-only neurodevelopmental disorder'},
 {'qid':'q2069','currentS':'Radiology','currentT':'Histoplasmosis','correctS':'Medicine','correctT':'Alcohol Withdrawal','reason':'Delirium tremens management'},
 {'qid':'q2070','currentS':'Radiology','currentT':'HIV Diagnosis in Infants','correctS':'Psychiatry','correctT':'Paraphilias','reason':'Paraphilia matching'},
 {'qid':'q2076','currentS':'Radiology','currentT':'Enterobius (Pinworm)','correctS':'Surgery','correctT':'Breast Lump Workup','reason':'Triple assessment cannot rule out malignancy'},
 {'qid':'q2250','currentS':'Radiology','currentT':'Breast Cancer Prognosis','correctS':'Paediatrics','correctT':'Rickets','reason':'Growth retardation wrist X-ray ALP>1500; NODIA garbage in stem'},
 {'qid':'q2251','currentS':'Radiology','currentT':'Burns','correctS':'OBG','correctT':'Gestational Diabetes','reason':'Diabetes in pregnancy management'},
 {'qid':'q2252','currentS':'Radiology','currentT':'Childhood Pneumonia','correctS':'OBG','correctT':'Antenatal Screening','reason':'Cost-effectiveness of prenatal screening'},
 {'qid':'q2253','currentS':'Radiology','currentT':'Neonatal Herpes','correctS':'Medicine','correctT':'Cystic Fibrosis','reason':'CBAVD in CF'},
 {'qid':'q2254','currentS':'Radiology','currentT':'Teratogenic Drugs','correctS':'Paediatrics','correctT':'Congenital Syphilis','reason':'Kassowitz rule'},
 {'qid':'q2255','currentS':'Radiology','currentT':'Neonatal Pulmonary Hypertension','correctS':'OBG','correctT':'Placental Hormones','reason':'hCG secreted by placenta'},
 {'qid':'q2256','currentS':'Radiology','currentT':'Dengue','correctS':'OBG','correctT':'Hereditary Breast-Ovarian Cancer','reason':'BRCA counseling'},
 {'qid':'q2257','currentS':'Radiology','currentT':'Rheumatoid Arthritis','correctS':'OBG','correctT':'Succenturiate Lobe','reason':'Placental image'},
 {'qid':'q2412','currentS':'Radiology','currentT':'Bacillus cereus Food Poisoning','correctS':'OBG','correctT':'Long-Acting Contraception','reason':'LARC methods'},
 {'qid':'q2413','currentS':'Radiology','currentT':'Hanging','correctS':'OBG','correctT':'PCOS','reason':'PCOS management teenager'},
 {'qid':'q2753','currentS':'Radiology','currentT':'ECG Diagnosis','correctS':'OBG','correctT':'Leg Cramps in Pregnancy','reason':'Midwifery advice nocturnal cramps'},
 {'qid':'q2754','currentS':'Radiology','currentT':'ACTH Therapy','correctS':'OBG','correctT':'Fetal Position','reason':'ROA fetal position'},
 {'qid':'q2755','currentS':'Radiology','currentT':'Cyanotic Heart Disease','correctS':'OBG','correctT':'Leopold Maneuvers','reason':'Lateral grip obstetric palpation'},
 {'qid':'q2756','currentS':'Radiology','currentT':'SIRS Criteria','correctS':'OBG','correctT':'Cord Prolapse','reason':'Cord prolapse Trendelenburg'},
 {'qid':'q2757','currentS':'Radiology','currentT':'HPV Vaccination','correctS':'OBG','correctT':'Partograph','reason':'4cm cervical dilation partograph'},
 {'qid':'q2758','currentS':'Radiology','currentT':'Genetic Screening','correctS':'OBG','correctT':'Cervical Cancer Screening','reason':'Pap smear screening'},
 {'qid':'q2759','currentS':'Radiology','currentT':'Typhoid Prevention','correctS':'OBG','correctT':'HPV Cervical Carcinogenesis','reason':'HPV oncoproteins'},
 {'qid':'q902','currentS':'Radiology','currentT':'Measures of Association','correctS':'Paediatrics','correctT':'Neonatal RDS','reason':'Preterm ground-glass surfactant deficiency'},
]

# attach to Radiology audit (or matching subject); simply append to the audit of matching currentS when it exists
def audit_of(subj):
    for a in c['audits']:
        if a['subj'] == subj:
            return a['result']
    return None

n = 0
for x in NEW:
    r = audit_of(x['currentS'])
    if r is None:
        print('NO AUDIT FOR', x['currentS'], x['qid']); continue
    r['qidIssues'].append(x)
    n += 1
print('merged', n)
json.dump(c, open(r'F:\NEET PG\research\corrections.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
