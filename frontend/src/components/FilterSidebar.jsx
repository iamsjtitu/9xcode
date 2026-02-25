import React from 'react';
import { categories, operatingSystems, difficultyLevels } from '../data/mockData';
import * as Icons from 'lucide-react';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

const FilterSidebar = ({ filters, setFilters }) => {
  const toggleFilter = (type, value) => {
    setFilters((prev) => {
      const currentValues = prev[type] || [];
      const newValues = currentValues.includes(value)
        ? currentValues.filter((v) => v !== value)
        : [...currentValues, value];
      return { ...prev, [type]: newValues };
    });
  };

  const getIcon = (iconName) => {
    const Icon = Icons[iconName];
    return Icon ? <Icon className="h-4 w-4" /> : null;
  };

  return (
    <aside className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 sticky top-24 max-h-[calc(100vh-120px)] overflow-y-auto">
      <h3 className="text-lg font-bold text-slate-900 mb-4">Filters</h3>

      {/* Categories */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-slate-700 mb-3">Categories</h4>
        <div className="space-y-2">
          {categories.map((category) => {
            const isSelected = filters.category?.includes(category.slug);
            return (
              <button
                key={category.id}
                onClick={() => toggleFilter('category', category.slug)}
                className={`w-full flex items-center space-x-2 px-3 py-2 rounded-lg text-sm transition-all ${
                  isSelected
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-slate-600 hover:bg-slate-50 border border-transparent'
                }`}
              >
                {getIcon(category.icon)}
                <span className="flex-1 text-left">{category.name}</span>
                {isSelected && (
                  <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <Separator className="my-6" />

      {/* Operating Systems */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-slate-700 mb-3">Operating System</h4>
        <div className="space-y-2">
          {operatingSystems.map((os) => {
            const isSelected = filters.os?.includes(os.slug);
            return (
              <button
                key={os.id}
                onClick={() => toggleFilter('os', os.slug)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all ${
                  isSelected
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-slate-600 hover:bg-slate-50 border border-transparent'
                }`}
              >
                <span>{os.name}</span>
                {isSelected && (
                  <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <Separator className="my-6" />

      {/* Difficulty */}
      <div>
        <h4 className="text-sm font-semibold text-slate-700 mb-3">Difficulty</h4>
        <div className="space-y-2">
          {difficultyLevels.map((level) => {
            const isSelected = filters.difficulty?.includes(level.slug);
            return (
              <button
                key={level.id}
                onClick={() => toggleFilter('difficulty', level.slug)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all ${
                  isSelected
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-slate-600 hover:bg-slate-50 border border-transparent'
                }`}
              >
                <span>{level.name}</span>
                {isSelected && (
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: level.color }}></div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Clear Filters */}
      {(filters.category?.length > 0 || filters.os?.length > 0 || filters.difficulty?.length > 0) && (
        <button
          onClick={() => setFilters({})}
          className="w-full mt-6 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors"
        >
          Clear All Filters
        </button>
      )}
    </aside>
  );
};

export default FilterSidebar;