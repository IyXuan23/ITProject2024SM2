import React, { useState } from 'react';

const styles: { [key: string]: React.CSSProperties } = {
  sidebar: {
    position: 'fixed',
    top: '150px', 
    right: '20px',
    width: '250px',
    backgroundColor: '#e0f2ff',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
    zIndex: 1000,
  },
  filterItem: {
    marginBottom: '20px',
  },
  select: {
    width: '100%',
    padding: '8px',
    borderRadius: '4px',
    border: '1px solid #ccc',
  },
};

export default function FilterSidebar() {
  const initialFilters = {
    version: 'Current Handbook — 2024',
    subjectLevel: 'All subject levels',
    studyPeriod: 'All study periods',
    areaOfStudy: 'All areas of study',
    faculty: 'All faculties/departments',
    breadthCourse: 'No course selected',
    campus: 'All campuses',
  };

  const [filters, setFilters] = useState(initialFilters);

  const handleReset = () => {
    setFilters(initialFilters);
  };

  const handleUpdateResults = () => {
    // 在这里实现更新结果的逻辑
    console.log('Filters applied:', filters);
  };

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>, field: keyof typeof filters) => {
    setFilters({
      ...filters,
      [field]: e.target.value,
    });
  };

  return (
    <div style={styles.sidebar}>
      <div style={styles.filterItem}>
        <label>Version</label>
        <select 
          style={styles.select} 
          value={filters.version} 
          onChange={(e) => handleChange(e, 'version')}
        >
          <option>Current Handbook — 2024</option>
          <option>Previous Handbook — 2023</option>
        </select>
      </div>
      
      <div style={styles.filterItem}>
        <label>Subject Levels</label>
        <select 
          style={styles.select} 
          value={filters.subjectLevel} 
          onChange={(e) => handleChange(e, 'subjectLevel')}
        >
          <option>All subject levels</option>
          <option>Undergraduate</option>
          <option>Postgraduate</option>
        </select>
      </div>
      
      <div style={styles.filterItem}>
        <label>Study Periods</label>
        <select 
          style={styles.select} 
          value={filters.studyPeriod} 
          onChange={(e) => handleChange(e, 'studyPeriod')}
        >
          <option>All study periods</option>
          <option>Semester 1</option>
          <option>Semester 2</option>
        </select>
      </div>
      
      <div style={styles.filterItem}>
        <label>Areas of Study</label>
        <select 
          style={styles.select} 
          value={filters.areaOfStudy} 
          onChange={(e) => handleChange(e, 'areaOfStudy')}
        >
          <option>All areas of study</option>
          <option>Science</option>
          <option>Arts</option>
        </select>
      </div>
      
      <div style={styles.filterItem}>
        <label>Faculties/departments</label>
        <select 
          style={styles.select} 
          value={filters.faculty} 
          onChange={(e) => handleChange(e, 'faculty')}
        >
          <option>All faculties/departments</option>
          <option>Faculty of Science</option>
          <option>Faculty of Arts</option>
        </select>
      </div>
      
      <div style={styles.filterItem}>
        <label>Breadth in Courses</label>
        <select 
          style={styles.select} 
          value={filters.breadthCourse} 
          onChange={(e) => handleChange(e, 'breadthCourse')}
        >
          <option>No course selected</option>
          <option>Course A</option>
          <option>Course B</option>
        </select>
      </div>
      
      <div style={styles.filterItem}>
        <label>Campuses</label>
        <select 
          style={styles.select} 
          value={filters.campus} 
          onChange={(e) => handleChange(e, 'campus')}
        >
          <option>All campuses</option>
          <option>Parkville</option>
          <option>Southbank</option>
        </select>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
        <button
          onClick={handleReset}
          style={{
            padding: '10px 20px',
            backgroundColor: '#ff4d4f',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Reset
        </button>
        <button
          onClick={handleUpdateResults}
          style={{
            padding: '10px 20px',
            backgroundColor: '#1890ff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Update Results
        </button>
      </div>
    </div>
  );
}
