import json
p="F:/NEET PG/questions/_rad_new.json"
d=json.load(open(p,encoding="utf-8"))
fix={
 7:{"q":"On a supine abdominal radiograph of a baby, free intra-peritoneal air gathers under the anterior abdominal wall and outlines the whole cavity as an oval gas collection. Which sign is this?"},
 13:{"o":["Diffusion-weighted MRI","T2-weighted fast spin echo","Proton-density scan","T1 pre-contrast sequence"]},
 26:{"q":"A 3-month-old with projectile vomiting after each feed has a pyloric ultrasound showing muscle wall thickness of 4.5 mm and an elongated narrowed canal. Diagnosis:"},
 28:{"q":"A woman notes a gurgling lump in the neck during swallowing and regurgitates food eaten the previous day. The barium swallow shows a pouch of the hypopharynx just above the cricopharyngeus. Diagnosis:"},
 43:{"q":"A young hypoxic patient with pleuritic chest pain has a chest film showing a local lucent oligaemic patch in one zone and a prominent pulmonary trunk. The event most likely responsible is:"},
 45:{"q":"Contrast CT shows an enhancing liver mass that extends as thrombus into the inferior vena cava and portal vein. Which hepatic neoplasm has this characteristic vascular extension?","o":["Hepatocellular carcinoma","Cavernous haemangioma","Focal nodular hyperplasia","Regenerative nodule"]},
}
for i,f in fix.items():
    for k,v in f.items(): d[i][k]=v
json.dump(d,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(d))