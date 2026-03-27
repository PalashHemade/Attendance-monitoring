"use client";

import { useState } from "react";
import axios from "axios";
import UploadBox from "@/components/UploadBox";
import DefaulterTable, { Student } from "@/components/DefaulterTable";
import { FileText, Download } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [defaulters, setDefaulters] = useState<Student[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (uploadedFile: File) => {
    setFile(uploadedFile);
    setError(null);
    setLoading(true);
    setDefaulters(null);

    const formData = new FormData();
    formData.append("file", uploadedFile);

    try {
      const { data } = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setDefaulters(data.defaulters);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error parsing file.");
    } finally {
      setLoading(false);
    }
  };

  const generateLetters = async () => {
    if (!defaulters || defaulters.length === 0) return;
    setGenerating(true);
    setError(null);
    
    try {
      const response = await axios.post("http://localhost:8000/generate-letters", defaulters, {
        responseType: "blob", 
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "defaulter_letters.pdf");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err: any) {
      setError("Error generating PDF letters.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 py-12 px-4 sm:px-6 lg:px-8 font-sans transition-colors duration-200">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center p-3 bg-blue-100 dark:bg-blue-900/30 rounded-2xl mb-4">
            <FileText className="h-8 w-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl text-gray-900 dark:text-white">
            Attendance Defaulter
            <span className="block text-blue-600 dark:text-blue-500">Letter Generator</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-gray-500 dark:text-gray-400">
            Upload your attendance report (.csv or .xlsx) to instantly identify students under 75% attendance and generate professional warning letters.
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 shadow-xl shadow-gray-200/50 dark:shadow-none rounded-3xl p-6 sm:p-10 border border-gray-100 dark:border-gray-800">
          <UploadBox onUpload={handleUpload} />

          {error && (
            <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-xl border border-red-200 dark:border-red-800/30 flex items-center">
              <span className="font-semibold">{error}</span>
            </div>
          )}

          {loading && (
            <div className="mt-8 flex justify-center pb-4">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
            </div>
          )}

          {defaulters && (
            <div className="mt-10 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <h2 className="text-2xl font-bold">
                  Defaulters List <span className="text-sm font-medium text-gray-500 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full ml-2">{defaulters.length} Found</span>
                </h2>
                {defaulters.length > 0 && (
                  <button
                    onClick={generateLetters}
                    disabled={generating}
                    className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-xl font-bold transition-all shadow-md shadow-blue-500/30 active:scale-95"
                  >
                    {generating ? (
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    ) : (
                      <Download className="h-5 w-5" />
                    )}
                    Generate PDF Letters
                  </button>
                )}
              </div>
              <DefaulterTable defaulters={defaulters} />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
