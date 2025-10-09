select 
    segment_cd, count, created_dttm
from INTEGRATION.MO_SEGMENTS 
where CREATED_DTTM >= DATEADD(DAY, -2, GETDATE())