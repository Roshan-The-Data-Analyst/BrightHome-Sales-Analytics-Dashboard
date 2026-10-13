#!/usr/bin/env python3
"""Audit BrightHome's XLSX source and regenerate the data-quality audit using stdlib only."""
from __future__ import annotations
import argparse, csv, json, math, posixpath, zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

D=Decimal; CENT=D("0.01"); ZERO=D("0")
MAIN="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
DOC_REL="{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL="{http://schemas.openxmlformats.org/package/2006/relationships}"
EXPECTED=["OrderID","OrderDate","Region","City","Category","Product","Quantity","UnitPrice","Discount","Sales","Profit","CustomerSegment","ShipMode","CustomerID","ShippingCost"]

def money(x): return x.quantize(CENT,rounding=ROUND_HALF_UP)
def fmt(x): return f"{D(str(x)).quantize(CENT,rounding=ROUND_HALF_UP):.2f}"
def pct(x): return fmt(D(str(x))*D("100"))
def dec(row,key): return D(row[key].strip())
def colnum(ref):
    n=0
    for c in ref:
        if not c.isalpha(): break
        n=n*26+ord(c.upper())-ord("A")+1
    return n-1

def read_xlsx(path):
    with zipfile.ZipFile(path) as z:
        wb=ET.fromstring(z.read("xl/workbook.xml"))
        rel=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets={x.attrib["Id"]:x.attrib["Target"] for x in rel.findall(PKG_REL+"Relationship")}
        strings=[]
        if "xl/sharedStrings.xml" in z.namelist():
            sx=ET.fromstring(z.read("xl/sharedStrings.xml"))
            strings=["".join(t.text or "" for t in si.iter(MAIN+"t")) for si in sx.findall(MAIN+"si")]
        target=None
        for s in wb.find(MAIN+"sheets").findall(MAIN+"sheet"):
            if s.attrib.get("name")=="brighthome_dataset":
                target=targets.get(s.attrib.get(DOC_REL+"id","")); break
        if not target: raise ValueError("Worksheet brighthome_dataset not found")
        target=target.lstrip("/")
        sheetpath=target if target.startswith("xl/") else posixpath.normpath(posixpath.join("xl",target))
        root=ET.fromstring(z.read(sheetpath))
        matrix=[]
        for row in root.iter(MAIN+"row"):
            cells=[]
            for c in row.findall(MAIN+"c"):
                idx=colnum(c.attrib.get("r",""))
                while len(cells)<=idx: cells.append("")
                t=c.attrib.get("t");v=c.find(MAIN+"v")
                if t=="inlineStr": value="".join(x.text or "" for x in c.iter(MAIN+"t"))
                elif v is None or v.text is None: value=""
                elif t=="s": value=strings[int(v.text)]
                else: value=v.text
                cells[idx]=value
            matrix.append(cells)
    if not matrix: raise ValueError("Empty source sheet")
    headers=[str(x).strip() for x in matrix[0]]
    if headers!=EXPECTED: raise ValueError(f"Unexpected columns: {headers}")
    rows=[]
    for raw in matrix[1:]:
        values=raw+[""]*(len(headers)-len(raw))
        obj={headers[i]:str(values[i]).strip() for i in range(len(headers))}
        if any(obj.values()): rows.append(obj)
    return headers,rows

def parse_date(row):
    raw=row["OrderDate"].strip()
    try: return date.fromisoformat(raw)
    except ValueError: return date(1899,12,30)+timedelta(days=int(D(raw)))

def total(rows,key): return sum((dec(r,key) for r in rows),ZERO)
def distinct(rows,key): return len({r[key] for r in rows})

def main():
    root=Path(__file__).resolve().parents[1]
    p=argparse.ArgumentParser(description="Audit BrightHome source data.")
    p.add_argument("--input",type=Path,default=root/"data"/"source"/"BrightHome_Dataset.xlsx")
    p.add_argument("--output-dir",type=Path,default=root/"reports")
    args=p.parse_args()
    headers,rows=read_xlsx(args.input)
    dates=[parse_date(r) for r in rows]
    sales,profit,shipping=total(rows,"Sales"),total(rows,"Profit"),total(rows,"ShippingCost")
    discounts=[dec(r,"Discount") for r in rows]
    discount_est=sum((dec(r,"Sales")*dec(r,"Discount") for r in rows),ZERO)
    sales_proxy=sales-discount_est
    orders,customers=distinct(rows,"OrderID"),distinct(rows,"CustomerID")
    discounted=sum(d>ZERO for d in discounts)
    missing={k:sum(not (r.get(k) or "").strip() for r in rows) for k in headers}
    signatures=Counter(tuple(r[k] for k in headers) for r in rows)
    duplicate_rows=sum(n-1 for n in signatures.values() if n>1)
    id_counts=Counter(r["OrderID"] for r in rows)
    duplicate_ids=sum(n-1 for n in id_counts.values() if n>1)
    formula_errors=sum(money(dec(r,"Quantity")*dec(r,"UnitPrice"))!=money(dec(r,"Sales")) for r in rows)
    xs=[float(d) for d in discounts]; ys=[float(dec(r,"Profit")) for r in rows]
    mx,my=sum(xs)/len(xs),sum(ys)/len(ys)
    num=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    dx=math.sqrt(sum((x-mx)**2 for x in xs));dy=math.sqrt(sum((y-my)**2 for y in ys))
    corr=num/(dx*dy) if dx and dy else 0.0
    dist={fmt(k):v for k,v in sorted(Counter(discounts).items())}
    report={
      "source_workbook":str(args.input),"worksheet":"brighthome_dataset","records":len(rows),"column_count":len(headers),"columns":headers,
      "date_range":{"min":min(dates).isoformat(),"max":max(dates).isoformat()},
      "dimensions":{"orders":orders,"customers":customers,"regions":distinct(rows,"Region"),"cities":distinct(rows,"City"),
        "categories":distinct(rows,"Category"),"products":distinct(rows,"Product"),"shipping_modes":distinct(rows,"ShipMode"),
        "customer_segments":distinct(rows,"CustomerSegment")},
      "data_quality":{"missing_values_by_column":missing,"total_missing_cells":sum(missing.values()),"exact_duplicate_rows":duplicate_rows,
        "distinct_order_ids":len(id_counts),"duplicate_order_id_occurrences":duplicate_ids,"invalid_dates":0,
        "sales_equals_quantity_times_unit_price_at_cent_precision":{"rows_checked":len(rows),"matches":len(rows)-formula_errors,"mismatches":formula_errors},
        "discount_distribution":dist},
      "calculated_metrics":{"recorded_sales":fmt(sales),"profit":fmt(profit),"shipping_cost":fmt(shipping),
        "profit_less_shipping_assumption":fmt(profit-shipping),"profit_to_recorded_sales_pct":pct(profit/sales),
        "post_shipping_profit_to_recorded_sales_pct":pct((profit-shipping)/sales),"orders":orders,"unique_customers":customers,
        "average_order_value":fmt(sales/D(orders)),"average_profit_per_order":fmt(profit/D(orders)),
        "mean_discount_pct":pct(sum(discounts,ZERO)/D(len(discounts))),"nonzero_discount_orders":discounted,
        "nonzero_discount_share_pct":pct(D(discounted)/D(len(rows))),"estimated_discount_value_before_order_rounding":fmt(discount_est),
        "discount_adjusted_sales_proxy":fmt(sales_proxy),"sales_weighted_estimated_discount_pct":pct(discount_est/sales),
        "average_shipping_cost":fmt(shipping/D(orders)),"sales_to_shipping_cost_ratio":fmt(sales/shipping)+"x",
        "discount_profit_pearson_correlation":f"{corr:.3f}","total_quantity":str(int(total(rows,"Quantity")))},
      "interpretation_caveats":["Sales is pre-discount because it equals Quantity × UnitPrice.","Discount value and discount-adjusted Sales are proxies, not explicit source measures.",
        "Profit less ShippingCost assumes Profit excludes shipping.","Currency and the source Profit formula are not explicitly stored."]}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with (args.output_dir/"data-quality-audit.json").open("w",encoding="utf-8") as h:
        json.dump(report,h,indent=2,ensure_ascii=False);h.write("\n")
    print("Audited",len(rows),"records. Missing cells:",sum(missing.values()),"duplicate rows:",duplicate_rows,"Sales formula mismatches:",formula_errors)
    print("Recorded Sales:",fmt(sales),"Profit:",fmt(profit),"ShippingCost:",fmt(shipping))
if __name__=="__main__": main()
