# Finacel Report for {{ data.company_name }} ({{ data.symbol }})
## Company Information
**Name:** {{ data.company_name }}
**Ticker:** {{ data.symbol }}
**Sector:** {{ data.sector }}
**Industry:** {{ data.industry }}
**Address**
    {{ data.address.street_1 }}
    {{ data.address.street_2 if data.address.street_2 != None }}
    {{ data.address.city }}, {{ data.address.state }} {{ data.address.postal_code }} {{ data.address.country }}
**Website:** {{ data.website }}
---

## Balance Sheet

{{ data.generate_markdown_table(data.balance_sheet) }}

## Company Financials

{{ data.generate_markdown_table(data.financials) }}

## Cash Flow

{{ data.generate_markdown_table(data.cash_flow) }}

## Earning Statement

{{ data.generate_markdown_table(data.earnings) }}

---

## News

{% for n in data.news %}
### {{ n['content']['title'] }}
**Source:** {{ n['content']['clickThroughUrl']['url'] }} 

**Summary:**
{{ n['content']['summary'] }}

---
{% endfor %}