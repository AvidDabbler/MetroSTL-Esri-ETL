SELECT
    ml.signid || ',' ||
    xp.shape_id || ',' ||
    '"' || ml.lineabbr  || '"'  || ',' ||
    '"' || substr(mp.pattern, 0, 2) || '"'  || ',' ||
    '"' || ml.linename  || '"'  || ',' ||
    '"' || ML.USERLONG2  || '"'  || ',' ||
    '"' || to_number(ml.lineabbr)  || '"'  || ',' ||
    tm.fromlat / power(10,(length(abs(tm.fromlat)))-2) || ',' ||
    tm.fromlon / power(10,(length(abs(tm.fromlon)))-2) || ',' ||
    xp.shape_pt_sequence || ',' || ''
FROM trapeze.tracemap tm
INNER JOIN
    (
        SELECT
            pt.patternid AS shape_id,
            pt.sequence AS shape_pt_sequence,
            pt.traceid as traceid
        FROM trapeze.patterntrace pt
        WHERE pt.patternid IN
        (
            SELECT 
                DISTINCT mp.patternid AS patternid
            FROM  
                trapeze.masterline m
                INNER JOIN line l
                ON l.signid = m.signid 
                AND l.lineid = m.lineid
                INNER JOIN trapeze.trips t
                ON t.signid = l.signid 
                AND t.linedirid = l.linedirid
                INNER JOIN trapeze.linestop ls
                ON ls.linedirid = l.linedirid
                AND ls.signid = l.signid 
                AND ls.stopid NOT IN (14178, 14903, 13671, 14115)
                INNER JOIN trapeze.masterpattern mp
                ON mp.patternid = t.patternid
                AND mp.signid = t.signid 
                INNER JOIN trapeze.stoptimes st
                ON t.tripid = st.tripid 
                AND ls.stopnum = st.stopnum
            WHERE 
                m.signid in
                (
                    select signid from signupperiods sup
                    where sup.production = 1
                    and to_char(sysdate,'yyyymmdd') BETWEEN sup.FromDate and sup.ToDate
                )
                AND m.userstring8 IS NOT NULL
        )
        ORDER BY pt.patternid, pt.sequence
    ) xp
    ON tm.traceid = xp.traceid
inner join TRAPEZE.masterpattern mp on mp.patternid = xp.shape_id
inner join trapeze.masterline ml on ml.lineid = floor(mp.linedirid/10)
ORDER BY shape_id ASC, shape_pt_sequence ASC;

