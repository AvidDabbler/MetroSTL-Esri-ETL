SELECT
    ls.Sequence || ',' ||
    linesbystop.signid || ',' ||
    s.stopid || ',' ||
    '"' || s.stopabbr ||  '"' || ',' ||
    '"' || s.stopname ||  '"' || ',' ||
	'"' || s.onstreet ||  '"' || ',' ||
    '"' || s.atstreet ||  '"' || ',' ||
    '"' || s.stopposition ||  '"' || ',' ||
    '"' || CASE WHEN S.PREFERRED = 1 THEN 'YES'
        WHEN S.PREFERRED = 0 THEN 'NO'
        END ||  '"' || ',' ||
    '"' || CASE WHEN s.bench = 1 THEN 'YES'
        WHEN s.bench = 0 and s.shelter =1
            THEN 'YES'
        WHEN s.bench = 0 and s.shelter = 0
            THEN 'NO'
        END ||  '"' || ',' ||
    '"' || CASE WHEN s.Shelter = 1 THEN 'YES'
        WHEN s.shelter = 0 THEN 'NO'
        END ||  '"' || ',' ||
    '"' || CASE WHEN s.transfer = 1 THEN 'YES'
        WHEN s.transfer = 0 THEN 'NO'
        END ||  '"' || ',' ||
    '"' || CASE WHEN s.userstring12 = 'A' THEN 'YES'
        WHEN s.userstring12 <> 'A' THEN 'NO'
        END ||  '"' || ',' ||
    '"' || CASE WHEN s.userlongstring1 = 'A' THEN 'YES'
        WHEN s.userlongstring1 <> 'A' THEN 'NO'
        END ||  '"' || ',' ||
    '"' || CASE WHEN ls.nodeid > 0 THEN 'YES'
        WHEN ls.nodeid = 0 THEN 'NO'
        END ||  '"' || ',' ||
    '"' || ML.LINENAME ||  '"' || ',' ||
    '"' || ml.lineabbr ||  '"' || ',' ||
	'"' || l.directionname ||  '"' || ',' ||
    CAST(S.COUNTYCODE AS VARCHAR(30)) || ',' ||
    '"' || S.CITY ||  '"' || ',' ||
    s.gpslon / power(10,(length(abs(s.gpslon)))-2) || ',' ||
    s.gpslat / power(10,(length(abs(s.gpslat)))-2) || ',' ||
    sp.distance || ',' ||'' as LIST
FROM linestop ls
LEFT OUTER JOIN stops s ON s.stopid = ls.stopID
INNER JOIN line l ON l.linedirid = ls.linedirid AND l.signid = ls.signid
INNER JOIN masterline ml ON ml.lineid = l.lineid AND ml.signid = l.signid
INNER JOIN STOPPATTERN sp ON sp.fromstopnum = ls.stopnum and sp.linedirid = ls.linedirid and sp.signid = ls.signid
INNER JOIN
	(SELECT signid, stopid,
		   LTRIM(MAX(SYS_CONNECT_BY_PATH(linenum,','))
		   KEEP (DENSE_RANK LAST ORDER BY curr),',') AS lines
	FROM
		(SELECT DISTINCT signid, stopid, linenum,
			ROW_NUMBER() OVER (PARTITION BY stopid ORDER BY lineabbr) AS curr,
			ROW_NUMBER() OVER (PARTITION BY stopid ORDER BY lineabbr) -1 AS prev
		FROM
			(SELECT DISTINCT ls_in.signid, ls_in.stopid,  ml_in.lineabbr, ml_in.userstring8 linenum
			FROM   linestop ls_in, line l_in, masterline ml_in
			WHERE ls_in.signid in
                (
                    select signid from signupperiods sup
                    where sup.production = 1
                    and to_char(sysdate,'yyyymmdd') BETWEEN sup.FromDate and sup.ToDate
                )
				AND l_in.linedirid = ls_in.linedirid
				AND ml_in.lineid = l_in.lineid
			)
		)
	GROUP BY signid, stopid
	CONNECT BY prev = PRIOR curr AND stopid = PRIOR stopid
	START WITH curr = 1
	) linesbystop
	ON linesbystop.signid = ls.signid AND linesbystop.stopid = ls.stopid
  WHERE ml.lineabbr not in ('3600','3601','3599') 
GROUP BY
    ls.Sequence,
    linesbystop.signid,
    s.stopid,
    s.stopabbr,
    s.stopname,
	s.onstreet,
    s.atstreet,
    s.stopposition,
    CASE WHEN S.PREFERRED = 1 THEN 'YES'
        WHEN S.PREFERRED = 0 THEN 'NO'
        END,
    CASE WHEN s.bench = 1 THEN 'YES'
        WHEN s.bench = 0 and s.shelter =1
            THEN 'YES'
        WHEN s.bench = 0 and s.shelter = 0
            THEN 'NO'
        END,
    CASE WHEN s.Shelter = 1 THEN 'YES'
        WHEN s.shelter = 0 THEN 'NO'
        END,
    CASE WHEN s.transfer = 1 THEN 'YES'
        WHEN s.transfer = 0 THEN 'NO'
        END,
    CASE WHEN ls.nodeid > 0 THEN 'YES'
        WHEN ls.nodeid = 0 THEN 'NO'
        END,
    ML.LINENAME,
    ml.lineabbr,
	l.directionname,
    CAST(S.COUNTYCODE AS VARCHAR(30)),
    S.CITY,
    s.gpslon,
    s.gpslat,
    sp.distance,
    CASE WHEN s.userstring12 = 'A' THEN 'YES'
        WHEN s.userstring12 <> 'A' THEN 'NO'
        END,
    CASE WHEN s.userlongstring1 = 'A' THEN 'YES'
        WHEN s.userlongstring1 <> 'A' THEN 'NO'
        END
ORDER BY ml.lineabbr, l.directionname, ls.sequence;



