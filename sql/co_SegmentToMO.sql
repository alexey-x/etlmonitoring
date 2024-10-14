select [f_id]
      ,[dt]
      ,[dttm]
      ,[project]
      ,[status]
      ,[description]
      ,[load_type]
      ,[cdttm]
from ETL_HDP.LOAD_CALENDAR
where project = 'SEGMENT_MO'
    and dttm > DATEADD(DAY, -1, GETDATE())