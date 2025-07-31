import sys
import json

def main():
    try:
        # Get input from PHP
        input_data = json.loads(sys.argv[1])
        
        # Process data (example)
        result = {
            "status": "success",
            "received_data": input_data,
            "processed_result": f"Processed {len(input_data)} items"
        }
        
        # Output JSON to PHP
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()