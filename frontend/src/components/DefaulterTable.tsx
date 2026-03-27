"use client";

export interface Subject {
  name: string;
  theory: string;
  practical: string;
}

export interface Student {
  name: string;
  roll_no: string | number;
  class_name: string;
  attendance: number;
  subjects?: Subject[];
  overall_th?: string;
  overall_pr?: string;
}

interface DefaulterTableProps {
  defaulters: Student[];
}

export default function DefaulterTable({ defaulters }: DefaulterTableProps) {
  if (defaulters.length === 0) {
    return (
      <div className="text-center p-8 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 mt-6 shadow-sm">
        <p className="text-gray-500 dark:text-gray-400 text-lg">
          No defaulters found below 75% attendance!
        </p>
      </div>
    );
  }

  return (
    <div className="mt-8 overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 text-sm">
          <thead className="bg-gray-50 dark:bg-gray-800/80">
            <tr>
              <th className="px-6 py-4 text-left font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider text-xs">Name</th>
              <th className="px-6 py-4 text-left font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider text-xs">Roll No</th>
              <th className="px-6 py-4 text-left font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider text-xs">Class</th>
              <th className="px-6 py-4 text-left font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider text-xs">Attendance %</th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
            {defaulters.map((s, idx) => (
              <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-gray-800 dark:text-gray-200 font-medium">{s.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600 dark:text-gray-400">{s.roll_no}</td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600 dark:text-gray-400">{s.class_name}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400">
                    {s.attendance}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
