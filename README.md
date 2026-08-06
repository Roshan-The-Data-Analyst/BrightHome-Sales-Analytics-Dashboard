# 🏠 BrightHome Retail — Sales & Performance Analysis

A Power BI portfolio project analyzing 2,500 retail transactions across BrightHome's store network in the US, covering sales performance, customer behavior, and product trends. Built with **Power Query** for data transformation and **DAX** for business-ready metrics.

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-0078D4?style=flat)
![Power Query](https://img.shields.io/badge/Power%20Query-217346?style=flat)

---

## 📌 Project Overview

BrightHome Retail is a fictional home goods retailer with multiple store locations. This project simulates a real-world analytics engagement: raw, disconnected data is cleaned and modeled into a star schema, then turned into an interactive Power BI dashboard that answers key business questions for store and category managers.

**Dataset:** 2,500 rows across 4 related tables — Sales, Products, Customers, Stores.

---

## 🎯 Business Questions Answered

1. What is the total sales revenue?
$1,067,061.93
2. What is the total profit?
$198,747.08
3. What is the overall profit margin?
18.63%
4. Which region generates the highest sales?
South
5. Which region generates the lowest sales?
Midwest
6. Which region is most profitable?
West
7. Which category has the highest total sales?
Furniture
8. Which category has the lowest total sales?
Decor
9. Which category is the most profitable?
Furniture
10. Which product generates the highest total sales?
Office Chair

---

## 🗂️ Data Model

The four source tables are modeled into a star schema in Power BI:


## 📐 Key DAX Measures



Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

## 📊 Dashboard Preview

<img width="577" height="326" alt="dashboard 01" src="https://github.com/user-attachments/assets/30b71c49-7df3-44ca-922b-eb93e3a285eb" />


**Pages included:**
1. Executive Overview — revenue, profit, and trend KPIs
2. Store Performance — regional and store-level comparison
3. Product Insights — category and margin breakdown

---


## 🛠️ Tools Used

| Tool | Purpose |
|---|---|
| Power Query | Data cleaning & transformation |
| Power BI (Data Model) | Star schema modeling & relationships |
| DAX | Calculated measures & KPIs |
| Power BI Service | Publishing & sharing |

---

## 📁 Repository Structure

brighthome-retail/
├── data/
│   ├── sales.csv
│   ├── products.csv
│   ├── customers.csv
│   └── stores.csv
├── BrightHome_Retail_Dashboard.pbix
├── assets/
│   └── dashboard-overview.png
└── README.md



## 👤 About This Project

Built as part of a data analytics portfolio to demonstrate end-to-end BI workflow: data cleaning (Power Query) → data modeling → DAX measures → dashboard storytelling.
