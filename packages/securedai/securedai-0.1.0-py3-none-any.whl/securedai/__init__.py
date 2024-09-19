class Secured():
    def __init__(self) -> None:
        print("Constructed secured instance")
    
    def implement(self, num):
        print(f"Implemented securety for {num} models!")
        return {"status": True, "message": "Success"}