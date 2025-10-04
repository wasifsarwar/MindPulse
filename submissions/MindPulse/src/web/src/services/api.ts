import { SurveyRequest, SurveyResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const analyzeSurvey = async (data: SurveyRequest): Promise<SurveyResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/analyze-survey`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return response.json();
};

