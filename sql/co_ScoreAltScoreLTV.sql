select [f_id]
      ,[dt]
      ,[dttm]
      ,[project]
      ,[status]
      ,[description]
      ,[load_type]
      ,[cdttm]
from ETL_HDP.LOAD_CALENDAR
where project in ('MO_MONTHLY_ALTER',  'MO_LTV', 'MO_MONTHLY')
    and dttm > DATEADD(DAY, -1, GETDATE())