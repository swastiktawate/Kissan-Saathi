import datetime
import uuid

MOCK_NEWS = [
    {
        "title": "Government imposes export ban on onions to curb local price rise",
        "summary": "In a sudden move to control domestic inflation, the government has announced an immediate export ban on onions until further notice. Traders are halting procurement.",
        "source_url": "https://pib.gov.in/example-export-ban",
        "date": datetime.date.today().isoformat()
    },
    {
        "title": "Cabinet approves higher MSP for Kharif crops",
        "summary": "The Cabinet Committee on Economic Affairs has approved an increase in the Minimum Support Price (MSP) for all mandated Kharif crops to ensure remunerative prices to the growers for their produce.",
        "source_url": "https://pib.gov.in/example-msp",
        "date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    },
    {
        "title": "New solar pump subsidy announced for farmers in Maharashtra",
        "summary": "The state government launched a new scheme providing up to 90% subsidy for solar water pumps to reduce dependence on the erratic power grid.",
        "source_url": "https://example.com/subsidy",
        "date": (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    },
    {
        "title": "Heavy rain and weather alert issued for coastal regions",
        "summary": "The IMD has issued a severe weather alert forecasting unseasonal heavy rains that may impact standing vegetable crops in the coastal belt.",
        "source_url": "https://mausam.imd.gov.in/example-alert",
        "date": (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    },
    {
        "title": "Import duty reduced on edible oils",
        "summary": "The government has slashed the import duty on crude palm oil and sunflower oil to ease retail prices during the festival season.",
        "source_url": "https://pib.gov.in/example-import-duty",
        "date": (datetime.date.today() - datetime.timedelta(days=5)).isoformat()
    }
]

def get_policy_alerts():
    alerts = []
    for news in MOCK_NEWS:
        text_to_scan = (news["title"] + " " + news["summary"]).lower()
        
        severity = "Low"
        category = "General"
        
        # Keyword scanning
        if "export ban" in text_to_scan or "import duty" in text_to_scan:
            severity = "High"
            category = "Trade Policy"
        elif "weather alert" in text_to_scan or "msp" in text_to_scan:
            severity = "Medium"
            category = "Market & Weather"
        elif "subsidy" in text_to_scan:
            severity = "Low"
            category = "Government Scheme"
            
        alerts.append({
            "id": str(uuid.uuid4()),
            "title": news["title"],
            "summary": news["summary"],
            "category": category,
            "severity": severity,
            "source_url": news["source_url"],
            "date": news["date"]
        })
    
    return alerts
