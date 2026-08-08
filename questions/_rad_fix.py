import json

p = "F:/NEET PG/questions/_rad_new.json"
d = json.load(open(p, encoding="utf-8"))

# Fix garbled text in place
fixes = {
    2: {"q": "Routine personal dosimetry of diagnostic radiology personnel in India is monitored today with which device?"},
    7: {"ex": "The oval of gas under the ventral wall in a supine neonate is the football sign; Rigler sign is loop lamination."},
    24: {"ex": "A dilated oesophagus tapering to a smooth beak at the cardia with delayed emptying fits achalasia."},
    25: {"q": "Low-grade fever with an ileocaecal stricture, a contracted scarred caecum and a central contrast fleck on barium in a young Indian adult:", "ex": "A goblet caecum with terminal-ileal narrowing is the ileocaecal-TB pattern of a febrile young adult."},
    29: {"q": "An elderly obstructed patient has a plain film and CT showing abundant intraluminal gas, air lucencies over the hepatic shadow and a remote calcified stone lodged in a mid small-bowel loop. The unifying diagnosis is:"},
    43: {"ex": "The Westermark sign of regional oligaemia and an enlarged pulmonary artery is a strong hint for acute PE."},
}
for i, patch in fixes.items():
    for k, v in patch.items():
        d[i][k] = v

# Replace item 18 (duplicate of 22) with TAPVC snowman
d[18] = {"q": "An infant with mild cyanosis and heart failure has a chest film showing a cardiac silhouette shaped like a snowman on a pedestal. Which diagnosis best fits this configuration?",
    "o": ["Total anomalous pulmonary venous return (supracardiac)", "Coarctation of the aorta", "Transposition of great vessels", "Dilated cardiomyopathy"],
    "a": 0, "ex": "In supracardiac TAPVR the dilated vertical vein and SVC give the classic snowman or figure-of-eight sign on the film.",
    "e": "NEET PG", "y": "2022"}

# Replace item 44 (silicosis, existing bank already has it) with air crescent aspergilloma
d[44] = {"q": "In a patient with a pre-existing upper-lobe cavity from old tuberculosis, a new fungal ball fills the cavity and a crescent of air separates it from the cavity wall on the radiograph. The lesion is:",
    "o": ["Mycetoma (aspergilloma)","Hydatid daughter cyst","Lung abscess with debris","Bronchogenic carcinoma"],
    "a": 0, "ex": "The air-crescent (Monod) sign between the fungus ball and the cavity wall is typical of an aspergiloma.", "e": "NEET PG","y": "2021"}

json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", len(d))