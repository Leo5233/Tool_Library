--土法煉鋼排名
SELECT E1.EMPLOYEE_ID, E1.FIRST_NAME, E1.SALARY S1, COUNT(E2.SALARY) S2
FROM EMPLOYEES E1, EMPLOYEES E2
WHERE E1.SALARY <= E2.SALARY
GROUP BY E1.EMPLOYEE_ID, E1.FIRST_NAME, E1.SALARY
ORDER BY S2;

--排名中位數
WITH RA AS (
  SELECT E1.EMPLOYEE_ID E_ID, E1.FIRST_NAME, E1.SALARY, ROW_NUMBER() OVER( ORDER BY E1.SALARY DESC) RANK_SALARY
  FROM EMPLOYEES E1 LEFT JOIN DEPARTMENTS D
  ON E1.DEPARTMENT_ID = D.DEPARTMENT_ID
)
SELECT RANK_SALARY FROM RA
WHERE RANK_SALARY = (SELECT CEIL(COUNT(E_ID)/2) FROM RA);


--累計總和
SELECT E1.EMPLOYEE_ID , E1.FIRST_NAME, E1.SALARY, SUM(E2.SALARY) SUM_SALARY
FROM EMPLOYEES E1, EMPLOYEES E2
--不能同薪水的一次全部加入　所以用ＩＤ區分　ＩＤ＜＝自身才加入
WHERE E1.SALARY < E2.SALARY OR　E1.SALARY = E2.SALARY AND E1.EMPLOYEE_ID <= E2.EMPLOYEE_ID
GROUP BY E1.EMPLOYEE_ID , E1.FIRST_NAME, E1.SALARY
ORDER BY SUM_SALARY;

--一定要ＳＥＬＥＣＴ不能直接／ＳＵＭ（）
SELECT E1.EMPLOYEE_ID , E1.FIRST_NAME, E1.SALARY, ROUND(SUM(E2.SALARY)/(SELECT SUM(SALARY) FROM EMPLOYEES)*100, 2) SUM_SALARY
FROM EMPLOYEES E1, EMPLOYEES E2
WHERE E1.SALARY < E2.SALARY OR　E1.SALARY = E2.SALARY AND E1.EMPLOYEE_ID <= E2.EMPLOYEE_ID
GROUP BY E1.EMPLOYEE_ID , E1.FIRST_NAME, E1.SALARY
ORDER BY SUM_SALARY;


