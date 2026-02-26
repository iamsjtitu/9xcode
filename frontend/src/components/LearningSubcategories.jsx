import React, { useState, useEffect } from 'react';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

const LearningSubcategories = ({ selectedSubcategory, onSubcategoryChange }) => {
  const subcategories = [
    { id: 'all', name: 'All', icon: '📚', tag: null },
    { id: 'tally', name: 'Tally', icon: '📊', tag: 'tally' },
    { id: 'busy', name: 'Busy', icon: '💼', tag: 'busy' },
    { id: 'excel', name: 'MS Excel', icon: '📗', tag: 'excel' },
    { id: 'word', name: 'MS Word', icon: '📘', tag: 'word' },
    { id: 'powerpoint', name: 'PowerPoint', icon: '📙', tag: 'powerpoint' },
    { id: 'photoshop', name: 'Photoshop', icon: '🎨', tag: 'photoshop' },
  ];

  return (
    <div className="mb-6">
      <h3 className="text-sm font-semibold text-slate-700 mb-3">Learning Subcategories</h3>
      <div className="flex flex-wrap gap-2">
        {subcategories.map((subcat) => (
          <Badge
            key={subcat.id}
            onClick={() => onSubcategoryChange(subcat.tag)}
            className={`cursor-pointer text-sm px-4 py-2 transition-all ${
              selectedSubcategory === subcat.tag
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white border-blue-600 shadow-md hover:shadow-lg'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50 hover:border-blue-400'
            }`}
            style={{ borderWidth: '1px' }}
          >
            <span className="mr-1.5">{subcat.icon}</span>
            {subcat.name}
          </Badge>
        ))}
      </div>
      <Separator className="mt-4" />
    </div>
  );
};

export default LearningSubcategories;
