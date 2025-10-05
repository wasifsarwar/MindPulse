import React from 'react';
import { SurveyResponse } from '../types';

interface ResultDisplayProps {
    result: SurveyResponse;
    onNewCheckIn: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onNewCheckIn }) => {
    const getRiskColor = (level: string) => {
        switch (level) {
            case 'low':
                return '#10b981';
            case 'moderate':
                return '#f59e0b';
            case 'high':
                return '#ef4444';
            default:
                return '#6b7280';
        }
    };

    return (
        <div className="result-display">
            {result.provider_contacted && (
                <div className="provider-alert">
                    <div className="provider-alert-icon">📞</div>
                    <div className="provider-alert-content">
                        <strong>Your healthcare provider has been notified</strong>
                        <p>Based on your responses, we've alerted your provider. They may reach out to you soon.</p>
                    </div>
                </div>
            )}

            <div className="result-header">
                <h2>Your Check-In Results</h2>
                <div
                    className="risk-badge"
                    style={{ backgroundColor: getRiskColor(result.risk_level) }}
                >
                    {result.risk_level} risk
                </div>
            </div>

            <div className="result-message">
                <div className="message-icon">💙</div>
                <p>{result.message}</p>
            </div>

            {result.recommendations.length > 0 && (
                <div className="recommendations">
                    <h3>Personalized Recommendations</h3>
                    <ul>
                        {result.recommendations.map((rec, index) => (
                            <li key={index}>
                                <span className="rec-icon">✓</span>
                                {rec}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {result.key_concerns.length > 0 && (
                <div className="concerns">
                    <h4>Areas we're monitoring:</h4>
                    <div className="concern-tags">
                        {result.key_concerns.map((concern, index) => (
                            <span key={index} className="concern-tag">
                                {concern.replace(/_/g, ' ')}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            <div className="result-footer">
                <p className="disclaimer">
                    Remember: This is supportive guidance, not medical advice.
                    Please consult a healthcare professional for personalized care.
                </p>
                <button onClick={onNewCheckIn} className="new-checkin-button">
                    Start New Check-In
                </button>
            </div>

            <div className="crisis-resources">
                <p className="crisis-text">
                    <strong>In crisis?</strong> Call 988 (Suicide Prevention Lifeline) or text HOME to 741741
                </p>
            </div>
        </div>
    );
};

export default ResultDisplay;

