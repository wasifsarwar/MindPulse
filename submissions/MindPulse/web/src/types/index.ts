export interface SurveyRequest {
    medication_taken: boolean;
    mood_rating: number;
    sleep_quality: number;
    physical_activity: number;
    thoughts: string;
}

export interface SurveyResponse {
    message: string;
    recommendations: string[];
    risk_level: 'low' | 'moderate' | 'high';
    key_concerns: string[];
    provider_contacted: boolean;
}

