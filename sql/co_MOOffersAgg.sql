select 
    segment_cd,
	status,
	count(*) num_offers,
	max(created_dttm) created_dttm,
	max(updated_dttm) updated_dttm
from INTEGRATION.MO_OFFERS
where 1=1 
    and (CREATED_DTTM >= DATEADD(DAY, -2, GETDATE()) or UPDATED_DTTM >= DATEADD(DAY, -2, GETDATE()))
group by SEGMENT_CD,
		 STATUS