import pdfplumber
import sqlite3
import re

# File paths for the three years
pdf_files = {
    "2021": r"D:\Develop\Finance\caibao_data\2021data.pdf",
    "2022": r"D:\Develop\Finance\caibao_data\2022data.pdf",
    "2023": r"D:\Develop\Finance\caibao_data\2023data.pdf",
}

# Predefined item names (from 11 images)
item_names = [
    "货币资金", "结算备付金", "拆出资金", "交易性金融资产", "衍生金融资产", "应收票据", "应收账款", "应收款项融资",
    "预付款项", "应收保费", "应收分保账款", "应收分保合同准备金", "其他应收款", "其中：应收利息",
    "应收股利", "买入返售金融资产", "存货", "合同资产", "持有待售资产", "一年内到期的非流动资产",
    "其他流动资产", "流动资产合计", "非流动资产", "发放贷款和垫款", "债权投资", "其他债权投资",
    "长期应收款", "长期股权投资", "其他权益工具投资", "其他非流动金融资产", "投资性房地产",
    "固定资产", "在建工程", "生产性生物资产", "油气资产", "使用权资产", "无形资产",
    "开发支出", "商誉", "长期待摊费用", "递延所得税资产", "其他非流动资产", "非流动资产合计",
    "资产总计", "流动负债", "短期借款", "向中央银行借款", "拆入资金", "交易性金融负债",
    "衍生金融负债", "应付票据", "应付账款", "预收款项", "合同负债", "卖出回购金融资产款",
    "吸收存款及同业存放", "代理买卖证券款", "代理承销证券款", "应付职工薪酬", "应交税费",
    "其他应付款", "其中：应付利息", "应付股利", "应付手续费及佣金", "应付分保账款",
    "持有待售负债", "一年内到期的非流动负债", "其他流动负债", "流动负债合计", "非流动负债",
    "保险合同准备金", "长期借款", "应付债券", "其中：优先股", "永续债", "租赁负债",
    "长期应付款", "长期应付职工薪酬", "预计负债", "递延收益", "递延所得税负债", "其他非流动负债",
    "非流动负债合计", "负债合计", "所有者权益", "股本", "其他权益工具", "其中：优先股",
    "永续债", "资本公积", "减：库存股", "其他综合收益", "专项储备", "盈余公积", "一般风险准备",
    "未分配利润", "归属于母公司所有者权益合计", "少数股东权益", "所有者权益合计", "负债和所有者权益总计"
]

# Function to extract all text from a PDF file
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to normalize text (removing extra spaces, fixing line breaks)
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces/newlines with a single space
    text = text.replace("：", "")  # Remove colons to match item names better
    return text.strip()

# Function to extract values for predefined item names
def extract_values(text):
    text = clean_text(text)  # Clean extracted text
    extracted_values = {item: 0 for item in item_names}  # Initialize with zeros

    for item in item_names:
        pattern = rf"{item}\s*([\d,]+)"  # Match number after item name
        match = re.search(pattern, text)
        if match:
            value = match.group(1).replace(',', '')  # Remove commas
            extracted_values[item] = float(value) if value else 0
    return extracted_values

# Extract text and match values for all three years
extracted_data = {
    year: extract_values(extract_text_from_pdf(path))
    for year, path in pdf_files.items()
}

# Connect to SQLite and insert data
conn = sqlite3.connect("financial_data.db")
cursor = conn.cursor()

# Create table for financial data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS financial_data (
        item_name TEXT PRIMARY KEY,
        year_2021 REAL,
        year_2022 REAL,
        year_2023 REAL
    )
''')

# Insert extracted data into SQLite using `INSERT OR REPLACE` to avoid duplicates
for item_name in item_names:
    cursor.execute('''
        INSERT OR REPLACE INTO financial_data (item_name, year_2021, year_2022, year_2023)
        VALUES (?, ?, ?, ?)
    ''', (
        item_name,
        extracted_data["2021"].get(item_name, 0),
        extracted_data["2022"].get(item_name, 0),
        extracted_data["2023"].get(item_name, 0)
    ))

# Commit and close
conn.commit()
conn.close()

print("✅ Data has been inserted into the SQLite database successfully.")
