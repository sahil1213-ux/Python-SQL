select * from orders_data;
select count(*) from orders_data;


-- 1. Find to 10 highest revenue generated products
select product_id, round(sum(revenue), 2) as revenue
from orders_data
group by product_id
order by revenue desc
limit 10;



-- 2. Find top 5 highest selling products in each region
with cte1 as (
select region, product_id, round(sum(revenue), 2) as sales_price
from orders_data
group by 1, 2
),

cte2 as (
select *, 
       row_number() over(partition by region order by sales_price desc) as rn
from cte1
)

select region, product_id, sales_price
from cte2
where rn < 6;



-- 3. Find month over month growth comparison for 2022 and 2023 sales": eg Jan 2022 vs Jan 2023
with cte1 as (
select date_format(order_date, '%Y-%m-01') as month, 
       year(order_date) as year,
       round(sum(revenue), 2) as current_year_sales
from orders_data
group by 1, 2
order by 1, 2
),

cte2 as (
select *,
       lag(current_year_sales) over(partition by month(month) order by year) as previous_year_sales
from cte1),

cte3 as (
select *,
       case when current_year_sales is not null then 
                 round((current_year_sales - previous_year_sales) / previous_year_sales * 100, 2)
		    else null
	   end as mom_sales_growth_percentage
from cte2)

select *
from cte3
where previous_year_sales is not null;



-- 4. For each category, which month had highest sales?
with cte1 as (
select category, order_date, round(sum(revenue), 2) as sales
from orders_data
group by 1, 2
),

cte2 as (
select *,
       row_number() over(partition by category order by sales desc) as rn
from cte1
)

select category, order_date, sales
from cte2
where rn = 1;



-- 5. Which sub category had the highest growth in 2023 compared to 2022
with cte1 as (
select date_format(order_date, '%Y-%m-01') as month, 
       year(order_date) as year,
       sub_category,
       round(sum(revenue), 2) as current_year_sales
from orders_data
group by 1, 2, 3
order by 1, 2
),

cte2 as (
select *,
       lag(current_year_sales) over(partition by sub_category order by year, month) as previous_year_sales
from cte1),

cte3 as (
select *,
       case when previous_year_sales > 0 then 
                 round((current_year_sales - previous_year_sales) / previous_year_sales * 100, 2)
		    else null
	   end as mom_sales_growth_percentage
from cte2),

cte4 as (
select *,
       row_number() over(partition by sub_category order by mom_sales_growth_percentage desc) as rn
from cte3
where previous_year_sales is not null
)

select sub_category, mom_sales_growth_percentage as best_growth, month as best_growth_month
from cte4
where rn = 1
order by best_growth desc
limit 1;