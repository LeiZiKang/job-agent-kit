import json,sys,datetime as dt,glob,collections
def ts(s): return dt.datetime.fromisoformat(s.replace('Z','+00:00'))
for f in sys.argv[1:]:
    ev=[json.loads(l) for l in open(f) if l.strip()]
    start=ts(ev[0]['timestamp']); end=ts(ev[-1]['timestamp'])
    calls={}; tool=0.0; think=0.0; last_out=start; names=collections.Counter(); ntok=None; slow=[]
    for e in ev:
        p=e.get('payload') or {}; t=ts(e['timestamp'])
        if p.get('type')=='custom_tool_call' or p.get('type')=='function_call':
            think+=(t-last_out).total_seconds(); calls[p.get('call_id')]=(t,p.get('name')); names[p.get('name')]+=1
            inp=(p.get('input') or p.get('arguments') or '')
        if p.get('type') in('custom_tool_call_output','function_call_output'):
            c=calls.get(p.get('call_id'))
            if c: d=(t-c[0]).total_seconds(); tool+=d; slow.append((d,c[1])); last_out=t
        if p.get('type')=='token_count':
            ntok=(p.get('info') or {}).get('total_token_usage')
    tot=(end-start).total_seconds()
    print(f"\n{f.split('-',6)[-1][:44]}  total {tot/60:.1f}min  calls {sum(names.values())} {dict(names)}")
    print(f"  model thinking {think/60:.1f}min ({think/tot*100:.0f}%)   tool exec {tool/60:.1f}min ({tool/tot*100:.0f}%)")
    slow.sort(reverse=True); print("  slowest tool calls(s):",[round(x[0]) for x in slow[:6]])
    if ntok: print("  tokens:",{k:ntok[k] for k in ntok if 'token' in k})
