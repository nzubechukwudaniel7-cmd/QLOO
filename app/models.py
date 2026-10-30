from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResidentProfile(BaseModel):
    id: Optional[str] = "res_001"
    name: str = Field(..., example="Eleanor Vance")
    age: int = Field(..., example=82)
    birth_decade: str = Field(..., example="1940s")
    hometown: str = Field(..., example="Chicago, IL")
    youth_anchors: List[str] = Field(
        default_factory=list,
        example=["Nat King Cole", "Humphrey Bogart", "Chicago Jazz"]
    )
    notes: Optional[str] = "Mild-to-moderate vascular dementia with late-afternoon sundowning syndrome."

class SundowningTrigger(BaseModel):
    time_of_day: str = Field(default="16:30 (Late Afternoon)", example="16:30")
    agitation_level: int = Field(..., ge=1, le=10, example=8, description="1=Calm, 10=Severe Distress/Combative")
    primary_symptoms: List[str] = Field(
        default_factory=lambda: ["Pacing hallway", "Repetitive crying to go home", "Refusing evening meal"]
    )
    sensory_sensitivities: List[str] = Field(
        default_factory=lambda: ["Sensitive to sharp brass sounds", "Disoriented by flickering lights"]
    )
    # Tri-Modal Biofeedback Telemetry (Contactless rPPG, BLE Wearable, Manual)
    biometric_source: Optional[str] = Field(default="manual_clinical", example="contactless_rppg")
    heart_rate_bpm: Optional[int] = Field(default=None, example=94)
    hrv_rmssd_ms: Optional[float] = Field(default=None, example=22.4)

class IntakeRequest(BaseModel):
    resident: ResidentProfile
    trigger: SundowningTrigger

class SensoryPillarItem(BaseModel):
    entity_id: str
    name: str
    category: str  # auditory, visual, olfactory_culinary, literary
    qloo_type: str  # urn:entity:artist, urn:entity:movie, etc.
    affinity_score: float
    image_url: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    therapeutic_rationale: str
    sensory_instructions: str  # e.g., "Play at 45 dB volume; soft lighting"

class ReminiscenceProtocol(BaseModel):
    protocol_id: str
    resident_name: str
    resident_age: int
    birth_decade: str
    hometown: str
    initial_agitation_level: int
    created_at: str
    qloo_resolved_anchors: List[Dict[str, Any]]
    auditory_pillar: List[SensoryPillarItem]
    visual_pillar: List[SensoryPillarItem]
    culinary_olfactory_pillar: List[SensoryPillarItem]
    verbal_validation_prompts: List[str]
    environmental_settings: Dict[str, Any]
    qloo_telemetry: Dict[str, Any]

class RecalibrationRequest(BaseModel):
    protocol_id: str
    caregiver_observation: str = Field(..., example="Disliked brass trumpet, smiled when acoustic piano played")
    disliked_entity_ids: List[str] = Field(default_factory=list)
    current_agitation_level: int = Field(..., ge=1, le=10, example=6)

class SessionFeedback(BaseModel):
    session_id: str
    protocol_id: str
    pre_agitation_level: int
    post_agitation_level: int
    duration_minutes: int
    interventions_used: List[str]
    caregiver_notes: str
    sedatives_avoided: bool = True
    # Objective Autonomic Validation Telemetry
    biometric_source: Optional[str] = Field(default="manual_clinical", example="contactless_rppg")
    pre_heart_rate_bpm: Optional[int] = None
    post_heart_rate_bpm: Optional[int] = None
    pre_hrv_rmssd_ms: Optional[float] = None
    post_hrv_rmssd_ms: Optional[float] = None
