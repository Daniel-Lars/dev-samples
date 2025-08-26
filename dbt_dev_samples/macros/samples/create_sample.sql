{% macro create_small_sample(source_name) %}

    {% do log("Yooooo running the full sample") %}
    {% set sql %}
    create table if exists webshop."{{ target.dbname }}".{{source_name}} as
    select *
    from foreign_raw.{{source_name}}
    limit 1
    {% endset %}
    {% do run_query(sql) %}

    {% do log("Executing SQL: " ~ sql, info=True) %}
    {% do log("Created full sample") %}

{% endmacro %}