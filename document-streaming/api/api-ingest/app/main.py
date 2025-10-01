#import FastAPI modules 
from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import json

#import Pydantic models
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime,time

#create class (model) for the data to be ingested
class RideBooking(BaseModel):
    Date: str = Field(..., example="2024-03-23")
    Time: str = Field(..., example="12:29:38")
    Booking_ID: str = Field(..., alias="Booking ID", example="CNR5884300")
    Booking_Status: str = Field(..., alias="Booking Status", example="Completed")
    Customer_ID: str = Field(..., alias="Customer ID", example="CID1982111")
    Vehicle_Type: str = Field(..., alias="Vehicle Type", example="eBike")
    Pickup_Location: str = Field(..., alias="Pickup Location", example="Palam Vihar")
    Drop_Location: str = Field(..., alias="Drop Location", example="Jhilmil")
    Booking_Value: Optional[float] = Field(None, alias="Booking Value", example=250.50)
    Ride_Distance: Optional[float] = Field(None, alias="Ride Distance", example=15.3)
    Driver_Ratings: Optional[float] = Field(None, alias="Driver Ratings", example=4.5)
    Customer_Rating: Optional[float] = Field(None, alias="Customer Rating", example=4.8)
    Payment_Method: Optional[str] = Field(None, alias="Payment Method", example="Credit Card")


#initialize FastAPI app
app = FastAPI()


# Define a root endpoint
@app.get("/", tags=["Root"])
async def root()-> dict:
    return {"message": "Welcome to the Ride Booking Ingestion API!"}

# Define a POST endpoint to ingest ride booking data
@app.post("/ride-booking", status_code=status.HTTP_201_CREATED, tags=["Ingestion"])
async def post_ride_booking(ride_booking: RideBooking) -> JSONResponse:
    try:
        # Convert the Pydantic model to a dictionary
        ride_booking_dict = ride_booking.model_dump(by_alias=True)
        
        # Convert the dictionary to a JSON string
        ride_booking_json = json.dumps(ride_booking_dict)

        #print(ride_booking_json)
        print(ride_booking_json)
        
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Ride booking data ingested successfully."})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while ingesting data: {str(e)}")