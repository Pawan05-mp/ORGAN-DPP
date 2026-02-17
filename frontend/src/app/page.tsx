"use client";

import { useState } from "react";

interface Molecule {
  smiles: string;
  qed: number | null;
  sa: number | null;
  diversity: number | null;
  validity: boolean;
}

interface GenerateResponse {
  run_id: string;
  molecules: Molecule[];
  summary_metrics: {
    count: number;
    valid: number;
  };
}

export default function Home() {
  const [batchSize, setBatchSize] = useState(64);
  const [temperature, setTemperature] = useState(1.0);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const apiUrl = process.env.NODE_ENV === "production"
        ? "/.netlify/functions/generate"
        : "http://127.0.0.1:8000/api/generate";
      
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          batch_size: batchSize,
          temperature: temperature,
          diversity_weight: 0.1,
          curriculum_stage: 1,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">ORGAN-DPP</h1>
          <p className="text-xl text-gray-600">
            Molecular Generation with Diversity-Promoting Priors
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Generate Molecules
          </h2>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Batch Size: {batchSize}
              </label>
              <input
                type="range"
                min="1"
                max="512"
                value={batchSize}
                onChange={(e) => setBatchSize(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <p className="text-xs text-gray-500 mt-1">1 - 512 molecules</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Temperature: {temperature.toFixed(2)}
              </label>
              <input
                type="range"
                min="0.5"
                max="2.0"
                step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <p className="text-xs text-gray-500 mt-1">0.5 - 2.0 (higher = more diverse)</p>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
            >
              {loading ? "Generating..." : "Generate Molecules"}
            </button>
          </div>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">
                <strong>Error:</strong> {error}
              </p>
            </div>
          )}
        </div>

        {results && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Results</h2>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-indigo-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Total Generated</p>
                <p className="text-3xl font-bold text-indigo-600">
                  {results.summary_metrics.count}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Valid SMILES</p>
                <p className="text-3xl font-bold text-green-600">
                  {results.summary_metrics.valid}
                </p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-100 border-b">
                    <th className="px-4 py-2 text-left font-semibold">SMILES</th>
                    <th className="px-4 py-2 text-center font-semibold">Valid</th>
                    <th className="px-4 py-2 text-center font-semibold">QED</th>
                    <th className="px-4 py-2 text-center font-semibold">SA</th>
                    <th className="px-4 py-2 text-center font-semibold">Diversity</th>
                  </tr>
                </thead>
                <tbody>
                  {results.molecules.slice(0, 10).map((mol, idx) => (
                    <tr key={idx} className="border-b hover:bg-gray-50">
                      <td className="px-4 py-2 font-mono text-xs">
                        {mol.smiles}
                      </td>
                      <td className="px-4 py-2 text-center">
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            mol.validity
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          {mol.validity ? "✓" : "✗"}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-center">
                        {mol.qed?.toFixed(3) || "-"}
                      </td>
                      <td className="px-4 py-2 text-center">
                        {mol.sa?.toFixed(3) || "-"}
                      </td>
                      <td className="px-4 py-2 text-center">
                        {mol.diversity?.toFixed(3) || "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {results.molecules.length > 10 && (
                <p className="text-center text-gray-500 text-sm mt-4">
                  Showing first 10 of {results.molecules.length} molecules
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
