"use client";

import { useDropzone } from "react-dropzone";
import { UploadCloud } from "lucide-react";

interface UploadBoxProps {
  onUpload: (file: File) => void;
}

export default function UploadBox({ onUpload }: UploadBoxProps) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "text/csv": [".csv"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onUpload(acceptedFiles[0]);
      }
    },
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
        isDragActive
          ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
          : "border-gray-300 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500"
      }`}
    >
      <input {...getInputProps()} />
      <UploadCloud className="mx-auto h-12 w-12 text-blue-500 mb-4" />
      {isDragActive ? (
        <p className="text-blue-500 font-semibold text-lg">Drop the attendance report here...</p>
      ) : (
        <p className="text-gray-600 dark:text-gray-300 text-lg">
          Drag & drop a <span className="font-semibold text-blue-600 dark:text-blue-400">CSV</span> or <span className="font-semibold text-blue-600 dark:text-blue-400">Excel</span> file here, or click to select
        </p>
      )}
    </div>
  );
}
