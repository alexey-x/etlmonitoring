SELECT
      count(*) as total_rows,
      count(distinct GOLD_CUSTOMER_ID) as unique_customers,
      SEGMENT_CD as segment,
      min(REPORT_DATE) as min_report_date,
      max(REPORT_DATE) as max_report_date,
      min(SCORE_RESPONSE_AMT) as min_score_response,
      avg(SCORE_RESPONSE_AMT) as avg_score_response,
      max(SCORE_RESPONSE_AMT) as max_score_response,
      min(T_CHANGED) as min_t_deleted_flg,
      max(T_CHANGED) as max_t_deleted_flg,
      min(T_SYS_DATETIME) as min_t_changed_dttm,
      max(T_SYS_DATETIME) as max_t_changed_dttm
FROM INTEGRATION.T_F_MO_LTV
GROUP BY SEGMENT_CD