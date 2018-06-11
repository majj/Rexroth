
CREATE OR REPLACE FUNCTION public.get_date_v1(i_json json)
  RETURNS json AS
$BODY$

v_sql = "select now()"

try
    rtn = plv8.execute(v_sql)
catch err
    plv8.elog(DEBUG, v_sql)
    msg = "#{err}"
    return {"error":msg, "sql": v_sql}

return {"returning":rtn}

$BODY$
  LANGUAGE plcoffee VOLATILE
  COST 100;
ALTER FUNCTION public.get_date_v1(json)
  OWNER TO mabo;
