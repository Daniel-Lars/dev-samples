{% macro generate_alias_name(custom_alias_name=none, node=none) -%}

    {%- if custom_alias_name is none -%} {%- set table_name = node.name -%}
    {%- else -%} {%- set table_name = custom_alias_name ~ "_" ~ node.name | trim -%}
    {%- endif -%}

    {%- if target.name == "dev" or target.name == "test" -%}
        {#- Get custom schema name -#}
        {%- set schema_prefix = node.unrendered_config.schema | trim -%}

        {% do log(schema_prefix) %}

        {{ schema_prefix ~ "__" ~ table_name }}

    {%- else -%} {{ table_name }}

    {% endif %}

{%- endmacro %}