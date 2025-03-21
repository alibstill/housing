WITH aggregated_yearly_property_price_data AS (
    SELECT 
        dd.year, 
        ll.county, 
        pt.property_type_name, 
        t.tenure_name, 
        ps.is_new_build, 
        COUNT(*) num_transactions, 
        ROUND(AVG(ps.price), 2) avg_price, 
        MIN(ps.price) min_price, 
        MAX(ps.price) max_price,
        APPROX_QUANTILES(ps.price, 100)[SAFE_OFFSET(50)] median_price
    FROM `dezc-housing.housing.fact_property_sales` ps
    INNER JOIN `dezc-housing.housing.dim_locations` ll ON ps.location_id = ll.location_id
    INNER JOIN `dezc-housing.housing.dim_dates` dd on ps.date_of_transfer = dd.day_date
    INNER JOIN `dezc-housing.housing.dim_property_types` pt on ps.property_type_id = pt.property_type_id
    INNER JOIN `dezc-housing.housing.dim_tenures` t on ps.tenure_id = t.tenure_id
    GROUP BY CUBE(dd.year, ll.county, pt.property_type_name, t.tenure_name, ps.is_new_build)
)

SELECT * FROM aggregated_yearly_property_price_data

