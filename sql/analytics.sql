-- Import data/student_performance.csv into SQLite as student_performance.
-- 1. Performance by program
SELECT program, COUNT(*) AS students,
       ROUND(AVG(attendance_pct),1) AS avg_attendance,
       ROUND(AVG(assignment_avg),1) AS avg_assignment,
       ROUND(AVG(midterm_score),1) AS avg_midterm,
       ROUND(AVG(final_score),1) AS avg_final
FROM student_performance GROUP BY program ORDER BY avg_final DESC;

-- 2. Attendance bands and outcomes
SELECT CASE WHEN attendance_pct < 60 THEN '<60%'
            WHEN attendance_pct < 75 THEN '60-74.9%'
            WHEN attendance_pct < 90 THEN '75-89.9%'
            ELSE '90-100%' END AS attendance_band,
       COUNT(*) AS students, ROUND(AVG(final_score),1) AS avg_final
FROM student_performance GROUP BY attendance_band ORDER BY attendance_band;

-- 3. Performance band distribution
SELECT performance_band, COUNT(*) AS students,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM student_performance),1) AS pct
FROM student_performance GROUP BY performance_band;
