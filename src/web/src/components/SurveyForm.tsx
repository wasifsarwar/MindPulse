import React, { useState } from 'react';
import { SurveyRequest } from '../types';

interface SurveyFormProps {
    onSubmit: (data: SurveyRequest) => void;
    isLoading: boolean;
}

const SurveyForm: React.FC<SurveyFormProps> = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState<SurveyRequest>({
        medication_taken: false,
        mood_rating: 5,
        sleep_quality: 5,
        physical_activity: 5,
        thoughts: '',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="survey-form">
            <div className="form-header">
                <h2>Daily Check-In</h2>
                <p>Let's see how you're doing today</p>
            </div>

            {/* Question 1: Medication */}
            <div className="form-group">
                <label className="checkbox-label">
                    <input
                        type="checkbox"
                        checked={formData.medication_taken}
                        onChange={(e) => setFormData({ ...formData, medication_taken: e.target.checked })}
                        className="checkbox-input"
                    />
                    <span className="checkbox-text">I took my medication today</span>
                </label>
            </div>

            {/* Question 2: Mood */}
            <div className="form-group">
                <label className="slider-label">
                    <span className="label-text">How would you rate your mood today?</span>
                    <span className="rating-value">{formData.mood_rating}/10</span>
                </label>
                <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.mood_rating}
                    onChange={(e) => setFormData({ ...formData, mood_rating: parseInt(e.target.value) })}
                    className="slider"
                />
                <div className="slider-labels">
                    <span>Low</span>
                    <span>High</span>
                </div>
            </div>

            {/* Question 3: Sleep */}
            <div className="form-group">
                <label className="slider-label">
                    <span className="label-text">How would you rate your sleep quality last night?</span>
                    <span className="rating-value">{formData.sleep_quality}/10</span>
                </label>
                <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.sleep_quality}
                    onChange={(e) => setFormData({ ...formData, sleep_quality: parseInt(e.target.value) })}
                    className="slider"
                />
                <div className="slider-labels">
                    <span>Poor</span>
                    <span>Excellent</span>
                </div>
            </div>

            {/* Question 4: Activity */}
            <div className="form-group">
                <label className="slider-label">
                    <span className="label-text">What was your level of physical activity lately?</span>
                    <span className="rating-value">{formData.physical_activity}/10</span>
                </label>
                <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.physical_activity}
                    onChange={(e) => setFormData({ ...formData, physical_activity: parseInt(e.target.value) })}
                    className="slider"
                />
                <div className="slider-labels">
                    <span>None</span>
                    <span>Very Active</span>
                </div>
            </div>

            {/* Question 5: Thoughts */}
            <div className="form-group">
                <label className="textarea-label">
                    <span className="label-text">What's been on your mind?</span>
                </label>
                <textarea
                    value={formData.thoughts}
                    onChange={(e) => setFormData({ ...formData, thoughts: e.target.value })}
                    placeholder="Share what you've been thinking about or feeling..."
                    className="textarea-input"
                    rows={4}
                    required
                />
            </div>

            <button type="submit" className="submit-button" disabled={isLoading}>
                {isLoading ? (
                    <>
                        <span className="spinner"></span>
                        Analyzing...
                    </>
                ) : (
                    'Submit Check-In'
                )}
            </button>
        </form>
    );
};

export default SurveyForm;

