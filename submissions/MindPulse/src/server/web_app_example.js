/**
 * Example: How to call the survey endpoint from your web app
 * 
 * This shows how to send survey responses and display the results
 */

// Example survey data from your web app form
const surveyResponses = {
  medication_taken: false,  // Checkbox value
  mood_rating: 4,           // Slider 1-10
  sleep_quality: 3,         // Slider 1-10
  physical_activity: 2,     // Slider 1-10
  thoughts: "I've been feeling overwhelmed with work and can't seem to catch up..."
};

// Function to analyze survey
async function analyzeSurvey(responses) {
  try {
    const response = await fetch('http://localhost:8000/api/analyze-survey', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(responses)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error analyzing survey:', error);
    throw error;
  }
}

// Example usage
async function handleSurveySubmit() {
  try {
    console.log('Sending survey responses...');
    
    const result = await analyzeSurvey(surveyResponses);
    
    // Display empathetic message
    console.log('\n💬 Message from MindPulse:');
    console.log(result.message);
    
    // Display recommendations
    console.log('\n📝 Recommendations:');
    result.recommendations.forEach((rec, i) => {
      console.log(`  ${i + 1}. ${rec}`);
    });
    
    // Display risk level
    console.log(`\n⚠️  Risk Level: ${result.risk_level}`);
    
    // Display concerns
    if (result.key_concerns.length > 0) {
      console.log(`\n🔍 Key Concerns: ${result.key_concerns.join(', ')}`);
    }
    
    // In your web app, you would update the UI here:
    // - Show message in a card/modal
    // - Display recommendations as a list
    // - Use risk_level to color-code the response
    // - Highlight key_concerns for the user
    
  } catch (error) {
    console.error('Failed to analyze survey:', error);
    // Show error message to user
  }
}

// React Example
function SurveyResult({ result }) {
  return (
    <div className="survey-result">
      <div className="message">
        <p>{result.message}</p>
      </div>
      
      <div className="recommendations">
        <h3>Recommendations</h3>
        <ul>
          {result.recommendations.map((rec, i) => (
            <li key={i}>{rec}</li>
          ))}
        </ul>
      </div>
      
      <div className={`risk-badge risk-${result.risk_level}`}>
        Risk Level: {result.risk_level}
      </div>
      
      {result.key_concerns.length > 0 && (
        <div className="concerns">
          <strong>Areas of concern:</strong> {result.key_concerns.join(', ')}
        </div>
      )}
    </div>
  );
}

// Run the example
handleSurveySubmit();

