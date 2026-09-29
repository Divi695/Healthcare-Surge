const form = document.getElementById('predictionForm');
const result = document.getElementById('result');
const predictionText = document.getElementById('predictionText');
const probabilityText = document.getElementById('probabilityText');

form.addEventListener('submit', async function (event) {
  event.preventDefault();

  const data = {
    age: Number(document.getElementById('age').value),
    gender: Number(document.getElementById('gender').value),
    total_bilirubin: Number(document.getElementById('total_bilirubin').value),
    direct_bilirubin: Number(document.getElementById('direct_bilirubin').value),
    alkaline_phosphotase: Number(document.getElementById('alkaline_phosphotase').value),
    alamine_aminotransferase: Number(document.getElementById('alamine_aminotransferase').value),
    aspartate_aminotransferase: Number(document.getElementById('aspartate_aminotransferase').value),
    total_proteins: Number(document.getElementById('total_proteins').value),
    albumin: Number(document.getElementById('albumin').value),
    albumin_and_globulin_ratio: Number(document.getElementById('albumin_and_globulin_ratio').value)
  };

  predictionText.textContent = 'Checking...';
  probabilityText.textContent = '';
  result.classList.remove('hidden');

  try {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const output = await response.json();
    if (!response.ok) throw new Error(output.error || 'Prediction failed');

    predictionText.textContent = output.prediction;
    probabilityText.textContent = `Risk probability: ${(output.probability * 100).toFixed(2)}%`;
  } catch (error) {
    predictionText.textContent = 'Backend connection error';
    probabilityText.textContent = 'Please make sure the Python backend is running on port 5000.';
    console.error(error);
  }
});
