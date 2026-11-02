-- ============================================================================
-- Project: Study on Awareness and Understanding of Budget Terms Among Students
-- Author: Dhruv Chhaganlal Shah (Lead Data Analyst, 4-Member Field Study Team)
-- Institution: Bharat College of Arts & Commerce (University of Mumbai)
-- Dataset: student_budget_literacy_survey_40.csv (N = 40 Undergraduate Students)
-- ============================================================================

CREATE TABLE student_budget_survey (
    respondent_id VARCHAR(10) PRIMARY KEY,
    stream VARCHAR(30) NOT NULL,
    academic_year VARCHAR(15) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    term_awareness VARCHAR(5) NOT NULL,          -- 'Yes' or 'No'
    understanding_level VARCHAR(25) NOT NULL,    -- 'Correct', 'Partial/Confused', 'No Knowledge'
    primary_info_source VARCHAR(35) NOT NULL,
    budget_relevance_interest VARCHAR(10) NOT NULL,
    quiz_score_out_of_10 INT NOT NULL,
    interviewer_observation TEXT
);

-- 1. Overall Comprehension Breakdown (Reproduces Field Visit Report Appendix A)
SELECT
    understanding_level AS category,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS percentage
FROM student_budget_survey
GROUP BY understanding_level
ORDER BY
    CASE understanding_level
        WHEN 'Correct' THEN 1
        WHEN 'Partial/Confused' THEN 2
        WHEN 'No Knowledge' THEN 3
    END;

-- 2. Stream-Wise Awareness vs. Actual Understanding (Reproduces Report Appendix B)
-- Highlights the 2x Awareness Gap (90% Commerce vs. 45% CS) and
-- 9x Deep Comprehension Gap (45% Commerce vs. 5% CS)
SELECT
    stream,
    COUNT(*) AS total_students,
    SUM(CASE WHEN term_awareness = 'Yes' THEN 1 ELSE 0 END) AS aware_count,
    ROUND(SUM(CASE WHEN term_awareness = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS awareness_pct,
    SUM(CASE WHEN understanding_level = 'Correct' THEN 1 ELSE 0 END) AS correct_understanding_count,
    ROUND(SUM(CASE WHEN understanding_level = 'Correct' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS understanding_pct,
    ROUND(AVG(quiz_score_out_of_10), 2) AS avg_quiz_score
FROM student_budget_survey
GROUP BY stream
ORDER BY awareness_pct DESC;

-- 3. Primary Information Source Impact on Budget Comprehension
-- Demonstrates why structured textbook learning outperforms informal social media
SELECT
    stream,
    primary_info_source,
    COUNT(*) AS respondents,
    SUM(CASE WHEN understanding_level = 'Correct' THEN 1 ELSE 0 END) AS correct_count,
    ROUND(AVG(quiz_score_out_of_10), 2) AS avg_comprehension_score
FROM student_budget_survey
GROUP BY stream, primary_info_source
ORDER BY stream, respondents DESC;

-- 4. Identify "High Awareness but Jargon-Confused" Target Cohort for Workshops
SELECT
    respondent_id,
    stream,
    academic_year,
    primary_info_source,
    quiz_score_out_of_10,
    interviewer_observation
FROM student_budget_survey
WHERE term_awareness = 'Yes'
  AND understanding_level = 'Partial/Confused'
ORDER BY stream, quiz_score_out_of_10 DESC;
