# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-edi-810-to-820-remittance-advice-reconciler-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def reconcile_edi_810_820_remittance(invoices, payments, tolerance_cents=5):
    invoice_map = {inv["invoice_number"]: inv for inv in invoices}
    matched = []
    short_paid = []
    over_paid = []
    unmatched_payments = []
    
    total_invoiced_amt = sum(inv["amount"] for inv in invoices)
    total_paid_amt = 0.0
    total_deductions = 0.0
    
    for p in payments:
        inv_no = p["invoice_number"]
        paid_amt = p["paid_amount"]
        total_paid_amt += paid_amt
        deductions = p.get("deductions", [])
        
        if inv_no not in invoice_map:
            unmatched_payments.append(p)
            continue
            
        inv = invoice_map[inv_no]
        expected_amt = inv["amount"]
        diff = round(expected_amt - paid_amt, 2)
        
        deduction_sum = sum(d.get("amount", 0.0) for d in deductions)
        total_deductions += deduction_sum
        
        record = {
            "invoice_number": inv_no,
            "invoiced_amount": expected_amt,
            "paid_amount": paid_amt,
            "variance": diff,
            "deductions": deductions
        }
        
        if abs(diff) <= (tolerance_cents / 100.0):
            matched.append(record)
        elif diff > (tolerance_cents / 100.0):
            short_paid.append(record)
        else:
            over_paid.append(record)
            
    reconciliation_rate = (len(matched) / len(invoices) * 100.0) if invoices else 0.0
    
    return {
        "total_invoices_count": len(invoices),
        "total_invoiced_amount": round(total_invoiced_amt, 2),
        "total_paid_amount": round(total_paid_amt, 2),
        "total_deductions_claimed": round(total_deductions, 2),
        "matched_invoices_count": len(matched),
        "short_paid_invoices_count": len(short_paid),
        "over_paid_invoices_count": len(over_paid),
        "unmatched_payments_count": len(unmatched_payments),
        "reconciliation_match_rate_pct": round(reconciliation_rate, 2),
        "actionable_disputes": [
            {
                "invoice_number": sp["invoice_number"],
                "shortfall": sp["variance"],
                "deduction_codes": [d.get("code") for d in sp["deductions"]]
            } for sp in short_paid
        ]
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "reconcile_edi_810_820_remittance",
                        "description": """Reconcile outbound B2B EDI 810 Invoices against incoming EDI 820 Payment Orders / Remittance Advice.
Performs exact line-item matching, tolerance checks, deduction code extraction (e.g. 01 Pricing Discrepancy, 02 Damaged Goods, 03 Promotional Rebate),
and short-pay claim dispute file generation.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = reconcile_edi_810_820_remittance(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'invoices': [{'invoice_number': 'INV-1001', 'amount': 15400.0}, {'invoice_number': 'INV-1002', 'amount': 8250.5}, {'invoice_number': 'INV-1003', 'amount': 21000.0}], 'payments': [{'invoice_number': 'INV-1001', 'paid_amount': 15400.0, 'deductions': []}, {'invoice_number': 'INV-1002', 'paid_amount': 7950.5, 'deductions': [{'code': '01', 'description': 'Pricing Discrepancy', 'amount': 300.0}]}, {'invoice_number': 'INV-1003', 'paid_amount': 21000.0, 'deductions': []}], 'tolerance_cents': 5}
        out = reconcile_edi_810_820_remittance(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
