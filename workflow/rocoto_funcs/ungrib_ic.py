#!/usr/bin/env python
import os
from rocoto_funcs.base import xml_task, source, get_cascade_env

### begin of ungrib_ic --------------------------------------------------------
def ungrib_ic(xmlFile, expdir, do_ensemble=False):
  # Task-specific EnVars beyond the task_common_vars
  dcTaskEnv={
    'FHR': '000',
    'TYPE': 'ic'
  }
  #
  if not do_ensemble:
    metatask=False
    meta_id=''
    task_id='ungrib_ic'
    cycledefs='ic'
    prefix=os.getenv('IC_PREFIX','IC_PREFIX_not_defined')
    offset=os.getenv('IC_OFFSET','3')
    meta_bgn=""
    meta_end=""
  else:
    metatask=True
    meta_id='ungrib_ic'
    task_id=f'{meta_id}_m#ens_index#'
    cycledefs='ens_ic'
    dcTaskEnv['ENS_INDEX']="#ens_index#"
    prefix=os.getenv('ENS_IC_PREFIX','GEFS')
    offset=os.getenv('ENS_IC_OFFSET','36')
    ens_size=int(os.getenv('ENS_SIZE','2'))
    ens_indices=''.join(f'{i:03d} ' for i in range(1,int(ens_size)+1)).strip()
    gmems=''.join(f'{i:02d} ' for i in range(1,int(ens_size)+1)).strip()
    meta_bgn=f'''
<metatask name="ens_{meta_id}">
<var name="ens_index">{ens_indices}</var>
<var name="gmem">{gmems}</var>'''
    meta_end=f'</metatask>\n'
  #
  # dependencies
  COMINgfs=os.getenv("COMINgfs",'COMINgfs_not_defined')
  COMINrrfs=os.getenv("COMINrrfs",'COMINrrfs_not_defined')
  COMINrap=os.getenv("COMINrap",'COMINrap_not_defined')
  COMINhrrr=os.getenv("COMINhrrr",'COMINhrrr_not_defined')
  COMINgefs=os.getenv("COMINgefs",'COMINgefs_not_defined')
  if prefix == "GFS":
    fpath=f'{COMINgfs}/gfs.@Y@m@d/@H/gfs.t@Hz.pgrb2.0p25.f{offset:>03}'
  elif prefix == "RRFS":
    fpath=f'{COMINrrfs}/rrfs.@Y@m@d/@H/rrfs.t@Hz.natlve.f{offset:>02}.grib2'
  elif prefix == "RAP":
    fpath=f'{COMINrap}/rap.@Y@m@d/rap.t@Hz.wrfnatf{offset:>02}.grib2'
  elif prefix == "GEFS":
    fpath=f'{COMINgefs}/gefs.@Y@m@d/@H/pgrb2ap5/gep#gmem#.t@Hz.pgrb2a.0p50.f{offset:>03}'
    fpath2=f'{COMINgefs}/gefs.@Y@m@d/@H/pgrb2bp5/gep#gmem#.t@Hz.pgrb2b.0p50.f{offset:>03}'
  else:
    fpath=f'/not_supported_LBC_PREFIX={prefix}'

  timedep=""
  realtime=os.getenv("REALTIME","false")
  starttime=get_cascade_env(f"STARTTIME_{task_id}".upper())
  if realtime.upper() == "TRUE":
    timedep=f'\n  <timedep><cyclestr offset="{starttime}">@Y@m@d@H@M00</cyclestr></timedep>'
  #
  datadep=f'<datadep age="00:05:00"><cyclestr offset="-{offset}:00:00">{fpath}</cyclestr></datadep>'
  if do_ensemble:
    datadep=datadep+f'\n  <datadep age="00:05:00"><cyclestr offset="-{offset}:00:00">{fpath2}</cyclestr></datadep>'
  dependencies=f'''
  <dependency>
  <and>{timedep}
  {datadep}
  </and>
  </dependency>'''
  #
  xml_task(xmlFile,expdir,task_id,cycledefs,dcTaskEnv,dependencies,metatask,meta_id,meta_bgn,meta_end,"UNGRIB",do_ensemble)
### end of ungrib_ic --------------------------------------------------------
