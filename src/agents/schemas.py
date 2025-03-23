from pydantic import BaseModel, Field

class AvailabilityInput(BaseModel):
    checkin: str = Field(..., description="Check-in date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)")
    checkout: str = Field(..., description="Check-out date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)")

class InfoRequest(BaseModel):
    query: str = Field(..., description="The user question to retrieve contextual information for")

class ReservationData(BaseModel):
    nombre: str = Field(..., description="Name of the guest")
    checkin: str = Field(..., description="Check-in date in ISO 8601 format")
    checkout: str = Field(..., description="Check-out date in ISO 8601 format")
    departamento: int = Field(..., description="Apartment number to reserve")
