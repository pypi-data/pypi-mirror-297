class Secured():
    def __init__(self) -> None:
        print("Constructed secured instance")
    
    def implement(self, model_count: int) -> dict:
        print(f"Implemented securety for {model_count} models!")
        return {"status": True, "message": "Success"}