SELECT
	lc.F_ID,
	lc.DTTM,
	lc.LOAD_SCHEME,
	ll.ROWS_AFFECTED
FROM ETL_HDP.LOADER_LOG ll
inner join 
(SELECT top 1 * from ETL_HDP.LOAD_CALENDAR t where t.project = 'CMDM_BRT' order by t.F_ID desc) lc
       on ( ll.project = lc.project and ll.f_id = lc.f_id)
WHERE 1=1
       and ll.TABLE_NAME = 'T_F_OFFER_ROTATION'