import React, { useState } from 'react';

export default function SearchBar() {
    const [showOnly, setShowOnly] = useState('All result types');

  const handleShowOnlyChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setShowOnly(e.target.value);
    console.log(`Show only: ${e.target.value}`);
  };
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      backgroundColor: '#003366', 
      padding: '20px',
      borderRadius: '8px', 
      margin: '30px auto',
      width:'65%',
      position:'relative',
      left:'-150px'
    }}>
      <label style={{
        color: 'white',
        marginRight: '10px',
        fontSize: '18px',
        fontFamily: 'Georgia, serif',
      }}>
        Search for
      </label>
      <input 
        type="text" 
        placeholder="Courses, subjects or keywords" 
        style={{
          width: '400px',
          padding: '10px',
          fontSize: '16px',
          borderRadius: '4px 0 0 4px',
          border: '1px solid #ccc',
          outline: 'none',
        }}
      />
      <button style={{
        padding: '10px 20px',
        fontSize: '16px',
        borderRadius: '0 4px 4px 0',
        backgroundColor: '#336699',
        color: 'white',
        border: 'none',
        cursor: 'pointer',
      }}>
        Search
      </button>
      <div style={{ display: 'flex', alignItems: 'center', marginLeft: '50px' }}>
        <label style={{
          color: 'white',
          marginRight: '20px',
          fontSize: '18px',
          fontFamily: 'Georgia, serif',
        }}>
          Show only
        </label>
        <select
          value={showOnly}
          onChange={handleShowOnlyChange}
          style={{
            padding: '8px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '1px solid #ccc',
          }}
        >
          <option value="All result types">All result types</option>
          <option value="Courses">Courses</option>
          <option value="Subjects">Subjects</option>
          <option value="Breadth Track">Breadth Track</option>
        </select>
      </div>
    </div>
    
  );
}
