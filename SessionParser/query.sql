-- Группировка по country, region, city
select country, region, city from sessions
group by country, region, city
order by country, region, city
;

-- Группировка по user_country, user_city
select user_country, user_city from sessions
group by user_country, user_city
order by user_country, user_city
;
