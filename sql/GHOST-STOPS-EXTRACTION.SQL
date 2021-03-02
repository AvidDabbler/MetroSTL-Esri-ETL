WITH sgn AS
(
                SELECT signid
                FROM signupperiods
                WHERE 0 = 0
                AND production = 1
                AND TO_NUMBER(TO_CHAR(SYSDATE,'YYYYMMDD')) BETWEEN FromDate AND ToDate
)
SELECT
                (SELECT signid FROM sgn)  || ',' ||
                s.stopid || ',' ||
                '"' || s.stopabbr || '"' || ',' ||
                '"' || s.stopname || '"' || ',' ||
                '"' || s.onstreet || '"' || ',' ||
                '"' || s.atstreet || '"' || ',' ||
                '"' || s.stopposition || '"' || ',' ||
                '"' || CASE WHEN s.preferred = 1 THEN 'YES' WHEN s.preferred = 0 THEN 'NO' END || '"' || ',' ||
                '"' || CASE WHEN s.bench = 1 THEN 'YES' WHEN s.bench = 0 and s.shelter =1 THEN 'YES' WHEN s.bench = 0 and s.shelter = 0 THEN 'NO' END || '"' || ',' ||
                '"' || CASE WHEN s.Shelter = 1 THEN 'YES' WHEN s.shelter = 0 THEN 'NO' END || '"' || ',' ||
                '"' || CASE WHEN s.transfer = 1 THEN 'YES' WHEN s.transfer = 0 THEN 'NO' END || '"' || ',' ||
                '"' || CASE WHEN s.userstring12 = 'A' THEN 'YES' WHEN s.userstring12 != 'A' THEN 'NO' END || '"' || ',' ||
                '"' || CASE WHEN s.userlongstring1 = 'A' THEN 'YES' WHEN s.userlongstring1 != 'A' THEN 'NO' END || '"' || ',' ||
                nvl(CAST(s.countycode AS VARCHAR(30)),'""')  || ',' ||
                '"' || s.city || '"' || ',' ||
                s.gpslon / power(10,(length(abs(s.gpslon)))-2) || ',' ||
                s.gpslat / power(10,(length(abs(s.gpslat)))-2) || ',' || '' AS list
FROM stops s
FULL JOIN -- Routes and Lines by Stop
(
                SELECT
                                stopid,
                                LISTAGG(lineabbr, ', ') WITHIN GROUP (ORDER BY lineabbr ASC) AS routes,
                                LISTAGG(linenum, ', ') WITHIN GROUP (ORDER BY lineabbr ASC) AS lines
                FROM
                (
-- Returns all of the stops used by a route and line, and which other routes share that stop
                                SELECT ls_in.signid, ls_in.stopid, ml_in.lineabbr, ml_in.userstring8 linenum
                                FROM
                                                linestop ls_in,
                                                line l_in,
                                                masterline ml_in
                                WHERE 0 = 0
                                AND ls_in.signid = (SELECT signid FROM sgn)
                                AND l_in.linedirid = ls_in.linedirid
                                AND ml_in.lineid = l_in.lineid
                                AND ml_in.lineabbr NOT IN ('3600', '3601', '3599') -- Add 3599 to filter off MetroLink
                                GROUP BY ls_in.signid, ls_in.stopid, ml_in.lineabbr, ml_in.userstring8
                                ORDER BY stopid ASC
                )
                WHERE 1 = 1
                GROUP BY signid, stopid
) lbs
ON lbs.stopid = s.stopid;
