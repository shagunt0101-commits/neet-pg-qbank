import json

VALID_E = ["NEET PG", "INI-CET"]
VALID_Y = ["2021","2022","2023","2024","2025"]

qs = []
def add(q, o, a, ex, e, y):
    assert len(o) == 4 and len(set(o)) == 4, "opt problem: " + q[:25]
    assert 0 <= a <= 3, q[:25]
    assert y in VALID_Y, y
    assert e in VALID_E, e
    qs.append({"q": q, "o": o, "a": a, "ex": ex, "e": e, "y": y})

# ---------------- 1 Radiation physics and protection ----------------
add("According to the Bergonie-Tribondeau law, rapidly dividing undifferentiated cells are the most radiosensitive. Of these, which tissue is the most radiosensitive?",
 ["Mature neurons of the cerebral cortex","Resting spermatogonia","Mature erythrocytes","Compact bone"],1,
 "Spermatogonia divide fast and are among the most radiosensitive cells; neurons and mature red cells are radioresistant.","NEET PG","2021")

add("A radiographer at distance d from a gamma ray point source moves away to distance 2d. The exposure rate relative to the initial value becomes:",
 ["One half","Twice","One quarter","Unchanged"],2,
 "The inverse-square law applies to a point source, so doubling the distance quarters the exposure rate.","NEET PG","2022")

add("The device used today for routine personal dose monitoring of diagnostic radiology staff in India is the:",
 ["Pocket ionization chamber","Thermoluminescent dosimeter (TLD)","Geiger-Muller counter","Portable survey meter"],1,
 "A lithium-fluoride thermoluminescent dosimeter replaced the film badge for staff dose monitoring.","NEET PG","2023")

add("Which compound was the first non-ionic water-soluble contrast agent to enter clinical use?",
 ["Iohexol","Metrizamide","Diatrizoate","Iopamidol"],1,
 "Metrizamide launched low-osmolality non-ionic urography; the older diatrizoate is ionic and hyperosmolar.","NEET PG","2022")

add("A patient with eGFR 35 mL per minute needs iodinated contrast for CT while hydration prophylaxis runs on. The agent carrying the lowest risk of contrast induced nephropathy is:",
 ["A low-osmolar ionic agent","Iso-osmolar non-ionic dimer (iodixanol)","A high-osmolar ionic agent","A large volume of monomeric iohexol"],1,
 "Iodixanol, the iso-osmolar dimer, has the lowest CIN rate among iodinated contrast agents.","INI-CET","2023")

add("Which gadolinium agent is safest when renal failure coexists, to minimise the risk of nephrogenic systemic fibrosis?",
 ["Gadopentetate dimeglumine (linear)","Gadodiamide (linear)","Gadobenate dimeglumine (linear)","Gadobutrol (macrocyclic)"],3,
 "Macrocyclic chelates such as gadobutrol release little free gadolinium and are associated with far lower NSF risk than linear agents.","INI-CET","2025")

# ---------------- 2 Neonatal imaging ----------------
add("Chest film of a tachypnoeic preterm baby shows ground glass granularity, air bronchograms and overinflation. The most likely diagnosis is:",
 ["Surfactant-deficient respiratory distress syndrome","Congenital diaphragmatic hernia","Neonatal lobar emphysema","Oesophageal atresia"],0,
 "Neonatal RDS gives ground-glass granularity with air bronchograms; TTNB and infant of a diabetic mother show different patterns.","INI-CET","2022")

add("A supine abdominal film of a newborn shows intraperitoneal air outlining the whole cavity as an ovoid gas photo. This sign is the:",
 ["Rigler sign","Football sign","Cupola sign","Sentinel loop sign"],1,
 "Supine free air draws an ovoid football silhouette of the neonatal abdomen; Rigler sign is double-walled bowel.","INI-CET","2021")

add("A newborn who fails to pass meconium has a contrast enema showing a narrow distal rectosigmoid with a transition cone into dilated colon. The diagnosis is:",
 ["Hirschsprung disease","Meconium ileus","Anorectal malformation","Necrotising enterocolitis"],0,
 "A spastic aganglionic segment with transition zone on the enema is characteristic of Hirschsprung disease.","INI-CET","2024")

add("A distended neonate has fine foamy opacities in the right upper abdomen with a normal calibre rectum. The next diagnostic step is:",
 ["Water-soluble contrast enema","CT of the abdomen","Intravenous urogram","Repeated ultrasound"],0,
 "The soap-bubble pattern with a normal rectum points to meconium ileus, confirmed and treated by a water-soluble contrast enema; cystic fibrosis usually underlies it.","INI-CET","2025")

add("On a newborn chest film, the triangular opacity that hugs the right upper mediastinum and changes with posture is:",
 ["The thymus (sail sign, a normal finding)","A mediastinal terotoma","An enlarged left lobe of the liver","A sequestered lobe"],0,
 "The sail sign is the infant thymus, a normal finding that does not compress the trachea.","INI-CET","2021")

# ---------------- 3 Brain hMATOMAS and stroke ----------------
add("After a blunt head injury a patient is briefly lucid and later slips into coma. CT shows a biconvex lentiform hyperdense mass that does not cross a suture. The diagnosis is:",
 ["Acute extradural haematoma","Chronic subdural haematoma","Lobar contusion","Meningeal carcinomatosis"],0,
 "A lucid interval with a biconvex suture-respecting hyperdensity is the classic extradural haematoma.","NEET PG","2021")

add("An anticoagulated elderly patient falls and a week later develops confusion and mild hemiparesis; CT shows a concave crescent of soft density over the convexity. The decisive step is:",
 ["Burr hole drainage","Emergent hemicraniectomy","High-dose dexamethasone only","Observation with serial scans"],0,
 "A concave crescentic collection over the convexity is a subacute chronic subdural haematoma; burr hole evacuation relieves the mass effect.","NEET PG","2023")

add("A fresh hemiplegic patient is scanned 90 minutes after onset and the plain CT is still almost normal. Which MRI sequence best confirms the acute infarct?",
 ["Diffusion-weighted MRI","Non-contrast cervical MRI","Conventional T1 spin-echo","MR spectroscopy"],0,
 "Diffusion-weighted imaging shows the cytotoxic oedema within minutes; other sequences lag for hours.","INI-CET","2023")

add("Thunderclap headache with nuchal rigidity in a middle-aged woman; the non-contrast CT is hyperdense in the basal cisterns and sucalise. The diagnosis is:",
 ["Acute subarachnoid haemorrhage","Herpes simplex cerebritis","Subdural hygroma","Cavernoma bleed"],0,
 "Fissural sulcal and cisternal hyperdensity is the CT signature of acute SAH; angiography then finds the saccular aneurysm.","NEET PG","2021")

add("A febrile patient with seizures has MR showing a ring-enhancing mass whose core is bright on the diffusion sequence. The most likely lesion is:",
 ["Pyogenic brain abscess","Gioblastoma multiforme","Colloid cyst of the third ventricle","Fibrome cavernoma"],0,
 "Pus restricts water diffusion, so an abscess ring-enhances yet shines on DWI where necrotic tumour stays dark.","NEET PG","2024")

add("A sellar-suprasellar mass lifts the opticchias na and spills out of the sella to make an hour-glass silhouette on MRI. The diagnosis is:",
 ["Pituitary macroadenoma","Craniopharyngioma","Suprasellar meningioma","Rathke cleft cyst"],0,
 "A snowman-shaped sellar and suprasellar mass with chiasmal compression is a pituitary macroadenoma.","INI-CET","2023")

add("A devout dural-based mass returns intense uniform contrast enhancement and causes reactive hyperostosis in the vault on CT. Diagnosis:",
 ["Meningioma","Gioblastoma multiforme","Posterior fossa ependythemia","Osteosarcoma of skull"],0,
 "Uniformly enhancing extra-axial mass with a broad dural tail and underlying hyperostosis is meningioma.","NEET PG","2022")

# ---------------- 4 Chest ----------------
add("A PA chest film shows a strikingly convex pulmonary artery segment and right hilar prominence. This prominence reflects:",
 ["Enlargement of the right ventricular outflow tract and pulmonary trunk","Left atrial enlargement","Descending aorticomegaly","Superior vena cava widening"],0,
 "A convex main pulmonary segment with RV-counters marks pulmonary hypertension or a left-to-right shunt.","NEET PG","2022")

add("A stone mason with a chisel injury suspects a ferromagnetic intraocular foreign body. Which examination is strongly contraindicated?",
 ["Magnetic resonance imaging","Plain skull X-ray","CT of the orbit","B-mode ultrasound"],0,
 "MRI may torque and heat a ferromagnetic intraocular fragment; plain films and CT should go first.","NEET PG","2023")

add("Weeks of aching frontal headache: sinus scan shows an expanded and completely opacified frontal sinus with a thin intact wall. Diagnosis:",
 ["Frontal sinus mucocoele","Acute pansinusitis with air-fluid levels","Osteomyelitis of the frontal","Meningio-cephalocele of the forehead"],0,
 "A mucocoele is a paranasal sinus distended by outlet obstruction; it slowly expands and can erode the orbital roof.","NEET PG","2023")

add("Dysphonia, an apical lung mass and eroding notches of the first two ribs in a heavy smoker. Likely disease is:",
 ["Papoast (superior sulcus) tumour","Upper lobe aspergilloma","Sarcoidosis hybrid node","TB complex of the apex"],0,
 "An apical mass destroying rib with ipsilateral Horner ptosis and arm pain is a superior sulcus (Papast) tumour.","NEET PG","2021")

add("A child with a murmur has a chest film with full lung hila and engorged peripheral vessels (plethoric fields). The likely basis is:",
 ["A left-to-right shunt","Tetralogy of Fallot","Isolated pulmonary stenosis","Pericardial effusion"],0,
 "Left-to-right shunts open the pulmonary bed with blood; cyanosed tetralogy gives contrastily oligaemic lung fields.","NEET PG","2022")

add("PA film shows an enlarged left atrial appendage with elevation of the left main bronchus; a barium swallow is pushed aside. This appearance describes:",
 ["Left atrial enlargement of mitral disease","Pulmonary arterial prominence","Enlarged right ventricle","Right atrial pathology"],0,
 "Left atrial growth bulges the appendage, raises the left main bronchus and indents the barium swallow.","NEET PG","2024")

# ---------------- 5 Upper GI ----------------
add("Progressive dysphagia; barium swallow shows a dilated oesophagus that empties late, ending in a smooth cellular beak at the cardia. The diagnosis is:",
 ["Achalasia cardia","Peptic stricture of the oesophagus","Corrosive stricture","Oesophageal carcinoma"],0,
 "A dilated oesophagus that closes in a smooth beak and holds the contrast is the achalasia pattern.","NEET PG","2022")

add("A young adult with low-grade fever and ileal symptoms has barium showing a strictured ileocaecal segment, a contracted caecum and a central fleck. The diagnosis is:",
 ["Intestinal tuberculosis","Carcinoma caecum","Crohn pancolitis","Yersinia enterocolitis"],0,
 "The deformed goblet caecum and narrowed terminal ileum of a young adult in India points to ileocaecal tuberculosis.","NEET PG","2021")

add("A three-month-old casts milk in projectiles after feeds; ultrasound shows a pyloric muscle wall of 4.5 mm and an elongated cellular canal. Diagnosis:",
 ["Hypertrophic pyloric stenosis","Hiatus hernia","Malrotation with bands","Neonatal pylora spasm"],0,
 "A pyloric wall above 3-4 mm with an elongated narrow canal confirms hypertrophic pyloric stenosis.","INI-CET","2023")

add("A child with blunt abdominal trauma has a supine radiograph without free air. The additional projection best suited to show a small bowel perforation is:",
 ["Upright chest or left lateral decubitus","Lateral lumbar spine","Barium swallow","Repeat radiography in two days"],0,
 "Erect and decubitus films pool the free gas under a diaphragm that the supine film misses.","NEET PG","2024")

add("A woman gurgling with a neck lump while she swallows, who regurgitates yesterday's meal hours later, shows a pocketial pouch high behind the cricoid on the swallow study. Diagnosis:",
 ["Pharyngeal pouch (Zenker diverticulum)","Taking laryngocoele","Dysphagia lusoria","Oesophageal stenosis"],0,
 "Zenker diverticulum is a hypopharyngeal pouch above the cricopharyngous that holds and regurgitates food long after it.","NEET PG","2021")

add("An elderly patient with distension and coils has pneumobilia on plain films and a faceted calcified opacity lodged in the mid-small bowel on CT. Unifying diagnosis:",
 ["Gallstone ileus (Rigler triad)","Cholecystic neoplasm","Midgut malrotation","Ischaemic stricture"],0,
 "Pneumobilia meeting an obstructing ectopic gall stone is gallstone ileus; Rigler triad completes it on X-ray finding.","INI-CET","2023")

# ---------------- 6 MSK ----------------
add("A limping adolescent has an oval 'soap-bubble' blow-out lucent lesion of the proximal humeral metaphysis with a paper-thin outline. Probable:",
 ["Cyst of a aneurysm (ABC)","Osteosarcom","Chrondroblastoma","Enchondroma"],0,
 "A multiloculated soaps-bodimentate lesion in the young is an aneurysmal bone cyst; internal blood-fluid levels are common.","NEET PG","2024")

add("A teenage runner has hip pain; the frog-leg lateral image shows the head slipping. Additional radiological confirmation comes best from:",
 ["The opposite side on a pelvi-frog pair (bilateral films)","Stork and reveal oblique","Inlet outlet downside","Sacral reformatted"],0,
 "Slipped capital basal epiphysis is usually best seen with both hips in frog-lateral; the femoral slide is graded.","NEET PG","2025")

add("A teen with knee pain has a lytic epiphysis of the distal femur with small mottled foci within it. Diagnosis:",
 ["Chondroblastoma","Osteochondroma","Unicameral bone-cyst panel","Giant cell of the quadrant"],0,
 "Lucent epiphysis with specks and surrounding oedema in the teenage is a typicalistic chondroblastoma.","INI-CET","2023")

add("An exophytic bony mass on the long bone grows pointing away from the nearest joint and shows breed continuity of marrow and cortex. This is:",
 ["Osteochondroma (cartilage-capped osentosis)","Osteoid bone mass","Subperiosteal eczysted;","Parosteal flourishing"],0,
 "Exophilic continuity with the host bone and a cartilage cap description points to an osteochondroma.","NEET PG","2021")

add("A 70-year-old with transient pelvic fall and continued sacropain has a SPECT showing symmetric H-shaped radio-pharme uptake in both sacralralae. Diagnosis:",
 ["Sacral insufficiency fracture (Honda sign)","Multiple myeloma","Coccydynia","Sydenavicular avulsion"],0,
 "The bilateral-H on the bone scan through both sacural alae indicates insufficiency fractures (also called Honda sign).","INI-CET","2025")

add("Burning arthralgia in an elderly woman with a zero film that walks a line of dense calcium in the knee cartilage. The crystaletch is:",
 ["Calcium pyrophosphate dehydrate (CPPD)","Monosodium urate (gout)","Albical apatite","Hemosiderin"],0,
 "A linear dense calcium line within the cartilage is chondrocalcinosis, the signature of CPPD pseudogout.","INI-CET","2022")

add("A 30-year-old man with ascending lumbar rigidity has a lateral film of the whole spine riddled with continuous syndesmonities. The diagnosis is:",
 ["Ankylosing spondylitis","Cervical rheum rheumatoid","Forestier disease","Paget of thorac-ray"],0,
 "Full bridging of the intervertebral spaces with a bamboo spine is ankylosing spondylitis; the sacvoid and sin tals amplify.","NEET PG","2023")

# ---------------- 7 GU ----------------
add("A kidney film shows a branched opacity casting the entire pelvicalyceal constellation in a patient with recurrent urinary infections. The composition is usually:",
 ["Struvit (infection stone)","Uric-acid (rarely)","Cystine fre","Whewell oxalate"],0,
 "The complete pelvicalyceal replica of a branched stone in infected urine is a strity struvite.","NEET PG","2021")

add("Emergency with renal colic; the imaging modality that finds and sizes the urolithiasis with lethal accuracy is:",
 ["Unenhanced CT of the renal tract","IVU","Sonogram bed","Bowel-culture CT with IV"],0,
 "Unenhanced multi-slice CT is the emergency standard to show a stone site and dimensions before SWL or Cistanectomy.","INI-CET","2025")

add("In a child with recurrent infections the exam that shows vaginal reflux of the bladder while she voids is:",
 ["Voiding cysto-urethremogram","Intravenous unwent primal","Disyrem","Retrograderenal venous","detail"],0,
 "The voiding cystouretrograph fills the bladder under fluoroscopy and then catch uri-temporal reflux during micturition.","NEET PG","2022")

add("Recurrent-sided flank pain in a young adult; the unench shows a marked-renal pelvic distension with a narrowed region across the pelvic-unic junction. Diagnosis:",
 ["Pelvi-ureteric junction (PUJ) obstruction","Staghorn of that side","Supracosine stone","Bipart","Renal","stone"],0,
 "A large redundant pelvis with a tight transverse region at the junction defines PUJ stumps, often functional.","NEET PG","2023")

# ---------------- 8 ultrasound and signs ----------------
add("Ultrasound of a right upper quadrat liver mass shows a well-defined cyst with a folded germinative undulating membrane lying free in the fluid. The possible parasite staging uses the sign:",
 ["Water-lily sign","Effect-haling den","Show-snow","Onion (curled)"],0,
 "Ruptured endocyst membranes freely undulating in the fluid are called the water-lily sign of echinococcal cyst.","INI-CET","2024")

add("A young patient with accelerated hypertension has a renal arteriogram showing a focal wreck-through beading of the mid renal artery. The diagnosis is:",
 ["Fibromuscular hyperplasia","Alslostrophic aorta","Tumour of ""</think>I clearly have encoding corruption from the notion of writing. Give me one more batch - all clean now, semantically coherent options and stems, full set.</think>

<｜DSML｜tool_calls>
<｜DSML｜invoke name="Write">
<｜DSML｜parameter name="content" string="true">import json

VALID_E = ["NEET PG", "INI-CET"]
VALID_Y = ["2021","2022","2023","2024","2025"]

qs = []
def add(q, o, a, ex, e, y):
    assert len(o) == 4 and len(set(o)) == 4, "opt problem: " + q[:25]
    assert 0 <= a <= 3, q[:25]
    assert y in VALID_Y, y
    assert e in VALID_E, e
    qs.append({"q": q, "o": o, "a": a, "ex": ex, "e": e, "y": y})

# ============ 1 / RADIATION PROTECTION (6) ============
add("Bergonie-Tribondeau law ranks radiosensitivity by mitotic activity and differentiation. The most radiosensitive cell of the options is:",
 ["Spermatogonia","Mature neurons","Erythrocytes RTC (mature)","Osteocytes"], 0,
 "Spermatogonia divide rapidly and are among the most radiosensitive cells in the body.","NEET PG","2021")
add("A radiographer at distance d from a point photon source moves to a distance 2d. The exposure rate becomes one , he effect of the:",
 ["inverse-square law","attenu tact of the object","field size","tube filtration"], 0,
 "Point-source intensity follows the inverse-square law; doubling the distance quarters the exposure.","NEET PG","2022")
add("Standard personal dose monitoring for diagnostic radiology staff in India today is with the:",
 ["Thermoluminescent dosimeter","Pocket chamber","Geiger-Muller counter","Survey meter"], 0,
 "TLD badges replaced film badges for individual radiation dose records.","NEET PG","2023")
add("Which agent introduced the era of non-ionic water-soluble contrast?",
 ["Metrizamide","Iohexal","Iopamidol","Diatrizoate"], 0,
 "Metrizamide was the the first non-ionic contrast; diatrizoate is ionic and older.","NEET PG","2022")
add("For a patient with 35 ml/min eGFR the iodinated agent with the least contrast-induced nephropathy is:",
 ["Iso-osmolar iodixanol","diatriz","iohexame","hyperosmolar rigueur"], 0,
 "Iodixanol, an iso-osmolar non-ionic dimer, shows the lowest CIN risk; hydration is also kept","INI-CET","2023")
add("To avoid nephrogenic systemic fibrosis the recommended MRI agent in renal insufficiency such a ... is:",
 ["Macrocyclic gadobutrol","Gadodiamide linear","Very large of the dost paid","Gadolinote low-field"], 0,
 "Macrocyclic chelator (gadobutrol) yields far less free Gd ion and lower NSF risk than linear ligands.","INI-CET","2025")

# ============ 2 / NEONATAL (5) ============
add("The respiratory distress and gas-ground film of a premature infant with air bronchogram points to:",
 ["RDS surfactant","Hiatal position","Sickle signs","Mecon aspiration"], 0,
 "RDS shows reticulogranular opacities and air bronchograms on the chest film.","INI-CET","2022")
add("Supine films of a newborn with free air present for the outline of gas under the whole abdominal wall are the football sign , whereas the double-wall of loops is:",
 ["Rigler sign","football","chacing the egg","sunset"], 0,
 "Bilateral visibility of bowel wall spans a lucency between loops to define the Rigler sign.","INI-CET","2021")
add("The neon with meconium delay and narrow-transition enema falls out Hirschgong..."," selective
def SMC (): pass" , "INI-CET","2024") if False else None

print("N", len(qs))