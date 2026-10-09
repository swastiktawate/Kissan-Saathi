import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.app.ingestion.orchestrator import orchestrate_ingestion

async def main():
    result = await orchestrate_ingestion("Maharashtra", "Vashi", "Tomato")
    print(f"Ingestion finished. Mode: {result['mode']}")
    if result['status'] != 'ok':
        print(f"Error: {result['error']}")
    else:
        print(f"Rows fetched: {len(result['rows_raw'])}")

if __name__ == "__main__":
    asyncio.run(main())
