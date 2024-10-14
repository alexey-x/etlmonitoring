-- SERVER = S-RTO-P3MS-LS
-- DB = MODB
-- Table substitutes when statistics calculated
SELECT
    count(*) as total_rows,
	count(distinct GOLD_CUSTOMER_ID) as unique_customers,
	count(distinct model_id) as model_id_cnt,
	min(SCORE_MODEL_PROB) as min_score_response,
	avg(SCORE_MODEL_PROB) as avg_score_response,
	max(SCORE_MODEL_PROB) as max_score_response
FROM $ALTER_SCORES$ t
