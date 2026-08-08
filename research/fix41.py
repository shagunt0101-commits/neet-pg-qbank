# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
c = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
MAP = {
 'q1262': ('Microbiology','Graft Rejection'),
 'q1493': ('Anatomy','Oogenesis'),
 'q1494': ('OBG','Bacterial Vaginosis'),
 'q1495': ('OBG','Infertility'),
 'q1496': ('OBG','Bacterial Vaginosis'),
 'q1497': ('OBG','Amenorrhea'),
 'q1605': ('Medicine','Aphasia'),
 'q1654': ('Medicine','Lung Cancer'),
 'q1664': ('Medicine','Lateral Medullary Syndrome'),
 'q1666': ('Paediatrics','Vaccination Contraindications'),
 'q1667': ('Paediatrics','Rabies Prophylaxis'),
 'q1672': ('Paediatrics','Diamond-Blackfan Anemia'),
 'q1673': ('Paediatrics','Kawasaki Disease'),
 'q1674': ('Paediatrics','Vaccination Contraindications'),
 'q1675': ('Paediatrics','Scorpion Sting'),
 'q1676': ('Paediatrics','Sickle Cell Crisis'),
 'q1684': ('OBG','Uterine Fibroids'),
 'q1685': ('Paediatrics','Congenital Infections'),
 'q1686': ('OBG','Leukorrhea'),
 'q1687': ('OBG','Bacterial Vaginosis'),
 'q1688': ('OBG','Endometriosis'),
 'q1689': ('OBG','Disorders of Sex Development'),
 'q1690': ('OBG','Uterovaginal Prolapse'),
 'q1691': ('Anatomy','Male Reproductive System'),
 'q1692': ('OBG','Hormone Replacement Therapy'),
 'q1852': ('Paediatrics','Pneumonia (IMCI)'),
 'q1853': ('Paediatrics','Neonatal HSV'),
 'q1854': ('OBG','Perinatal Infections'),
 'q1855': ('Paediatrics','Persistent Pulmonary Hypertension of Newborn'),
 'q1856': ('Paediatrics','Dengue'),
 'q219': ('Anatomy','Brachial Plexus Injuries'),
 'q2347': ('Orthopaedics','Fracture Fixation'),
 'q2395': ('Paediatrics','H. influenzae Meningitis'),
 'q2584': ('Medicine','Neuromyelitis Optica'),
 'q2585': ('Medicine','Movement Disorders'),
 'q2706': ('Anaesthesia','Intravenous Cannulation'),
 'q2709': ('Anaesthesia','Injection Technique'),
 'q2710': ('Surgery','Head Injury'),
 'q2734': ('Orthopaedics','Osteoporosis'),
 'q2735': ('Orthopaedics','Osteosarcoma'),
 'q2738': ('Orthopaedics','Scoliosis Braces'),
}
n = 0
for a in c['audits']:
    for x in a['result'].get('qidIssues') or []:
        if x['qid'] in MAP:
            x['correctS'], x['correctT'] = MAP[x['qid']]
            n += 1
print('mapped', n)
json.dump(c, open(r'F:\NEET PG\research\corrections.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
