import os
from agents import BoxOfficeAgent  

def test_box_office_agent():
    agent = BoxOfficeAgent()

    state_with_title = {
        "metadata": {"Title": "Inception"}  
    }
    result = agent.fetch_box_office(state_with_title)
    print("\n--- Test Case 1: Valid Metadata ---")
    print(f"Box Office Data: {result['box_office']}")

    state_no_title = {"metadata": {}}
    result = agent.fetch_box_office(state_no_title)
    print("\n--- Test Case 2: No Title in Metadata ---")
    print(f"Box Office Data: {result['box_office']}")

    state_no_metadata = {}
    result = agent.fetch_box_office(state_no_metadata)
    print("\n--- Test Case 3: No Metadata ---")
    print(f"Box Office Data: {result['box_office']}")

if __name__ == "__main__":
    test_box_office_agent()
