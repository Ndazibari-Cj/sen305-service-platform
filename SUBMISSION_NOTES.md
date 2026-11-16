# SEN305 In-Lab Exercise — Submission Notes

- **Group NO:** Group 10
- **Group Leader:** Ekugo C. Daniel
- **Data Note:** Only synthetic lab data was created and used for testing and query analysis.

---

## Task 3: Query & Index Execution Plan Evidence

### 1. Raw SQL (`qs.query`)
```sql
SELECT `requests_app_servicerequest`.`id`, `requests_app_servicerequest`.`requester_id`, `requests_app_servicerequest`.`category_id`, `requests_app_servicerequest`.`title`, `requests_app_servicerequest`.`description`, `requests_app_servicerequest`.`location`, `requests_app_servicerequest`.`priority`, `requests_app_servicerequest`.`status`, `requests_app_servicerequest`.`due_at`, `requests_app_servicerequest`.`resolution_summary`, `requests_app_servicerequest`.`resolved_at`, `requests_app_servicerequest`.`created_at`, `requests_app_servicerequest`.`updated_at`
FROM `requests_app_servicerequest`
WHERE (`requests_app_servicerequest`.`category_id` = 4 AND `requests_app_servicerequest`.`status` IN ('open', 'assigned'))
ORDER BY `requests_app_servicerequest`.`priority` ASC, `requests_app_servicerequest`.`created_at` DESC;
```

### 2. MySQL Execution Plan (`qs.explain()`)
```text
-> Sort row IDs: requests_app_servicerequest.priority, requests_app_servicerequest.created_at DESC  (cost=2.31 rows=4)
    -> Index range scan on requests_app_servicerequest using req_app_cat_status_idx over (category_id = 4 AND status = 'assigned') OR (category_id = 4 AND status = 'open'), with index condition: ((requests_app_servicerequest.category_id = 4) and (requests_app_servicerequest.`status` in ('open','assigned')))  (cost=2.31 rows=4)
```

### 3. Index Usage Explanation
MySQL used the composite index **`req_app_cat_status_idx`** on `(category_id, status)` to perform an **index range scan** (`cost=2.31`, scanning only the 4 matching rows instead of all 24 rows in the table). Because the `ORDER BY` clause sorts by `(priority ASC, created_at DESC)`, which are not trailing columns of `req_app_cat_status_idx`, MySQL applies an in-memory sort (`Sort row IDs`) only to that narrow filtered subset of 4 rows.
