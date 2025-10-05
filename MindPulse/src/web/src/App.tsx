import React, { useState } from 'react';
import SurveyForm from './components/SurveyForm';
import ResultDisplay from './components/ResultDisplay';
import { analyzeSurvey } from './services/api';
import { SurveyRequest, SurveyResponse } from './types';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SurveyResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: SurveyRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await analyzeSurvey(data);

      // Debug logging
      console.log('=== MindPulse API Response ===');
      console.log('Risk Level:', response.risk_level);
      console.log('Provider Contacted:', response.provider_contacted);
      console.log('Key Concerns:', response.key_concerns);
      console.log('Full Response:', response);
      console.log('==============================');

      setResult(response);
    } catch (err) {
      setError('Unable to connect to MindPulse. Please make sure the server is running.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewCheckIn = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <div className="logo">
            <span className="logo-icon">🧠</span>
            <h1>MindPulse</h1>
          </div>
          <p className="tagline">Your daily mental health companion</p>
        </header>

        <main className="app-main">
          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
              <button onClick={handleNewCheckIn} className="error-retry">
                Try Again
              </button>
            </div>
          )}

          {!result && !error && (
            <SurveyForm onSubmit={handleSubmit} isLoading={isLoading} />
          )}

          {result && (
            <ResultDisplay result={result} onNewCheckIn={handleNewCheckIn} />
          )}
        </main>

        <footer className="app-footer">
        </footer>
      </div>
    </div>
  );
}

export default App;

