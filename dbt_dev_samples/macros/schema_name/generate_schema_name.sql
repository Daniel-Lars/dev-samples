{% macro generate_schema_name(custom_schema_name, node) -%}

    {% set dev_prefix = "dev_" %}
    {% set user_name = env_var('DEV_NAME', 'dev') | lower %}

    {% if target.name == "dev" %}
        {{ dev_prefix ~ user_name | trim }} 
    {% elif custom_schema_name is not none %}
        {{ custom_schema_name | trim }} 
    {% else %}
        {{ target.schema }} 
    {% endif %}  

{%- endmacro %}