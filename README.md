# genpark-agentic-commerce-edi-810-to-820-remittance-advice-reconciler-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

B2B EDI 810 invoice to EDI 820 payment order/remittance advice auto-match and line-item short-pay auditor.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `reconcile_edi_810_820_remittance`
- **Category**: `agentic_commerce`

### Method Documentation
Reconcile outbound B2B EDI 810 Invoices against incoming EDI 820 Payment Orders / Remittance Advice.
Performs exact line-item matching, tolerance checks, deduction code extraction (e.g. 01 Pricing Discrepancy, 02 Damaged Goods, 03 Promotional Rebate),
and short-pay claim dispute file generation.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "reconcile_edi_810_820_remittance",
    "arguments": {
    "invoices": [
        {
            "invoice_number": "INV-1001",
            "amount": 15400.0
        },
        {
            "invoice_number": "INV-1002",
            "amount": 8250.5
        },
        {
            "invoice_number": "INV-1003",
            "amount": 21000.0
        }
    ],
    "payments": [
        {
            "invoice_number": "INV-1001",
            "paid_amount": 15400.0,
            "deductions": []
        },
        {
            "invoice_number": "INV-1002",
            "paid_amount": 7950.5,
            "deductions": [
                {
                    "code": "01",
                    "description": "Pricing Discrepancy",
                    "amount": 300.0
                }
            ]
        },
        {
            "invoice_number": "INV-1003",
            "paid_amount": 21000.0,
            "deductions": []
        }
    ],
    "tolerance_cents": 5
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
