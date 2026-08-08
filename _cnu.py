import io, json
# consolidate from _rad_final + _rad_new + _phys_qs_tmp
out=[]
for fn in ['questions/_rad_final.json','questions/_rad_new.json','questions/_phys_qs_tmp.json']:
    try:
        d=json.loads(io.open(fn,encoding='utf-8').read())
        out+=d
    except Exception as e:
        print(fn,'ERR',e)
print('consolidated', len(out))
io.open('questions/_extra.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
