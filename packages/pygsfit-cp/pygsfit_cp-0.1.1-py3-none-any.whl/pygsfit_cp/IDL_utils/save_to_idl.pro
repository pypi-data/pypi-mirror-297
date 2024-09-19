;READ_HDF5_PATH = '/Users/walterwei/Dropbox/pygsfit_cp/IDL_utils/'
;!PATH = !PATH + ':' + READ_HDF5_PATH
;RESOLVE_ROUTINE, 'read_hdf5',/is_function
;.compile -f '/Users/walterwei/Dropbox/pygsfit_cp/IDL_utils/read_hdf5.pro'
cmaps=read_hdf5("/Users/walterwei/Downloads/20220511/gsfit_test/viewer_test/output_2.h5", /shallow)
cmaps2 = read_hdf5("/Users/walterwei/Downloads/20220511/gsfit_test/viewer_test/output_3.h5", /shallow)
;template_struct = cmaps.maps.datamaps.(0)
;n_maps = N_ELEMENTS(TAG_NAMES(cmaps.maps.datamaps))
;datamaps_array = REPLICATE(template_struct, n_maps)
;errmaps_array = REPLICATE(template_struct, n_maps)
;fitmaps_array = REPLICATE(template_struct, n_maps)
;FOR i = 0, n_maps - 1 DO BEGIN
;  datamaps_array[i] = cmaps.maps.datamaps.(i)
;  errmaps_array[i] = cmaps.maps.errmaps.(i)
;  fitmaps_array[i] = cmaps.maps.fitmaps.(i)
;ENDFOR
;datamaps_array_2 = REPLICATE(template_struct, n_maps)
;errmaps_array_2 = REPLICATE(template_struct, n_maps)
;fitmaps_array_2 = REPLICATE(template_struct, n_maps)
;FOR i = 0, n_maps - 1 DO BEGIN
;  datamaps_array_2[i] = cmaps2.maps.datamaps.(i)
;  errmaps_array_2[i] = cmaps2.maps.errmaps.(i)
;  fitmaps_array_2[i] = cmaps2.maps.fitmaps.(i)
;ENDFOR
sample_data = cmaps.maps.datamaps.(0)
new_datamaps_array =make_array(50,2,value=sample_data)
new_errmaps_array = make_array(50,2,value=sample_data)
new_fitmaps_array = make_array(50,2,value=sample_data)
FOR i = 0, 49 DO BEGIN
  new_datamaps_array[i, 0] = cmaps.maps.datamaps.(i)
  new_datamaps_array[i, 1] = cmaps2.maps.datamaps.(i)
  new_errmaps_array[i, 0] = cmaps.maps.errmaps.(i)
  new_errmaps_array[i, 1] = cmaps2.maps.errmaps.(i)
  new_fitmaps_array[i, 0] = cmaps.maps.fitmaps.(i)
  new_fitmaps_array[i, 1] = cmaps2.maps.fitmaps.(i)
ENDFOR
;new_datamaps_array = REPLICATE(datamaps_array, 2)
;new_datamaps_array[1] = datamaps_array_2
;new_errmaps_array = REPLICATE(errmaps_array, 2)
;new_errmaps_array[1] = errmaps_array_2
;new_fitmaps_array = REPLICATE(fitmaps_array, 2)
;new_fitmaps_array[1] = fitmaps_array_2


  new_maps = CREATE_STRUCT($
    'B', [cmaps.maps.B, cmaps2.maps.B], $
    'CHISQR', [cmaps.maps.CHISQR, cmaps2.maps.CHISQR], $
    'DATAMAPS', new_datamaps_array, $
    'DELTA', [cmaps.maps.DELTA, cmaps2.maps.DELTA], $
    'ERRB', [cmaps.maps.ERRB, cmaps2.maps.ERRB], $
    'ERRDELTA', [cmaps.maps.ERRDELTA, cmaps2.maps.ERRDELTA], $
    'ERRE_MAX', [cmaps.maps.ERRE_MAX, cmaps2.maps.ERRE_MAX], $
    'ERRMAPS', new_errmaps_array, $
    'ERRN_NTH', [cmaps.maps.ERRN_NTH, cmaps2.maps.ERRN_NTH], $
    'ERRN_TH', [cmaps.maps.ERRN_TH, cmaps2.maps.ERRN_TH], $
    'ERRPEAKFLUX', [cmaps.maps.ERRPEAKFLUX, cmaps2.maps.ERRPEAKFLUX], $
    'ERRPEAKFREQ', [cmaps.maps.ERRPEAKFREQ, cmaps2.maps.ERRPEAKFREQ], $
    'ERRTHETA', [cmaps.maps.ERRTHETA, cmaps2.maps.ERRTHETA], $
    'ERRT_E', [cmaps.maps.ERRT_E, cmaps2.maps.ERRT_E], $
    'ERRWB', [cmaps.maps.ERRWB, cmaps2.maps.ERRWB], $
    'ERRWNTH', [cmaps.maps.ERRWNTH, cmaps2.maps.ERRWNTH], $
    'E_MAX', [cmaps.maps.E_MAX, cmaps2.maps.E_MAX], $
    'FITMAPS', new_fitmaps_array, $
    'N_NTH', [cmaps.maps.N_NTH, cmaps2.maps.N_NTH], $
    'N_TH', [cmaps.maps.N_TH, cmaps2.maps.N_TH], $
    'PEAKFLUX', [cmaps.maps.PEAKFLUX, cmaps2.maps.PEAKFLUX], $
    'PEAKFREQ', [cmaps.maps.PEAKFREQ, cmaps2.maps.PEAKFREQ], $
    'RESIDUAL', [cmaps.maps.RESIDUAL, cmaps2.maps.RESIDUAL], $
    'THETA', [cmaps.maps.THETA, cmaps2.maps.THETA], $
    'T_E', [cmaps.maps.T_E, cmaps2.maps.T_E], $
    'WB', [cmaps.maps.WB, cmaps2.maps.WB], $
    'WNTH', [cmaps.maps.WNTH, cmaps2.maps.WNTH]$
    )
save,  filename='/Users/walterwei/Desktop/test_3.sav', new_maps
end