select
    scenario_id,
    scenario_nm,
    scenario_desc,
    scenario_period_dd,
    scenario_period_start_dt_bckp,
    scenario_goal,
    status,
    status_desc,
    deleted_flg,
    created_by,
    updated_by,
    last_run_by,
    last_run_dttm,
    last_run_id,
    created_dttm,
    updated_dttm,
    edit_dttm,
    edit_by,
    scenario_period_start_dt,
    delay_days,
    date_setting_method,
    start_period_dttm,
    end_period_dttm,
    is_using_alter_score_ind,
    size_pct,
    algo,
    algo_pct,
    customer_pct,
    alter_score_source
from [MO_DATA].[SCENARIO]
where 1=1
    and DELETED_FLG = 0
    and CREATED_DTTM > DATEADD(DAY, -1, GETDATE())
